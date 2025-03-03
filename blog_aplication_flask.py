from flask import Flask, render_template

app = Flask(__name__)

blog_posts = [
    {
        'id':1,
        'title': 'First Post',
        'content': 'This is my first post. It is very short.',
        'author': 'John Doe'
    },
    {
        'id':2,
        'title': 'Second Post',
        'content': 'This is my second post. It is a bit longer.',
        'author': 'Jane Smith'
    },
    {
        'id':3,
        'title': 'Third Post',
        'content': 'This is my third post. It is the longest.',
        'author': 'John Doe'
    }
]

@app.route('/')
def index():

    return render_template('index.html',posts=blog_posts)














if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=3000)