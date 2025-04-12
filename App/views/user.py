from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, send_file, current_app
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

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
    deleteFile,
    createGraph
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
@jwt_required()
def home_page():
    return render_template('index.html', current_user=jwt_current_user)

@user_views.route('/upload', methods=['GET', 'POST'])
@jwt_required()
def upload():
    if request.method == 'POST':
        file = request.files['file']
        userId = get_jwt_identity()
        user = get_user(userId)

        createFile(name=file.filename, data=file.read(), userId=user.id)

        flash('File successfully uploaded')
        return render_template('index.html')
    return render_template('index.html')

@user_views.route('/download/<file_id>', methods=['GET'])
@jwt_required()
def download(file_id):
    file = getFile(file_id)
    flash('File successfully downloaded')
    return send_file(BytesIO(file.fileData), download_name=file.name, as_attachment=True)

@user_views.route('/delete/<file_id>', methods=['POST'])
@jwt_required()
def delete(file_id):
    deleteFile(file_id)
    flash('File successfully deleted')
    return render_template('index.html')

@user_views.route('/generateGraph/<file_id>', methods=['POST'])
@jwt_required()
def generateGraph(file_id):
    userId = get_jwt_identity()
    user = get_user(userId)

    file = getFile(file_id)
    graph = pd.read_csv(BytesIO(file.fileData))
    mplot.figure()
    graph.plot()
    #mplot.show()
    graphName = f"{file.name}Graph.png"
    graphDir = os.path.join(current_app.root_path, 'static', 'graphs', graphName)
    
    os.makedirs(graphDir, exist_ok=True)
    
    graphPath = os.path.join(graphDir, graphName)
    mplot.savefig(graphDir)
    mplot.close()
    createGraph(name=graphName, data=graphPath.read(), userId=user.id)
    flash('Graph created')
    return render_template('index.html')

@user_views.route('/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test_route():
    return f"Method: {request.method}"
