import openai

from auth import *
from blog_post import BlogPost
from prompt_constructor import GPTBlogPrompts


class GPTApi:
    model_4 = "gpt-4"
    model_35 = "gpt-3.5-turbo"

    def __init__(self, test: bool, categories: list[str]):
        self.test = test
        self.categories = categories
    

    def get_post_category(self, title) -> str:
        categoriesListString = "[" + ", ".join(self.categories) + "]"
        category_prompt = GPTBlogPrompts.CATEGORIES.value.format(title, categoriesListString)


        role_prompt = GPTBlogPrompts.ROLE.value
        
        categoryResponse = openai.ChatCompletion.create(
        model = self.model_35,
        messages=[
                # The first will set the tone of GPT
                {"role": "system", "content": role_prompt},
                {"role" : "user", "content" : category_prompt},
            ]
        )

        categoryString = categoryResponse["choices"][0]["message"]["content"]

        chosenCategory = next((s for s in self.categories if s in categoryString), None)

        return chosenCategory

    def create_blog_post(self, topic: str, keywords: list[str]) -> BlogPost:
        role_prompt = GPTBlogPrompts.ROLE.value

        keywordsListString = "[" + ", ".join(keywords) + "]"
        blogWritingPrompt = GPTBlogPrompts.BLOG.value.format(topic, keywordsListString)

        openai.api_key = open_api_key

        print(f"Creating a blog post about... {topic} with keywords: {keywordsListString}")

        blogResponse = openai.ChatCompletion.create(
        model = self.model_35 if self.test == True else self.model_4,
        messages=[
                # The first will set the tone of GPT
                {"role": "system", "content": role_prompt},
                {"role" : "user", "content" : blogWritingPrompt},
            ]
        )
        
        blogResponse = blogResponse["choices"][0]["message"]["content"]
    
        print(blogResponse)
        lines = blogResponse.split("\n", 1)
        title = lines[0]
        body = lines[1] if len(lines) > 1 else ""
        # Remove newlines from beginning and end of body
        body = body.strip("\n")

        category = self.get_post_category(title)

        return BlogPost(title=title, content=body, category=category)
