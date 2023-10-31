from wp import WordPressApi
from gpt import GPTApi


def create_blog_post(title, keywords):

    wpAPI = WordPressApi() 
    availableCategories = wpAPI.get_categories()

    gptAPI = GPTApi(test=False, categories=availableCategories)

    blogPost = gptAPI.create_blog_post(title, keywords)

    wpAPI.create_draft_post(blogPost)