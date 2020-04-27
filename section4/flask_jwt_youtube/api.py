from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/fahri/Documents/flask_tut/section4/flask_jwt_youtube/todo.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.String(50))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)


@app.route('/user', methods=['GET'])
def get_all_user():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'Sorry, no user found with this user id.'})
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    return jsonify({'user': user_data})


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()),
                    name=data['name'],
                    password=hashed_password,
                    admin=False)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user has been created!'})


@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'Sorry, no user found with this user id.'})
    user.admin = True
    db.session.commit()
    return jsonify({'message': 'The user has been promoted to admin.'})


@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'Sorry, no user found with this user id.'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'The user has been deleted from database.'})


@app.route('/login')
def login():
    # When no authorization information is passed
    auth = request.authorization
    if not auth or not auth.username or auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # When there is no user in the database for the user they passed in
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # When the password is incorrect
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


if __name__ == '__main__':
    app.run(debug=True)
