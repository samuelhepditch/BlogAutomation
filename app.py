from flask import Flask, render_template, request, jsonify
from main import create_blog_post
import os

app = Flask(__name__)

used_keywords = set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write_blog', methods=['POST'])
def write_blog():
    title = request.form.get('topic')
    keywords = request.form.get('keywords').split(',')

    for keyword in keywords:
        keyword = keyword.strip()
        if keyword in used_keywords:
            return jsonify({"status": "error", "message": f"Keyword '{keyword}' has been used before!"})
    
    used_keywords.update(keywords)

    # Call your main code to create a blog post
    create_blog_post(title, keywords)

    return jsonify({"status": "success", "message": "Blog post written successfully!"})

if __name__ == "__main__":
    app.run(debug=True)