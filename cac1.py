from flask import Flask, request, jsonify
import json

app = Flask(__name__)

data_file = 'bookstore_data.json'

def load_data():
    with open(data_file, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Bookstore API!"})

# ---------------- BOOKS ----------------
@app.route('/books', methods=['GET'])
def get_books():
    data = load_data()
    return jsonify(data['books'])

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    data = load_data()
    book = next((b for b in data['books'] if b['id'] == book_id), None)
    return jsonify(book) if book else (jsonify({"error": "Book not found"}), 404)

@app.route('/books', methods=['POST'])
def add_book():
    data = load_data()
    new_book = request.json
    new_book['id'] = len(data['books']) + 1
    data['books'].append(new_book)
    save_data(data)
    return jsonify(new_book), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = load_data()
    book = next((b for b in data['books'] if b['id'] == book_id), None)
    if book:
        book.update(request.json)
        save_data(data)
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    data = load_data()
    books = [b for b in data['books'] if b['id'] != book_id]
    if len(books) == len(data['books']):
        return jsonify({"error": "Book not found"}), 404
    data['books'] = books
    save_data(data)
    return jsonify({"message": "Book deleted"})

@app.route('/books/genre/<string:genre>', methods=['GET'])
def get_books_by_genre(genre):
    data = load_data()
    books = [b for b in data['books'] if genre.lower() in b['genre'].lower()]
    return jsonify(books)

@app.route('/books/recent', methods=['GET'])
def get_recent_books():
    data = load_data()
    books = sorted(data['books'], key=lambda x: x['published_year'], reverse=True)[:5]
    return jsonify(books)

@app.route('/books/stock/<int:threshold>', methods=['GET'])
def get_books_below_stock(threshold):
    data = load_data()
    books = [b for b in data['books'] if b['stock'] < threshold]
    return jsonify(books)

@app.route('/books/max-price', methods=['GET'])
def get_most_expensive_book():
    data = load_data()
    book = max(data['books'], key=lambda x: x['price'], default=None)
    return jsonify(book) if book else jsonify({"error": "No books found"})

@app.route('/books/min-price', methods=['GET'])
def get_cheapest_book():
    data = load_data()
    book = min(data['books'], key=lambda x: x['price'], default=None)
    return jsonify(book) if book else jsonify({"error": "No books found"})

@app.route('/books/available', methods=['GET'])
def get_available_books():
    data = load_data()
    books = [b for b in data['books'] if b['stock'] > 0]
    return jsonify(books)

# ---------------- AUTHORS ----------------
@app.route('/authors/sort', methods=['GET'])
def get_authors_sorted():
    data = load_data()
    authors = sorted(data['authors'], key=lambda x: x['name'])
    return jsonify(authors)

@app.route('/authors/count', methods=['GET'])
def get_total_authors():
    data = load_data()
    return jsonify({"total_authors": len(data['authors'])})

@app.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    data = load_data()
    author = next((a for a in data['authors'] if a['id'] == author_id), None)
    return jsonify(author) if author else (jsonify({"error": "Author not found"}), 404)

@app.route('/authors/<int:author_id>/books', methods=['GET'])
def get_books_by_author(author_id):
    data = load_data()
    books = [b for b in data['books'] if b['author_id'] == author_id]
    return jsonify(books)

# ---------------- CUSTOMERS ----------------
@app.route('/customers/sort', methods=['GET'])
def get_customers_sorted():
    data = load_data()
    customers = sorted(data['customers'], key=lambda x: x['name'])
    return jsonify(customers)

@app.route('/customers/count', methods=['GET'])
def get_total_customers():
    data = load_data()
    return jsonify({"total_customers": len(data['customers'])})

@app.route('/customers/check', methods=['GET'])
def check_customer_exists():
    email = request.args.get('email')
    data = load_data()
    exists = any(c for c in data['customers'] if c['email'] == email)
    return jsonify({"exists": exists})

# ---------------- ORDERS ----------------
@app.route('/orders/revenue', methods=['GET'])
def get_total_revenue():
    data = load_data()
    revenue = sum(b['price'] * o['quantity'] for o in data['orders'] for b in data['books'] if b['id'] == o['book_id'])
    return jsonify({"total_revenue": revenue})

@app.route('/orders/books-sold', methods=['GET'])
def get_total_books_sold():
    data = load_data()
    total_books_sold = sum(o['quantity'] for o in data['orders'])
    return jsonify({"total_books_sold": total_books_sold})

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    data = load_data()
    order = next((o for o in data['orders'] if o['id'] == order_id), None)
    return jsonify(order) if order else (jsonify({"error": "Order not found"}), 404)

@app.route('/orders/average-price', methods=['GET'])
def get_average_order_price():
    data = load_data()
    total_price = sum(b['price'] * o['quantity'] for o in data['orders'] for b in data['books'] if b['id'] == o['book_id'])
    total_orders = len(data['orders'])
    return jsonify({"average_order_price": total_price / total_orders if total_orders > 0 else 0})

# ---------------- DISCOUNT ----------------
@app.route('/books/discount/<int:discount>', methods=['GET'])
def get_discounted_books(discount):
    data = load_data()
    discounted_books = [{**b, "discounted_price": b['price'] * (1 - discount / 100)} for b in data['books']]
    return jsonify(discounted_books)

# ---------------- POPULAR BOOKS ----------------
@app.route('/books/popular', methods=['GET'])
def get_popular_books():
    data = load_data()
    books = sorted(data['books'], key=lambda x: x['sold_copies'], reverse=True)[:5]
    return jsonify(books)

# ---------------- CUSTOMER ORDERS ----------------
@app.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    data = load_data()
    orders = [o for o in data['orders'] if o['customer_id'] == customer_id]
    return jsonify(orders)

# ---------------- AVERAGE BOOK PRICE ----------------
@app.route('/books/average-price', methods=['GET'])
def get_average_book_price():
    data = load_data()
    total_price = sum(b['price'] for b in data['books'])
    total_books = len(data['books'])
    return jsonify({"average_price": total_price / total_books if total_books > 0 else 0})

# ---------------- BOOK SEARCH ----------------
@app.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get('query', '').lower()
    data = load_data()
    books = [b for b in data['books'] if query in b['title'].lower() or query in b['author'].lower()]
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)
