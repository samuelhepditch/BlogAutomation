from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from blog_post import BlogPost
from logger import LoggerConfig
from wp import WordPressApi
from gpt import GPTApi
import os
import openai
from image_creation import create_image
from logging.config import dictConfig


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

app = Flask(__name__)
dictConfig(LoggerConfig.dictConfig)
cors = CORS(app, resources={r"/write_blog": {"origins": "http://localhost:3000"}})

app.config["CORS_HEADERS"] = "Content-Type"

wpAPI = WordPressApi()
gptAPI = GPTApi(categories=wpAPI.get_categories())


def get_used_keywords():
    with open(os.path.join(__location__, "used_keywords.txt"), "r") as f:
        return set(f.read().splitlines())


def add_keyword_to_file(keyword):
    with open(os.path.join(__location__, "used_keywords.txt"), "a") as f:
        f.write(keyword + "\n")


def create_blog_post(title, keywords, status):
    blogPost = gptAPI.create_blog_post(title, keywords, status)

    image_name = create_image(title)

    image_id = wpAPI.upload_image(title, image_name)

    if image_id is not None:
        blogPost.featured_image_id = image_id

    wpAPI.create_post(blogPost)


@app.route("/write_blog", methods=["POST"])
def write_blog():
    try:
        body = request.get_json()
        title = body["title"]
        keywords = body["keywords"].split(",") if body["keywords"] != "" else []
        status = body["status"]

        used_keywords = get_used_keywords()

        for keyword in keywords:
            keyword = keyword.strip()

            if keyword in used_keywords:
                return jsonify(
                    {
                        "status": "error",
                        "message": f"Keyword '{keyword}' has been used before!",
                    }
                )

            add_keyword_to_file(keyword)

        # Call your main code to create a blog post
        create_blog_post(title, keywords, status)

        return jsonify(
            {"status": "success", "message": "Blog post written successfully!"}
        )

    except openai.error.RateLimitError as e:
        # Log the rate limit error and return an appropriate response
        app.logger.error(f"Rate limit exceeded for post {title}: {str(e)}")
        return jsonify({"status": "error", "message": "Rate limit exceeded"}), 429
    except Exception as e:
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500


if __name__ == "__main__":
    # Make sure WP API is authenticated, or else you'll be making blogs for nothing
    if not wpAPI.is_auth():
        print("!!! WP API NOT AUTHENTICATED !!!")
        exit()

    # Check if the text file exists, if not, create it
    if not os.path.exists(os.path.join(__location__, "used_keywords.txt")):
        with open(os.path.join(__location__, "used_keywords.txt"), "w"):
            pass

    app.run(debug=True)
