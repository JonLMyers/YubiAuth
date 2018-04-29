import sys
from flask import Flask, render_template
from flask_restful import Api
from mongoengine import *
from flask_jwt_extended import JWTManager, jwt_required
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)
APP.config.from_object('app.config')
APP.config['JWT_BLACKLIST_ENABLED'] = True
APP.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(APP)
rest_api = Api(APP)
db = connect('mongoenginetest', host='mongomock://localhost')

import app.api
rest_api.add_resource(api.UserRegistration, '/registration')
rest_api.add_resource(api.UserLogin, '/login')
rest_api.add_resource(api.UserLogoutAccess, '/logout/access')
rest_api.add_resource(api.UserLogoutRefresh, '/logout/refresh')
rest_api.add_resource(api.TokenRefresh, '/token/refresh')
rest_api.add_resource(api.SecretResource, '/secret')

@APP.route('/')
def root():
    return render_template('index.html')

@APP.route('/authenticate')
def authenticator():
    return render_template('auth.html')

@APP.route('/security')
def security():
    return render_template('security.html')

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return aaxus.models.token.RevokedToken.is_jti_blacklisted(jti)

