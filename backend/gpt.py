import re
import openai
from auth import *
from image_creation import create_image
from blog_post import BlogPost
from prompt_constructor import GPTBlogPrompts
from wp import *
import logging


class GPTApi:
    model_4 = "gpt-4"
    model_35 = "gpt-3.5-turbo"

    def __init__(self, categories: list[tuple]):
        self.categories = categories
        openai.api_key = open_api_key
        self.logger = logging.getLogger()

    def get_post_category(self, title) -> str:
        categoriesListString = str([t[0] for t in self.categories])
        category_prompt = GPTBlogPrompts.CATEGORIES.value.format(
            title, categoriesListString
        )
        role_prompt = GPTBlogPrompts.ROLE.value

        categoryResponse = openai.ChatCompletion.create(
            model=self.model_4,
            messages=[
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": category_prompt},
            ],
        )

        categoryString = categoryResponse["choices"][0]["message"]["content"]
        chosenCategory = next(
            (t for t in self.categories if t[0] in categoryString), None
        )

        return chosenCategory

    def create_blog_post(self, title, keywords: list, status) -> BlogPost:
        content = []

        # 1. Get the introduction for the article. No try except because intro is mandatory
        try:
            intro_prompt = (
                f"Write a 100 word introduction for a blog article titled '{title}'. "
                "Keep it simple & informative. Use an active voice. Write at the level of a twelfth-grader. "
                f"Include these keywords: {', '.join(keywords)}. Output as HTML. Do not include quotes in your output. Do not include the title."
            )

            intro_response = openai.ChatCompletion.create(
                model=self.model_4, messages=[{"role": "user", "content": intro_prompt}]
            )
            intro = intro_response["choices"][0]["message"]["content"]
            content.append(intro)
        except openai.error.RateLimitError as e:
            raise e
        except Exception as e:
            self.logger.critical(
                f"Failed to create intro for {title}\n" f"The error was: {e}"
            )
            # Cannot continue without intro
            raise e

        # 2. Get the content outline for the blog post based on the title. No try except because outline is mandatory
        try:
            outline_prompt = (
                f"Create a detailed outline for the blog post titled '{title}' "
                f"using these keywords: {', '.join(keywords)}. "
                "Seperate each section. Do not give the title. Do not mention introduction. "
            )

            outline_response = openai.ChatCompletion.create(
                model=self.model_4,
                messages=[{"role": "user", "content": outline_prompt}],
            )
            outline = outline_response["choices"][0]["message"]["content"]
            outline_sections = re.split(r"\n\s*\n", outline)
        except openai.error.RateLimitError as e:
            raise e
        except Exception as e:
            self.logger.critical(
                f"Failed to create outline for {title}\n" f"The error was: {e}"
            )
            # Cannot continue without outline
            raise e

        # 3. For each item in the topic cluster, send a request to fill in the content.
        for section in outline_sections:
            content_prompt = (
                "Expand upon the outline below, writing 250 words for an article. "
                "No need for an intro or conclusion. "
                "Keep it interesting & informative. Organize the content by the subtopic, including "
                "headings for each subtopic. Write 2 paragraphs for each subtopic."
                "Use an active voice. Write at the level of a twelfth-grader. "
                "Output as HTML. Do not use <h1>. Do not include quotes in your output. "
                f"This is the outline:\n{section}"
            )
            # If one fails, still try to continue with the post. It might be salveagable.
            # We don't want a situaton where 9/10 sections are successful and the last one makes us lose the post
            try:
                content_response = openai.ChatCompletion.create(
                    model=self.model_4,
                    messages=[{"role": "user", "content": content_prompt}],
                )
                content.append(content_response["choices"][0]["message"]["content"])
            except Exception as e:
                self.logger.error(
                    f"Failed to create content for {title}\n"
                    f"The outline was: {section}\n"
                    f"The error was: {e}"
                )
                # Continue without this section
                continue

        # 4. Initialize and return an instance of the BlogPost class with the title and the concatenated content.
        full_content = "\n\n".join(content)

        blogPost = BlogPost(
            title=title,
            content=full_content,
            status=status,
        )

        # Try, and if failure, no problem. We will do it manually. We don't want to throw out the whole post because of a micategorization.
        try:
            category = self.get_post_category(title)
            blogPost.category = category[1]
        except Exception as e:
            self.logger.error(
                f"Failed to get post category for {title}\n" f"The error was: {e}"
            )

        return blogPost
