import pyodbc
from flask import Flask, request, jsonify

connection = pyodbc.connect(
    
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=.;"
    "Database=siparis;"
    "Trusted_Connection=yes;"
)

cursor = connection.cursor()

app = Flask(__name__)

@app.route('/orders', methods=['GET'])
def get_orders():
    if request.method == 'GET':
        cursor.execute("SELECT * FROM siparisler")
        rows = cursor.fetchall()
        orders = []
        for row in rows:
            orders.append({
                'id': row[0],
                'product_id': row[1],
                'quantity': row[2],
                'total_price': row[3]
            })
        return jsonify(orders)

@app.route('/orders', methods = ['POST'])
def add_order():
    if request.method == 'POST':
        data = request.get_json()
        cursor.execute("INSERT INTO siparisler (product_id, quantity, total_price) VALUES(?, ?,?)", data['product_id'], data['quantity'], data['total_price'])
        connection.commit()
        return jsonify({'message': 'sipariş eklendi.'}), 201
    
@app.route('/orders/<int:id>', methods = ['PUT'])
def update_order(id):
    update_order = request.get_json()
    cursor.execute("UPDATE siparisler SET product_id = ?, quantity = ?, total_price = ? WHERE id = ?", (update_order['product_id'], update_order['quantity'], update_order['total_price'], id))
    connection.commit()
    return jsonify({'message': 'siparis güncellendi.'}), 200

@app.route('/orders/<int:id>', methods = ['DELETE'])
def delete_order(id):
    cursor.execute("DELETE FROM siparisler WHERE id= ? ", (id,))
    connection.commit()
    return jsonify({'message': 'sipariş silindi.'}), 200

if __name__ == '__main__':
    app.run(debug = True)
