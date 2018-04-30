""" User Model """
from werkzeug.security import check_password_hash, generate_password_hash
from mongoengine import *
import datetime
import app.config
import jwt

class User(Document):
    username = StringField(max_length=50, required=True, unique=True)
    password_hash = StringField(max_length=128, required=True)
    yubikey_id = StringField(max_length=20, required=True)
    meta = {'unique': True}

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_u2f_devices(self):
        """Returns U2F devices"""
        return json.loads(self.u2f_devices)

    def set_u2f_devices(self, devices):
        """Saves U2F devices"""
        self.u2f_devices = json.dumps(devices)

    def has_u2f_devices(self):
        """Checks if user has any enrolled u2f devices"""
        return len(self.get_u2f_devices()) > 0

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