from flask import Flask,request,render_template_string



app = Flask(__name__)
# Define the routes
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the input from the form
        user_input = request.form.get('user_input')
        # Print the input to the terminal
        print(f"User entered: {user_input}")
        return f"<h1>You entered: {user_input} </h1>"

    # HTML form for user input
    form_html = """
    <form method="POST">
        <label for="user_input">Enter something:</label><br>
        <input type="text" id="user_input" name="user_input"><br><br>
        <input type="submit" value="Submit">
    </form>
    """
    return form_html
# Dynamic route
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)


# Run the app
if __name__ == '__main__':
    app.run(debug=True,port=3000)