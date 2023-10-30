from prompt_constructor import GPTBlogPrompts
import openai
from auth import *
from blog_post import BlogPost

MODEL_PROD = "gpt-4"
MODEL_TEST = "gpt-3.5-turbo"

TEST = True

def create_blog_post(topic: str, keywords: list[str]) -> BlogPost:
    role_prompt = GPTBlogPrompts.ROLE.value

    keywordsListString = "[" + ", ".join(keywords) + "]"

    prompt = GPTBlogPrompts.BLOG.value.format(topic, keywordsListString)

    openai.api_key = open_api_key

    response = openai.ChatCompletion.create(
    model = MODEL_TEST if TEST == True else MODEL_PROD,
    messages=[
            # The first will set the tone of GPT
            {"role": "system", "content": role_prompt},
            {"role" : "user", "content" : prompt}
        ]
    )

    textResponse = response["choices"][0]["message"]["content"]

    lines = textResponse.split("\n", 1)
    title = lines[0]
    body = lines[1] if len(lines) > 1 else ""
    # Remove newlines from beginning and end of body
    body = body.strip("\n")

    return BlogPost(title=title, body=body)
