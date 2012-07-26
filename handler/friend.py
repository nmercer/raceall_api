import tornado.web

from basehandler import BaseHandler
from database.db import Database
from bson.objectid import ObjectId


class FriendInfoHandler(BaseHandler):
    @tornado.web.addslash
    def get(self, friend_id):
        #XXX: Validation
        self.db = Database()

        token = self.request.headers.get('Authorization', 'http')
        user_id = self.token_check(token)

        friend_id = ObjectId(friend_id)
        self.friend_check(user_id, friend_id)

        friend_data = self.db.select('users', dict(_id, friend_id))
        #XXX: Get data needed and return
        


class FriendRaceHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)
        self.db = Database()

    def get(self, friend_id):
        #XXX: Validation
        friend_id = ObjectId(friend_id)
        self.friend_check(self.user_id, friend_id)

        race_data = self.db.select('races', dict(user_id = friend_id))
        races = {}

        for idx,race in enumerate(race_data):
            races[idx] = str(race['_id'])

        self.write(races)

        #XXX: Get data from races
        #XXX: Get data needed and return

