# src/api/users.py
from flask import Blueprint, request
from flask_restx import Resource, Api, fields, marshal_with
from src import db
from src.api.models import User

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)

# API model for User
user_model = api.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'created_date': fields.DateTime,
})

class UsersList(Resource):
    @api.expect(user_model, validate=True)  # Expecting user_model for POST request
    def post(self):
        post_data = request.get_json()
        username = post_data.get('username')
        email = post_data.get('email')
        response_object = {}

        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            response_object['message'] = 'Sorry. That email already exists.'
            return response_object, 400

        # Add new user to the database
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        response_object['message'] = f'{email} was added!'
        return response_object, 201

    @api.marshal_with(user_model, as_list=True)  # Serialize list of users
    def get(self):
        return User.query.all(), 200  # Fetch and return all users

class Users(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        return user

api.add_resource(UsersList, '/users')  # For listing and creating users
api.add_resource(Users, '/users/<int:user_id>')  # For retrieving a single user

