import pyodbc 
from flask import Flask, request, jsonify

connection = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=.;"
    "Database=members;"
    "Trusted_Connection=yes;"
)

cursor = connection.cursor()

app = Flask(__name__)

@app.route('/members', methods=['GET'])
def get_members():
    if request.method == 'GET':
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()
        members = []
        for row in rows:
            members.append({
                'memberID': row[0],
                'name': row[1],
                'phone': row[2],
                'email': row[3]
            })
        return jsonify(members)

@app.route('/members', methods=['POST'])
def add_member():
    if request.method == 'POST':
        data = request.get_json()
        cursor.execute("INSERT INTO members (name, phone, email) VALUES (?, ?, ?)", data['name'], data['phone'], data['email'])
        connection.commit()
        return jsonify({'message': 'Member added successfully.'}), 201
    
@app.route('/members/<int:memberID>', methods=['PUT'])
def update_member(memberID):
    if request.method == 'PUT':
        updated_member = request.get_json()
        cursor.execute("UPDATE members SET name = ?, phone = ?, email = ? WHERE memberID = ?", updated_member['name'], updated_member['phone'], updated_member['email'], memberID)
        connection.commit()
        return jsonify({'message': 'Member updated successfully.'}), 200
    

@app.route('/members/<int:memberID>', methods=['DELETE'])
def delete_member(memberID):
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM members WHERE memberID = ?", memberID)
        connection.commit()
        return jsonify({'message': 'Member deleted successfully.'}), 200
