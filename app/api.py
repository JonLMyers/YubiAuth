""" Authentication Managment API """
import json, sys
from flask import jsonify, request
from flask_restful import Resource, reqparse
from app import rest_api
from app.models import User
from app.models import RevokedToken
from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from yubico_client import Yubico
from yubico_client import yubico_exceptions
from yubico_client.py3 import PY3

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('yubikey', help = 'This is needed to use the forge', required = False)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        print(data)
        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}, 500
        if data['password'] == '':
            return {'message': 'A password is required'}, 500
        if data['yubikey'] == '':
            return {'message': 'A yubikey OTP is required'}, 500

        otp = data['yubikey']
        new_user = User(
            username = data['username'],
            password_hash = User.hash_password(data['password']),
            yubikey_id = otp[0:12]
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
        print(data)

        current_user = User.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} Does Not Exist'.format(data['username'])}

        if current_user.check_password(data['password']):
            otp = data['yubikey']

            client = Yubico(33781, None)
            
            status = False
            try:
                status = client.verify(otp)
            except yubico_exceptions.InvalidClientIdError:
                e = sys.exc_info()[1]
                print('Client with id %s does not exist' % (e.client_id))
                sys.exit(1)
            except yubico_exceptions.SignatureVerificationError:
                print('Signature verification failed')
                sys.exit(1)
            except yubico_exceptions.StatusCodeError:
                e = sys.exc_info()[1]
                print('Negative status code was returned: %s' % (e.status_code))
                sys.exit(1)

            if status:
                print('OTP: ' + str(status))
                access_token = create_access_token(identity = data['username'])
                refresh_token = create_refresh_token(identity = data['username'])
                return {
                    'message': 'Logged in as {}'.format(data['username']),
                    'access_token': access_token,
                    'refresh_token': refresh_token     
                }
            else:
                return {'message': "Invalid OTP"}, 403
        else:
            return {'message': 'Invalid Credentials'}, 403
 
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
