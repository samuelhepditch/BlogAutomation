from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from wp import WordPressApi
from gpt import GPTApi
import os



app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

wpAPI = WordPressApi() 
gptAPI = GPTApi(categories=wpAPI.get_categories())

def get_used_keywords():
    with open('used_keywords.txt', 'r') as f:
        return set(f.read().splitlines())

def add_keyword_to_file(keyword):
    with open('used_keywords.txt', 'a') as f:
        f.write(keyword + '\n')

def create_blog_post(title, keywords, status):
    blogPost = gptAPI.create_blog_post(title, keywords, status)

    wpAPI.create_post(blogPost)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write_blog', methods=['POST'])
@cross_origin(origin='*')
def write_blog():
    try:
        body = request.get_json()
        title = body['title']
        keywords = body['keywords'].split(',')
        keywords.append(title)
        status = body['status']

        used_keywords = get_used_keywords()

        for keyword in keywords:
            keyword = keyword.strip()

            # Add keyword to the file only if blog is created successfully
            add_keyword_to_file(keyword)
            
            if keyword in used_keywords:
                return jsonify({"status": "error", "message": f"Keyword '{keyword}' has been used before!"})
        
        # Call your main code to create a blog post
        create_blog_post(title, keywords, status)

        return jsonify({"status": "success", "message": "Blog post written successfully!"})
    
    except Exception as error:
        return jsonify({"status": "error", 'message': error})
    
if __name__ == "__main__":
    # Make sure WP API is authenticated, or else you'll be making blogs for nothing
    if not wpAPI.is_auth():
        print("!!! WP API NOT AUTHENTICATED !!!")
        exit()

    # Check if the text file exists, if not, create it
    if not os.path.exists('used_keywords.txt'):
        with open('used_keywords.txt', 'w'):
            pass

    app.run(debug=True)
