from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import json

app = Flask(__name__)

# Configure logging to write to a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='app.log',  # Logs will be written to app.log
    filemode='a'  # Append mode (add logs to the file without overwriting)
)

# Initialize Flask-Limiter
limiter = Limiter(
    get_remote_address,  # Use the client's IP address as the identifier
    app=app,
    default_limits=["100 per hour"]  # Default rate limit for all routes
)

# Helper functions
def save_data():
    with open('books.json', 'w') as file:
        json.dump(books, file, indent=4)

def load_data():
    try:
        with open('books.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Load books data
books = load_data()

def find_book_by_id(book_id):
    for book in books:
        if book_id == book['id']:
            return book
    return None

def validate_book(book):
    if 'title' not in book or 'author' not in book or 'year' not in book:
        return False
    return True

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f"404 Error: {error}")
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    app.logger.error(f"405 Error: {error}")
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(429)
def ratelimit_handler(e):
    app.logger.warning(f"Rate limit exceeded: {e.description}")
    return jsonify({"error": "Rate limit exceeded", "message": str(e.description)}), 429

# Routes
@app.route('/api/books', methods=['GET', 'POST'])
@limiter.limit("50 per minute")  # Apply rate limit to this route
def handle_books():
    app.logger.info("Handling /api/books route")
    if request.method == 'POST':
        new_book = request.get_json()
        app.logger.info(f"Adding new book: {new_book}")
        if not validate_book(new_book):
            app.logger.error("Invalid book data received")
            return jsonify({"error": "Invalid book"}), 400

        new_id = max((book['id'] for book in books), default=0) + 1
        new_book['id'] = new_id
        books.append(new_book)
        save_data()

        app.logger.info(f"New book added: {new_book}")
        return jsonify(new_book), 201
    else:
        # Handle GET requests with query parameters
        author = request.args.get('author')
        title = request.args.get('title')
        page = int(request.args.get('page', 1))  # Default page is 1
        limit = int(request.args.get('limit', 10))  # Default limit is 10

        filtered_books = books

        # Filter by author
        if author:
            filtered_books = [book for book in filtered_books if author.lower() in book['author'].lower()]
        # Filter by title
        if title:
            filtered_books = [book for book in filtered_books if title.lower() in book['title'].lower()]

        # Pagination logic
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_books = filtered_books[start_index:end_index]

        app.logger.info(f"Returning paginated books: page={page}, limit={limit}")
        # Return paginated results with metadata
        return jsonify({
            "page": page,
            "limit": limit,
            "total_books": len(filtered_books),
            "books": paginated_books
        })

@app.route('/api/books/<int:id>', methods=['PUT'])
@limiter.limit("5 per minute")  # Apply rate limit to this route
def update_book(id):
    app.logger.info(f"Updating book with ID: {id}")
    book = find_book_by_id(id)

    if book is None:
        app.logger.error(f"Book not found: ID={id}")
        return jsonify({"error": "Book not found"}), 404

    new_data = request.get_json()
    book.update(new_data)
    save_data()

    app.logger.info(f"Book updated: {book}")
    return jsonify(book)

@app.route('/api/books/<int:id>', methods=['DELETE'])
@limiter.limit("5 per minute")  # Apply rate limit to this route
def delete_book(id):
    app.logger.info(f"Deleting book with ID: {id}")
    book = find_book_by_id(id)

    if book is None:
        app.logger.error(f"Book not found: ID={id}")
        return jsonify({"error": "Book not found"}), 404

    books.remove(book)
    save_data()

    app.logger.info(f"Book deleted: {book}")
    return jsonify(book)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)