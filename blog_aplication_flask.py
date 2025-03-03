from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Function to save data to a JSON file
def save_data():
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

# Function to load data from a JSON file
def load_data():
    try:
        with open('blog_posts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Initialize blog_posts with data from the JSON file
blog_posts = load_data()

# Home route to display all blog posts
@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)

# Add route to handle adding new blog posts
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']

        blog_posts.append({
            'id': len(blog_posts) + 1,
            'title': title,
            'content': content,
            'author': author
        })
        save_data()  # Save data to JSON file
        return redirect(url_for('index'))

    return render_template('add.html')

# Delete route to handle deleting blog posts
@app.route('/delete/<int:post_id>')
def delete(post_id):
    if 0 <= post_id < len(blog_posts):
        blog_posts.pop(post_id)
        save_data()  # Save data to JSON file
    return redirect(url_for('index'))

# Update route to handle updating blog posts
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    if 0 <= post_id < len(blog_posts):
        post = blog_posts[post_id]
    else:
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')

        blog_posts[post_id] = {
            'id': post['id'],
            'title': title,
            'content': content,
            'author': author
        }
        save_data()
        return redirect(url_for('index'))

    return render_template('update.html', post=post, post_id=post_id)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=3000)