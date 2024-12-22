import pyodbc 
from flask import Flask, request, jsonify

connection = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=.;"
    "Database=Library;"
    "Trusted_Connection=yes;"
)

cursor = connection.cursor()
print("SQL Bağlantısı Kuruldu.")

app = Flask(__name__)

@app.route('/library', methods=['GET'])
def get_books():
    cursor.execute("SELECT * FROM Books")
    books = [
        {
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'year': row[3],
            'stock': row[4]
        }
        for row in cursor
    ]
    return jsonify(books)

@app.route('/library', methods=['POST'])
def add_book():
    new_book = request.get_json()
    cursor.execute("INSERT INTO Books (Title, Author, Year, Stock) VALUES (?, ?, ?, ?)", new_book['Title'], new_book['Author'], new_book['Year'], new_book['Stock'])
    connection.commit()
    return jsonify({'message': 'Kitap eklendi.'}), 201

@app.route('/library/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_book = request.get_json()
    cursor.execute("UPDATE Books SET Title = ?, Author = ?, Year = ?, Stock = ? WHERE ID = ?", updated_book['Title'], updated_book['Author'], updated_book['Year'], updated_book['Stock'], book_id)
    connection.commit()
    return jsonify({'message': 'Kitap güncellendi.'}), 200

@app.route('/library/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    cursor.execute("DELETE FROM Books WHERE ID = ?", book_id)
    connection.commit()
    return jsonify({'message': 'Kitap silindi.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
