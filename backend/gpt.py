import re
import openai

from auth import *
from blog_post import BlogPost
from prompt_constructor import GPTBlogPrompts
from wp import *

class GPTApi:

    model_4 = "gpt-4"
    model_35 = "gpt-3.5-turbo"

    def __init__(self, categories: list[tuple]):
        self.categories = categories
        openai.api_key = open_api_key
    

    def get_post_category(self, title) -> str:

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


    def create_blog_post(self, topic, keywords: list) -> BlogPost:

        # 1. Get a title based on the topic and list of keywords.
        title_prompt = (f"You want to write a blog post about: {topic}. "
                        "You must come up with a concise and SEO optimized title."
                        "Include the topic in the title. Only return the title and ensure"
                        "that it is 60 characters or less.")
        
        title_response = openai.ChatCompletion.create(
            model=self.model_4, 
            messages=[
                {"role": "user", "content": title_prompt}
            ]
        )
        title = title_response['choices'][0]['message']['content']
        title = title.strip("""\"""")

        # 2. Get the content outline for the blog post based on the title.
        outline_prompt = (f"Create a topic cluster for the blog post titled: {title} "
                          f"using these keywords: {', '.join(keywords)}. "
                          "Separate clusters by empty line. Do not give the title.")

        outline_response = openai.ChatCompletion.create(
            model=self.model_4, 
            messages=[
                {"role": "user", "content": outline_prompt}
            ]
        )
        outline = outline_response['choices'][0]['message']['content']
        outline_sections = re.split(r'\n\s*\n', outline)
        
        # 3. For each item in the topic cluster, send a request to fill in the content.
        content = []
        for section in outline_sections:
            content_prompt = ("Expand upon the topic outline below, writing 250 words for an article."
                              "This is only one section of the article. No need for an intro or conclusion. " 
                              "Keep it interesting & informative. Organize the content by the subtopic, including "
                              "headings for each subtopic. Write 2 paragraphs for each subtopic."
                              "Use an active voice. Write at the level of a twelfth-grader. Try to include "
                              f"these keywords, if they are relevant: {', '.join(keywords)}\n"
                              f"This is the topic outline: {section}")
            
            content_response = openai.ChatCompletion.create(
                model=self.model_4, 
                messages=[
                    {"role": "user", "content": content_prompt}
                ]
            )
            content.append(content_response['choices'][0]['message']['content'])
            content.append("\n")

        # 4. Initialize and return an instance of the BlogPost class with the title and the concatenated content.
        full_content = '\n\n'.join(content)

        category = self.get_post_category(title)

        return BlogPost(title=title, content=full_content, category_id=category[1],featured_image_id=CATEGORY_IMAGE_IDS[category[0]])