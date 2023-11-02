import requests
import base64
from auth import *
from blog_post import BlogPost


CATEGORY_IMAGE_IDS = {
    'Disease Prevention': 545, 
    'Fitness & Exercise': 536, 
    'Holistic Health': 537, 
    'Longevity': 538, 
    'Nutrition & Diet': 543, 
    'Skincare': 539, 
    'Sleep': 540, 
    'Wellnesss': 541, 
    "Women's Health": 542 
}

class WordPressApi:

    def create_post(self, blogPost: BlogPost):
        
        auth_string = '{}:{}'.format(wp_username, wp_password)
        encoded_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

        headers = {
            'Authorization': 'Basic ' + encoded_auth_string
        }

        post_args = {
            'title': blogPost.title,
            'content': blogPost.content,
            'status': blogPost.status,
            'categories': blogPost.category_id,
            'featured_media': blogPost.featured_image_id
        }

        response = requests.post(f'{wp_domain}/wp-json/wp/v2/posts', headers=headers, data=post_args)
        return response.json()


    def get_categories(self) -> list[str]:

        endpoint = wp_domain + "/wp-json/wp/v2/categories"

        response = requests.get(endpoint, headers={
            'Content-Type': 'application/json'
        })
        responseJson = response.json()

        categories = [(item["name"], item["id"]) for item in responseJson]
        cleanedCategories = []

        for category in categories:
            cleaned = (category[0].replace("&amp;", "&"), category[1])
            cleanedCategories.append(cleaned)

        return cleanedCategories


WordPressApi().get_categories()

