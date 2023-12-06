# src/api/ping.py
from flask import Blueprint, jsonify
from flask_restx import Resource, Api

ping_blueprint = Blueprint('ping', __name__)
api = Api(ping_blueprint)

class Ping(Resource):
    def get(self):
        return jsonify({
            'status': 'success',
            'message': 'pong!'
        })

api.add_resource(Ping, '/ping')
