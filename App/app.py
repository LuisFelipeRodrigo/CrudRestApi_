from cmath import e
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= environ.get('DB_URL')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique =True, nullable=False)
    
    def json(self):
        return{'id': id,'username': self.username, 'email': self.email}

db.create_all()

@app.route('/test', methods=['GET'])
def test(): 
    return make_response(jsonify({'message':'test route'}), 200)

#created user
@app.route('/test', methods=['POST'])
def create_user():
    try:
        data = request.get_jason()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'mesage':'user created'}), 201)
    except e:
      return make_response(jsonify({'mesage': 'error creating user'}), 500)     

#get user 
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify({'users':[user.json() for user in users]}), 200)
    except e:
        make_response(jsonify({'mesage': 'error getting users'}), 500)

#get user by id 
@app.route('/users/<int:id>', method=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        return make_response(jsonify({'user': user.jason()}), 200)
    except e:
        return make_response(jsonify({'mesage': 'error getting user'}), 500)

#update user   
@app.route('/users/<int:id>', method=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'mesage':'user update'}), 200)
        return make_response(jsonify({'mesage': 'user not found'}), 404)
    except e:
        return make_response(jsonify({'mesage': 'error updating user'}), 500)
    