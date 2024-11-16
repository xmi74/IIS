from flask import jsonify, request
from api import api
from models.user import User, Admin, Caretaker, Vet, Volunteer
from __init__ import db

# READ ALL
@api.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [
        {
            "id": user.id,
            "login": user.login,
            "first_name": user.first_name,            
            "last_name": user.last_name,
            "role": user.role,
            "verified": user.verified,
        } for user in users
    ]
    return jsonify(result)

# READ ONE (GET)
@api.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    result = [
        {
            "id": user.id,
            "login": user.login,
            "first_name": user.first_name,            
            "last_name": user.last_name,
            "role": user.role,
            "verified": user.verified,
        }
    ]
    return jsonify(result)

# CREATE
@api.route('/api/users', methods='POST')
def create_user():
    data = request.get_json()

    role_mapping = {
        "admin": Admin,
        "caretaker": Caretaker,
        "vet": Vet,
        "volunteer": Volunteer
    }

    user_role = role_mapping.get(data['role'].lower())

    new_user = user_role(login=['login'], first_name=data.get('first_name'), last_name=data.get('last_name'), email=data.get('email'), password=data['password'], verified=data.get('verified', False))

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created", "id": new_user.id})

# EDIT
@api.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.verified = data.get('verified', user.verified)

    db.session.commit()
    return jsonify({"message": "User edited", "id": user.id})

# DELETE
@api.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)