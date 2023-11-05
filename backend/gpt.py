import re
import openai
import logging
from auth import *
from blog_post import BlogPost
from prompt_constructor import GPTBlogPrompts
from flask import jsonify, abort
from wp import *

class GPTApi:

    model_4 = "gpt-4"
    model_35 = "gpt-3.5-turbo"

    def __init__(self, categories: list[tuple]):
        self.categories = categories
        openai.api_key = open_api_key
    

    def get_post_category(self, title) -> str:
        try:
            categoriesListString = str([t[0] for t in self.categories])
            category_prompt = GPTBlogPrompts.CATEGORIES.value.format(title, categoriesListString)
            role_prompt = GPTBlogPrompts.ROLE.value

            categoryResponse = openai.ChatCompletion.create(
                model = self.model_4,
                messages=[
                    {"role": "system", "content": role_prompt},
                    {"role": "user", "content": category_prompt},
                ]
            )

            categoryString = categoryResponse["choices"][0]["message"]["content"]
            chosenCategory = next((t for t in self.categories if t[0] in categoryString), None)

            return chosenCategory
        except Exception as err:
            logging.error(f"Failed to categorize the blog post: {err}")
            raise
            


    def create_blog_post(self, title, keywords: list, status) -> BlogPost:
        try:
            content = []
            
            # 1. Get the introduction for the article.
            intro_prompt = (f"Write a 200 word introduction for a blog article titled '{title}'. "
                            "Keep it simple & informative. Use an active voice. Write at the level of a twelfth-grader. "
                            f"Include these keywords: {', '.join(keywords)}. Output as HTML. Do not include quotes in your output. Do not include the title.")
            
            intro_response = openai.ChatCompletion.create(
                model=self.model_4, 
                messages=[
                    {"role": "user", "content": intro_prompt}
                ]
            )
            intro = intro_response['choices'][0]['message']['content']
            content.append(intro)

            # 2. Get the content outline for the blog post based on the title.
            outline_prompt = (f"Create a detailed outline for the blog post titled '{title}' "
                            f"using these keywords: {', '.join(keywords)}. "
                            "Seperate each section. Do not give the title. Do not mention introduction. ")

            outline_response = openai.ChatCompletion.create(
                model=self.model_4, 
                messages=[
                    {"role": "user", "content": outline_prompt}
                ]
            )
            outline = outline_response['choices'][0]['message']['content']
            outline_sections = re.split(r'\n\s*\n', outline)
            
            # 3. For each item in the topic cluster, send a request to fill in the content.
            for section in outline_sections:
                content_prompt = ("Expand upon the outline below, writing 250 words for an article. "
                                "No need for an intro or conclusion. " 
                                "Keep it interesting & informative. Organize the content by the subtopic, including "
                                "headings for each subtopic. Write 2 paragraphs for each subtopic."
                                "Use an active voice. Write at the level of a twelfth-grader. "
                                "Output as HTML. Do not use <h1>. Do not include quotes in your output. "
                                f"This is the outline:\n{section}")
                
                content_response = openai.ChatCompletion.create(
                    model=self.model_4, 
                    messages=[
                        {"role": "user", "content": content_prompt}
                    ]
                )
                content.append(content_response['choices'][0]['message']['content'])

            # 4. Initialize and return an instance of the BlogPost class with the title and the concatenated content.
            full_content = '\n\n'.join(content)

            category = self.get_post_category(title)

            return BlogPost(title=title, content=full_content, category_id=category[1],featured_image_id=CATEGORY_IMAGE_IDS[category[0]], status=status)
        
        except Exception as err:
            logging.error(f"Failed to create blog post: {err}")
            raise