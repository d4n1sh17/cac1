# cac1
# Bookstore Management System

## Overview
This is a RESTful API built using Flask for managing a bookstore. It allows users to manage books, authors, customers, and orders while providing various functionalities such as book searching, sorting, revenue calculation, and discount applications.

## Features
- CRUD operations for books, authors, customers, and orders
- Search books by title or author
- Filter books by genre, availability, and stock level
- Retrieve popular books, recent books, and books with discounts
- Calculate total revenue and average order price
- Check customer existence and sort customers/authors

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/bookstore-management.git
   cd bookstore-management
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python app.py
   ```

## API Endpoints

### Books
- `GET /books` - Retrieve all books
- `GET /books/<book_id>` - Get a specific book by ID
- `POST /books` - Add a new book
- `PUT /books/<book_id>` - Update an existing book
- `DELETE /books/<book_id>` - Delete a book
- `GET /books/genre/<genre>` - Get books by genre
- `GET /books/recent` - Get 5 most recently published books
- `GET /books/stock/<threshold>` - Get books below a stock threshold
- `GET /books/max-price` - Get the most expensive book
- `GET /books/min-price` - Get the cheapest book
- `GET /books/available` - Get available books in stock
- `GET /books/discount/<discount>` - Get books with discounted prices
- `GET /books/popular` - Get 5 most sold books
- `GET /books/search?query=<text>` - Search books by title or author

### Authors
- `GET /authors/sort` - Get authors sorted by name
- `GET /authors/count` - Get total number of authors
- `GET /authors/<author_id>` - Get details of a specific author
- `GET /authors/<author_id>/books` - Get books by a specific author

### Customers
- `GET /customers/sort` - Get customers sorted by name
- `GET /customers/count` - Get total number of customers
- `GET /customers/check?email=<email>` - Check if a customer exists by email

### Orders
- `GET /orders/revenue` - Get total revenue from all orders
- `GET /orders/books-sold` - Get the total number of books sold
- `GET /orders/<order_id>` - Get details of a specific order
- `GET /orders/average-price` - Get the average order price

### Customer Orders
- `GET /customers/<customer_id>/orders` - Get all orders for a specific customer

## Sample `bookstore_data.json` Format
```json
{
  "books": [
    {
      "id": 1,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "genre": "Classic",
      "published_year": 1925,
      "price": 10.99,
      "stock": 50,
      "sold_copies": 500
    }
  ],
  "authors": [
    {
      "id": 1,
      "name": "F. Scott Fitzgerald"
    }
  ],
  "customers": [
    {
      "id": 1,
      "name": "danish khan",
      "email": "danish.khan@example.com"
    }
  ],
  "orders": [
    {
      "id": 1,
      "customer_id": 1,
      "book_id": 1,
      "quantity": 2
    }
  ]
}
```



## Author
[Danish khan]

