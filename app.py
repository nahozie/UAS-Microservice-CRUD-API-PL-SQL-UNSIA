from sqlalchemy.exc import IntegrityError
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
import jwt
from sqlalchemy import asc
from crypto import decrypt, encrypt
from sqlalchemy import event 
import datetime




SECRET_KEY = b'secretkey1234567' 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/db_employee'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db) 



class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    gender = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(15), nullable=False)



def generate_token(user_id):
    return jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')

        user = Employee.query.filter_by(username=username).first()
    
        if user:
            decrypt_pass = decrypt(user.password)
            if decrypt_pass == password:
                # Generate a JWT token
                token = generate_token(user.id)
                return jsonify({'status': 'Success', "id": user.id, 'message': 'Login successful', 'token': token}), 200
            else:
                 return jsonify({'status': 'Error', 'message': 'Invalid password'}), 401
        else:
            return jsonify({'status': 'Error', 'message': 'Invalid username'}), 401

    except SQLAlchemyError as e:
        # Log the detailed error for debugging purposes
        print(f"Error: {str(e)}")
        return jsonify({'status': 'Error', 'message': 'Login failed'}), 500

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        new_user = Employee(
            username=data['username'],
            password=encrypt(data['password']),
            first_name=data['first_name'],
            last_name=data['last_name'],
            gender=data['gender'],
            status=data['status']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'status': 'Success', 'message': 'Success created'}), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': 'Error', 'message': 'Username already exists'}), 400

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'status': 'Error', 'message': 'Authorization token is missing'}), 401

        # Decode and verify the token
        payload = decode_token(token)
        if not payload:
            return jsonify({'status': 'Error', 'message': 'Invalid or expired token'}), 401
        
        
        users = Employee.query.order_by(asc(Employee.id)).all()
        user_list = []

        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.gender,
                'status': user.status
            }
            user_list.append(user_data)

        return jsonify({'status': 'Success', 'data': user_list}), 200

    except SQLAlchemyError as e:
        # Log the detailed error for debugging purposes
        print(f"Error: {str(e)}")
        return jsonify({'status': 'Error', 'message': 'Failed to retrieve users'}), 500

@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'status': 'Error', 'message': 'Authorization token is missing'}), 401

        # Decode and verify the token
        payload = decode_token(token)
        if not payload:
            return jsonify({'status': 'Error', 'message': 'Invalid or expired token'}), 401
        
        
        user = Employee.query.get(user_id)

        if user:
            user_data = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.gender,
                'status': user.status
            }
            return jsonify({'status': 'Success', 'data': user_data}), 200
        else:
            return jsonify({'status': 'Error', 'message': 'User not found'}), 404

    except SQLAlchemyError as e:
        # Log the detailed error for debugging purposes
        print(f"Error: {str(e)}")
        return jsonify({'status': 'Error', 'message': 'Failed to retrieve user'}), 500

@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'status': 'Error', 'message': 'Authorization token is missing'}), 401

        # Decode and verify the token
        payload = decode_token(token)
        if not payload:
            return jsonify({'status': 'Error', 'message': 'Invalid or expired token'}), 401

        # Ensure the authenticated user is the same as the one being updated
        if payload['user_id'] != user_id:
            return jsonify({'status': 'Error', 'message': 'Unauthorized to update this user'}), 403

        # Proceed with updating the user (modify as needed)
        user = Employee.query.get(user_id)
        if user:
            data = request.get_json()
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.gender = data.get('gender', user.gender)
            user.status = data.get('status', user.status)
        
            db.session.commit()
            return jsonify({'status': 'Success', 'message': 'User updated successfully'}), 200
        else:
            return jsonify({'status': 'Error', 'message': f'User with ID {user_id} not found'}), 404


    except SQLAlchemyError as e:
        # Log the detailed error for debugging purposes
        print(f"Error: {str(e)}")
        db.session.rollback()
        return jsonify({'status': 'Error', 'message': 'Failed to update user'}), 500

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'status': 'Error', 'message': 'Authorization token is missing'}), 401

        # Decode and verify the token
        payload = decode_token(token)
        if not payload:
            return jsonify({'status': 'Error', 'message': 'Invalid or expired token'}), 401

        # Ensure the authenticated user is the same as the one being deleted
        if payload['user_id'] != user_id:
            return jsonify({'status': 'Error', 'message': 'Unauthorized to delete this user'}), 403

        # Proceed with deleting the user (modify as needed)
        user = Employee.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'status': 'Success', 'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'status': 'Error', 'message': f'User with ID {user_id} not found'}), 404

    except SQLAlchemyError as e:
        # Log the detailed error for debugging purposes
        print(f"Error: {str(e)}")
        db.session.rollback()
        return jsonify({'status': 'Error', 'message': 'Failed to delete user'}), 500
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

# trigger manajemen log

class UserActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    activity_type = db.Column(db.String(15))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
@event.listens_for(Employee, 'after_insert')
def after_employee_insert(mapper, connection, target):
    try:
        log_entry = UserActivityLog(user_id=target.id, activity_type='INSERT')
        connection.execute(UserActivityLog.__table__.insert(), log_entry)
    except Exception as e:
        print(f"Error during after_insert: {str(e)}")

@event.listens_for(Employee, 'after_update')
def after_employee_update(mapper, connection, target):
    try:
        log_entry = UserActivityLog(user_id=target.id, activity_type='UPDATE')
        connection.execute(UserActivityLog.__table__.insert(), log_entry)
    except Exception as e:
        print(f"Error during after_update: {str(e)}")

@event.listens_for(Employee, 'after_delete')
def after_employee_delete(mapper, connection, target):
    try:
        log_entry = UserActivityLog(user_id=target.id, activity_type='DELETE')
        connection.execute(UserActivityLog.__table__.insert(), log_entry)
    except Exception as e:
        print(f"Error during after_delete: {str(e)}")