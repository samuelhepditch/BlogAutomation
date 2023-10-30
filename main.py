from wp import WordPressApi
from gpt import GPTApi


if __name__ == "__main__":
    
    topic = "the dangers of sleeping on an air mattress"

    keywords = ["air mattress dangers", "air mattress back problems"]

    wpAPI = WordPressApi() 
    availableCategories = wpAPI.get_categories()

    gptAPI = GPTApi(test=True, categories=availableCategories)

    blogPost = gptAPI.create_blog_post(topic, keywords)

    wpAPI.create_draft_post(blogPost)