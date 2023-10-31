import requests

from auth import *
from blog_post import BlogPost


class WordPressApi:
    def __init__(self):
        self.accessKey = self.get_access_key(wp_auth_args)

    def get_access_key(self, auth_args):
        # Step 2: Get Access Key
        response = requests.post('https://public-api.wordpress.com/oauth2/token', data=auth_args)
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
    

    def create_post(self, blogPost: BlogPost):
        headers = {
            'Authorization': f'Bearer {self.accessKey}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        post_args = {
            'title': blogPost.title,
            'content': blogPost.content,
            'status': blogPost.status,
            'categories': blogPost.category
        }

        print(f"Publishing the blog post...")
        response = requests.post(f'https://public-api.wordpress.com/rest/v1/sites/{wp_site_id}/posts/new/', headers=headers, data=post_args)
        return response.json()


    def get_categories(self) -> list[str]:

        endpoint = wp_domain + "/wp-json/wp/v2/categories"

        response = requests.get(endpoint, headers={
            'Content-Type': 'application/json'
        })

        responseJson = response.json()

        categories = [item["name"] for item in responseJson]

        return categories








