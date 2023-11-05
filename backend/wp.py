import requests
import base64
import logging
from auth import *
import os
from blog_post import BlogPost
from requests_toolbelt.multipart.encoder import MultipartEncoder


CATEGORY_IMAGE_IDS = {
    "Disease Prevention": 545,
    "Fitness & Exercise": 536,
    "Holistic Health": 537,
    "Longevity": 538,
    "Nutrition & Diet": 543,
    "Skincare": 539,
    "Sleep": 540,
    "Wellnesss": 541,
    "Women's Health": 542,
}

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class WordPressApi:
    def __init__(self):
        auth_string = "{}:{}".format(wp_username, wp_password)
        self.encoded_auth_string = base64.b64encode(auth_string.encode("utf-8")).decode(
            "utf-8"
        )
        self.logger = logging.getLogger()

    def upload_image(self, title, image_name) -> int:
        try:
            # This will happen is theres a faliure uploading the image
            if image_name == None:
                return None

            image_path = os.path.join(__location__, "images", image_name)

            # 1. Upload the Image
            media_endpoint = f"{wp_domain}/wp-json/wp/v2/media"
            headers = {
                "Authorization": "Basic " + self.encoded_auth_string,
                "Content-Disposition": f'attachment; filename="{image_name}"',
                "Content-Type": "image/jpeg",
            }

            # Read the binary content of the image
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()

            # Make the request to upload
            response = requests.post(
                media_endpoint,
                headers=headers,
                data=image_data,
            )

            # Check the response
            if response.status_code in [200, 201]:
                media_id = response.json()["id"]
            else:
                self.logger.error(
                    f"Failed to upload image {image_name}. Response: {response.text}"
                )
                return None

            response_update = self.update_image_alt_text(
                media_endpoint, media_id, title
            )

            # Check the response
            if response_update.status_code not in [200, 201]:
                self.logger.error(
                    f"Failed to update image alt text {image_name}. Response: {response.text}"
                )

            return media_id

        except Exception as e:
            self.logger.error(f"Failed to upload image {image_name}. Error: {e}")
            return None

    def create_post(self, blogPost: BlogPost):
        try:
            headers = {"Authorization": "Basic " + self.encoded_auth_string}

            post_args = {
                "title": blogPost.title,
                "content": blogPost.content,
                "status": blogPost.status,
                "categories": blogPost.category_id,
                "featured_media": blogPost.featured_image_id
                if blogPost.featured_image_id is not None
                else -1,
            }

            response = requests.post(
                f"{wp_domain}/wp-json/wp/v2/posts", headers=headers, data=post_args
            )
            return response.json()
        except Exception as err:
            blogPost.save()
            self.logger.critical(f"Failed to upload post {blogPost.title}: {err}")
            raise

    def get_categories(self) -> list[str]:
        endpoint = wp_domain + "/wp-json/wp/v2/categories"

        response = requests.get(endpoint, headers={"Content-Type": "application/json"})
        responseJson = response.json()

        categories = [(item["name"], item["id"]) for item in responseJson]
        cleanedCategories = []

        for category in categories:
            cleaned = (category[0].replace("&amp;", "&"), category[1])
            cleanedCategories.append(cleaned)

        return cleanedCategories

    def update_image_alt_text(self, media_endpoint, media_id, title):
        headers_update = {
            "Authorization": "Basic " + self.encoded_auth_string,
            "Content-Type": "application/json",
        }
        data_update = {"alt_text": title}

        response_update = requests.post(
            f"{media_endpoint}/{media_id}",
            headers=headers_update,
            json=data_update,
        )
        return response_update

    def is_auth(self) -> bool:
        try:
            endpoint = wp_domain + "/wp-json/wp/v2/users?context=edit"
            headers = {"Authorization": "Basic " + self.encoded_auth_string}
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as err:
            self.logger.critical(f"Failed to authorize the WordPress user: {err}")
            raise
