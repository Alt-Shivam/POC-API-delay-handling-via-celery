from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import time
import os

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@db/{os.environ['POSTGRES_DB']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

# CRUD Endpoints with 10-second delay

@app.route('/api/employees', methods=['GET'])
def get_employees():
    # Wait for 10 seconds before processing
    time.sleep(10)
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees])


@app.route('/api/employee', methods=['POST'])
def add_employee():
    # Wait for 10 seconds before processing
    time.sleep(10)
    data = request.get_json()
    new_employee = Employee(name=data['name'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify(new_employee.to_dict()), 201


@app.route('/api/employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    # Wait for 10 seconds before processing
    time.sleep(10)
    employee = Employee.query.get(id)
    if employee is None:
        return jsonify({"error": "Employee not found"}), 404
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5083)
