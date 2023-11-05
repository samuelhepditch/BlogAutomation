import requests
import base64
import logging
from auth import *
from blog_post import BlogPost
from flask import jsonify, abort


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

    def __init__(self):
        auth_string = '{}:{}'.format(wp_username, wp_password)
        self.encoded_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    def create_post(self, blogPost: BlogPost):
        try:
            headers = {
                'Authorization': 'Basic ' + self.encoded_auth_string
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
        except Exception as err:
            logging.error(f"Failed to upload post as {blogPost.status}: {err}")
            raise


    def get_categories(self) -> list[str]:
        try:
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
        except Exception as err:
            logging.error(f"Failed to get WordPress categories: {err}")
            raise

    def is_auth(self) -> bool:
        try:
            endpoint = wp_domain + "/wp-json/wp/v2/users?context=edit"
            headers = {
                'Authorization': 'Basic ' + self.encoded_auth_string
            }
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as err:
            logging.error(f"Failed to authorize the WordPress user: {err}")
            raise
