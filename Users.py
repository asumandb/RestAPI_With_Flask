import pyodbc 
from flask import Flask, request, jsonify

connection = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=.;"
    "Database=users;"
    "Trusted_Connection=yes;"
)

cursor = connection.cursor()
print("SQL Bağlantısı Kuruldu.")

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = [
        {
            'userID': row[0],
            'username': row[1],
            'email': row[2],
            'password': row[3]
        }
        for row in cursor
    ]
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.get_json()
    if "username" not in new_user and "email" not in new_user and "password" not in new_user:
        return jsonify({"error": "Eksik bilgiler"}), 400
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (new_user['username'], new_user['email'], new_user['password']))
    connection.commit()
    return jsonify(new_user), 201

@app.route('/users/<int:userID>', methods=['PUT'])
def update_user(userID):
    updated_user = request.get_json()
    if "username" not in updated_user and "email" not in updated_user and "password" not in updated_user:
        return jsonify({"error": "Eksik bilgiler"}), 400
    cursor.execute("UPDATE users SET username = ?, email = ?, password = ? WHERE userID = ?", (updated_user['username'], updated_user['email'], updated_user['password'], userID))
    connection.commit()

@app.route('/users/<int:userID>', methods=['DELETE'])
def delete_user(userID):
    cursor.execute("DELETE FROM users WHERE userID = ?", (userID,))
    connection.commit()
    return jsonify({"message": "Kullanıcı silindi"}), 200

if __name__ == '__main__':
    app.run(debug=True)
