from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, send_file, current_app
from flask_jwt_extended import jwt_required, current_user as jwt_current_user, set_access_cookies,create_access_token,unset_jwt_cookies  # Add this import at the top

from.index import index_views

from App.controllers import (
    create_user,
    get_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_jwt_identity,
    createFile,
    getFile,
    getAllFiles,
    deleteFile,
    getData,
    createData,
    getFilebyName,
    createGraphData,
    login_user,
    getHeaders
)


from App.database import db

from io import BytesIO
import pandas as pd
import matplotlib.pyplot as mplot

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
    return send_from_directory('static', 'static-user.html')


ALLOWED_EXTENSIONS = {'csv'}

import os
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_views.route('/', methods=['GET'])
def home_page():
    files = getAllFiles()
    return render_template('index.html', files=files)

@user_views.route('/upload', methods=['GET', 'POST'])
@jwt_required()
def upload():
    userId = get_jwt_identity()
    user = get_user(userId)
    if not user.admin:
        flash('Admins only can upload files.')
        return redirect(url_for('user_views.home_page'))
    
    if request.method == 'POST':
        file = request.files['file']

        createFile(name=file.filename, data=file.read(), userId=user.id)
        save_file = getFilebyName(file.filename)
        createData(file_id=save_file.id)
        flash('File successfully uploaded')
        return redirect(url_for('user_views.home_page'))
    return render_template('index.html')

@user_views.route('/download/<file_id>', methods=['GET'])
@jwt_required()
def download(file_id):    
    userId = get_jwt_identity()
    user = get_user(userId)
    if not user.admin:
        flash('Admins only can delete files.')
        return redirect(url_for('user_views.home_page'))
    
    file = getFile(file_id)
    flash('File successfully downloaded')
    return send_file(BytesIO(file.fileData), download_name=file.name, as_attachment=True)

@user_views.route('/delete/<file_id>', methods=['GET','POST'])
@jwt_required()
def delete(file_id):
    userId = get_jwt_identity()
    user = get_user(userId)
    if not user.admin:
        flash('Admins only can delete files.')
        return redirect(url_for('user_views.home_page'))
    
    deleteFile(file_id)
    flash('File successfully deleted')
    return render_template('index.html')

@user_views.route('/generateGraph/<data_type>/<file_id>', methods=['GET', 'POST'])
def generateGraph(file_id, data_type):
    headers = getHeaders(file_id)
    
    if request.method == 'GET':
        files = getAllFiles()
        return render_template('index.html', file_id=file_id, headers=headers, files=files)
    if data_type:
        chart_data = createGraphData(file_id, f'{data_type}')
        return jsonify(chart_data)
    else:
        return jsonify({'error': 'Invalid data type'}), 400



@user_views.route('/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test_route():
    return f"Method: {request.method}"

@user_views.route('/login', methods=['GET'])
def show_login_page():
    return render_template('login.html')

@user_views.route('/login', methods=['POST'])
def login_page():
    data = request.form
    token = login_user(data['username'], data['password'])
    response = None
    
    if token:
        flash('Logged in successfully.')
        response = redirect(url_for('user_views.admin_view'))
        set_access_cookies(response, token)
    else:
        flash('Invalid username or password')
        response = redirect(url_for('user_views.show_login_page'))
    return response

@user_views.route('/admin',methods=['GET'])
@jwt_required()
def admin_view():
    userId = get_jwt_identity()  # This will now be a string
    user = get_user(int(userId))  # Convert back to integer for database query
    files = getAllFiles()
    return render_template('admin/index.html', current_user=user, files=files)

@user_views.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = redirect(url_for('user_views.home_page'))
    unset_jwt_cookies(response)
    flash('Successfully logged out')
    return response