from api import api
from models.user import User, Admin, Caretaker, Vet, Volunteer
from __init__ import db

# READ ALL
def get_users():
    return User.query.all()

# READ ONE
def get_user(user_id):
    return User.query.get_or_404(user_id)

# CREATE
def create_user(data):    
    role_mapping = {
        "admin": Admin,
        "caretaker": Caretaker,
        "vet": Vet,
        "volunteer": Volunteer
    }

    user_role = role_mapping.get(data['role'].lower())

    new_user = user_role(login=['login'], 
                        first_name=data.get('first_name'), 
                        last_name=data.get('last_name'), 
                        email=data.get('email'), 
                        password=data['password'])

    db.session.add(new_user)
    db.session.commit()
    return new_user

# EDIT ALL
def edit_user(user_id, data):
    user = User.query.get_or_404(user_id)

    user.login = data.get('login', user.login)
    user.first_name = data.get('fist_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.verified = data.get('verified', user.verified)

    try:
        db.session.commit()
    except Exception as e:
        print(f"Error commiting to database: {str(e)}")
        raise
    return user

# EDIT LOGIN
def edit_user_login(user_id, new_login):
    user = User.query.get_or_404(user_id)
    user.login = new_login

    db.session.commit()

# EDIT FIRST NAME
def edit_user_first_name(user_id, new_first_name):
    user = User.query.get_or_404(user_id)    
    user.first_name = new_first_name
    db.session.commit()

# EDIT LAST NAME
def edit_user_last_name(user_id, new_last_name):
    user = User.query.get_or_404(user_id)
    user.last_name = new_last_name
    db.session.commit()

# EDIT EMAIL
def edit_user_email(user_id, new_email):    
    user = User.query.get_or_404(user_id)
    user.email = new_email
    db.session.commit()

# EDIT VERIFIED STATUS
def edit_user_verified(user_id, new_verified):
    user = User.query.get_or_404(user_id)
    user.verified = new_verified
    db.session.commit()

# EDIT ROLE
def edit_user_role(user_id, new_role):
    user = User.query.get_or_404(user_id)    
    user.role = new_role.lower()    
    db.session.commit()

# DELETE
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return user

def filter_users(filters):
    query = User.query

    if 'login' in filters and filters['login']:
        query = query.filter(User.login.ilike(f"%{filters['login']}%"))

    if 'first_name' in filters and filters['first_name']:
        query = query.filter(User.first_name.ilike(f"%{filters['first_name']}%"))

    if 'last_name' in filters and filters['last_name']:
        query = query.filter(User.last_name.ilike(f"%{filters['last_name']}%"))

    if 'email' in filters and filters['email']:
        query = query.filter(User.email.ilike(f"%{filters['email']}%"))

    if 'role' in filters and filters['role']:
        query = query.filter(User.role == filters['role'].lower())

    if 'verified' in filters and filters['verified']:
        if filters['verified'] == 'verified':
            query = query.filter(User.verified.is_(True))
        if filters['verified'] == 'unverified':
            query = query.filter(User.verified.is_(False))

    return query.all()

def get_caretakers():
    return User.query.filter_by(role='caretaker').all()
    
