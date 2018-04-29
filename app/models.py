""" User Model """
from werkzeug.security import check_password_hash, generate_password_hash
from mongoengine import *
import datetime
import config
import jwt

class User(Document):
    username = StringField(max_length=50, required=True, unique=True)
    password_hash = StringField(max_length=128, required=True)
    meta = {'unique': True}

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_username(self, user_name):
        for user in User.objects(username = user_name):
            return user


""" Token Model """
from mongoengine import *

class RevokedToken(Document):
    jti = StringField(max_length=120, required=True)

    @classmethod
    def is_jti_blacklisted(self, jtokeni):
        for token in RevokedToken.objects(jti = jtokeni):
            return True
        return False