from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
import time
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@db/{os.environ['POSTGRES_DB']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

# Define the Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

# Celery task for adding an employee with delay
@celery.task
def add_employee_to_db(name):
    with app.app_context():  # Push the application context for the task
        time.sleep(10)  # Simulate a 10-second delay
        new_employee = Employee(name=name)
        db.session.add(new_employee)
        db.session.commit()
        return {"id": new_employee.id, "name": new_employee.name}

# API to add a new employee (immediate response)
@app.route('/api/employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    # Queue the task for adding employee
    task = add_employee_to_db.delay(data['name'])
    return jsonify({"status": "processing", "task_id": task.id}), 202

# API to retrieve all employees
@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees])

# API to delete an employee
@app.route('/api/employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    if employee is None:
        return jsonify({"error": "Employee not found"}), 404
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
