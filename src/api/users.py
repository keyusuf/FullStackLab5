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
    @api.expect(user_model, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get('username')
        email = post_data.get('email')
        response_object = {}

        user = User.query.filter_by(email=email).first()
        if user:
            response_object['message'] = 'Sorry. That email already exists.'
            return response_object, 400

        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        response_object['message'] = f'{email} was added!'
        return response_object, 201

    @api.marshal_with(user_model, as_list=True)
    def get(self):
        return User.query.all(), 200

class Users(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f"User {user_id} does not exist")
        return user

    @api.expect(user_model, validate=True)
    def put(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f"User {user_id} does not exist")

        post_data = request.get_json()
        user.username = post_data.get('username', user.username)
        user.email = post_data.get('email', user.email)
        db.session.commit()

        return {"message": f"User {user_id} was updated."}, 200

    def delete(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(404, f"User {user_id} does not exist")

        db.session.delete(user)
        db.session.commit()

        return {"message": f"User {user_id} was deleted."}, 200

api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<int:user_id>')
