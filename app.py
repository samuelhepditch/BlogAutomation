from flask import Flask, render_template, request, jsonify
from main import create_blog_post
import os

app = Flask(__name__)

def get_used_keywords():
    with open('used_keywords.txt', 'r') as f:
        return set(f.read().splitlines())

def add_keyword_to_file(keyword):
    with open('used_keywords.txt', 'a') as f:
        f.write(keyword + '\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write_blog', methods=['POST'])
def write_blog():
    topic = request.form.get('topic')
    keywords = request.form.get('keywords').split(',')
    keywords.append(topic)

    used_keywords = get_used_keywords()

    for keyword in keywords:
        keyword = keyword.strip()
        
        if keyword in used_keywords:
            return jsonify({"status": "error", "message": f"Keyword '{keyword}' has been used before!"})

        # Add keyword to the file
        add_keyword_to_file(keyword)

    # Call your main code to create a blog post
    create_blog_post(topic, keywords)

    return jsonify({"status": "success", "message": "Blog post written successfully!"})

if __name__ == "__main__":
    # Check if the text file exists, if not, create it
    if not os.path.exists('used_keywords.txt'):
        with open('used_keywords.txt', 'w'):
            pass

    app.run(debug=True)
