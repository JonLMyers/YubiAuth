import sys 
import sys
from flask import Flask, render_template
from flask_restful import Api
from mongoengine import *
from flask_jwt_extended import JWTManager, jwt_required
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object('app.config')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
rest_api = Api(app)
db = connect('mongoenginetest', host='mongomock://localhost')

import api
rest_api.add_resource(api.UserRegistration, '/registration')
rest_api.add_resource(api.UserLogin, '/login')
rest_api.add_resource(api.UserLogoutAccess, '/logout/access')
rest_api.add_resource(api.UserLogoutRefresh, '/logout/refresh')
rest_api.add_resource(api.TokenRefresh, '/token/refresh')
rest_api.add_resource(api.SecretResource, '/secret')

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/authenticate')
def authenticator():
    return render_template('auth.html')

@app.route('/security')
def security():
    return render_template('security.html')

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return aaxus.models.token.RevokedToken.is_jti_blacklisted(jti)

