""" Authentication Managment API """
import json
from flask import jsonify, request
from flask_restful import Resource, reqparse
from app import rest_api
from models import User
from models import RevokedToken
from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}, 500
        if data['password'] == '':
            return {'message': 'A password is required'}, 500
        
        new_user = User(
            username = data['username'],
            password_hash = User.hash_password(data['password'])
        )

        try:
            new_user.save()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return{
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        except:
            return{'message': 'Something went wrong'}, 500

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()

        current_user = User.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} Does Not Exist'.format(data['username'])}

        if current_user.check_password(data['password']):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token     
            }
        else:
            return {'message': 'Invalid Credentials'}, 500
        
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti = jti)
            revoked_token.save()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
    
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti = jti)
            revoked_token.save()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
            
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
       
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }