from wp import WordPressApi
from gpt import GPTApi

def create_blog_post(title, keywords):

    wpAPI = WordPressApi() 
    availableCategories = wpAPI.get_categories()

    gptAPI = GPTApi(categories=availableCategories)

    blogPost = gptAPI.create_blog_post(title, keywords)

    wpAPI.create_post(blogPost)

create_blog_post("honey tea", "tea")