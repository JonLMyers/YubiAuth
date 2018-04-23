import sys 
import sys
from flask import Flask
from flask_restful import Api
from mongoengine import *
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from mongoengine import connect, MongoEngineConnectionError

DB = MongoEngine()
db = connect('mongoenginetest', host='mongomock://localhost')

app = Flask(__name__)
CORS(app)
app.config.from_object('app.config')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
rest_api = Api(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return aaxus.models.token.RevokedToken.is_jti_blacklisted(jti)

