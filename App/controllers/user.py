from App.models import User
from App.database import db
from flask_jwt_extended import create_access_token

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def create_user(username, password, admin=False):
    newuser = User(username=username, password=password, admin=admin)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Convert user.id to string when creating the token
        return create_access_token(identity=str(user.id))
    return None