import requests
import json
from auth import *
from requests.auth import HTTPBasicAuth
from blog_post import BlogPost



def upload_post_draft(blogPost: BlogPost):
    # Endpoint for creating posts
    # endpoint = f"{wp_domain}/wp-json/wp/v2/posts"


    # auth = HTTPBasicAuth(wp_username, wp_password)

    # headers = {
    # "Accept": "application/json",
    # "Content-Type": "application/json"
    # }

    # payload = json.dumps({ 
    #     "status":"draft",
    #     "title": blogPost.title,
    #     "content": blogPost.body,
    # })

    # response = requests.request(
    #     "POST",
    #     endpoint,
    #     data=payload,
    #     headers=headers,
    #     auth=auth
    # )

    import requests

    url = 'https://public-api.wordpress.com/rest/v1.1/sites/wellness-wonders.ca/posts/new/'

    headers = {
        'authorization': wp_key
    }

    data = {
        'title': 'Hello World',
        'content': 'Hello. I am a test post. I was created by the API',
        'tags': 'tests',
        'categories': 'API',
        'status': 'draft',
    }

    response = requests.post(url, headers=headers, data=data)

    print(response.text)




testBlogPost = BlogPost("Test Title 2", "Test Body 2")

upload_post_draft(blogPost=testBlogPost)
