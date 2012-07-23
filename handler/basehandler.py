import tornado.web
import json
import base64
import OpenSSL
import datetime

from bcrypt import hashpw, gensalt
from database.db import Database
from bson.objectid import ObjectId
from bson.code import Code

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header("Content-Type", "application/json")

    def jsoncheck(self, request):
        try:
            return tornado.escape.json_decode(request)
        except ValueError:
            raise tornado.web.HTTPError(400)

    def dict_to_json(self, data):
        self.write(json.dumps(data))

    def token_new(self, username):
        db = Database()

        user_data = db.select_one('users', dict(username=username))

        #Check if user already has token
        token = db.select_one('tokens', dict(users_id=user_data['_id']))
        if token:
            self.dict_to_json(dict(token = token['token']))
        else:
            token = base64.b64encode(OpenSSL.rand.bytes(16))
            db.insert('tokens', dict(users_id=user_data['_id'],
                                     token=token,
                                     created=datetime.datetime.utcnow()))

            self.write(dict(token = token))

    def token_check(self, token):
        db = Database()
        token_data = db.select_one('tokens', dict(token=token))

        if token_data:
            return ObjectId(token_data['users_id'])

        raise tornado.web.HTTPError(403)

    def pw_encrpyt(self, password):
        return hashpw(password, gensalt())

    def friend_check(self, user_id, friend_id):
        db = Database()
        friend_data = db.select_one('friends', dict(user_id = user_id,
                                                    friend_id = friend_id))
        user_data = db.select_one('friends', dict(user_id = friend_id,
                                                  friend_id = user_id))
        if friend_data and user_data:
            return True

        raise tornado.web.HTTPError(403)

    def race_user_check(self, user_id, race_id):
        db = Database()
        if db.select_one('race_user', dict(user_id = user_id,
                                           race_id = race_id)):
            return True
        return False

    def race_owner_check(self, user_id, race_id):
        db = Database()
        if db.select_one('races', dict(user_id = user_id,
                                       _id = race_id)):

            return True
        return False

    def race_public_check(self, race_id):
        db = Database()
        if db.select_one('races', dict(private = False,
                                       _id = race_id)):

            return True
        return False

    #def map(race_id):
    #    mapper = Code("""
    #                  function () {
    #                    this.races.forEach(function(z) {
    #                    
    #                """)
