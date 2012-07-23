import datetime
import tornado.web

from basehandler import BaseHandler
from database.db import Database
from bson.objectid import ObjectId

class UsersHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self):
        self.db = Database()

    def get(self):
        test = {}
        for x in self.db.select('users', {}):
            test[x['username']] =  _id=str(x['_id'])
        self.write(test)

    def post(self):
        data = self.jsoncheck(self.request.body)

        user_err = []
        pass_err = []

        #XXX: Sanitize user, pw1, pw2, large lengths for username and password
        if len(data['username']) < 4:
            user_err.append('Username must be larger then 3 characters')
        if len(data['password1']) < 4:
            pass_err.append('Password must be larger then 3 characters')
        if data['password1'] != data['password2']:
            pass_err.append('Password\'s do not match')
        #XXX: Maybe not the best way to test this
        for users in self.db.select('users', dict(username=data['username'])):
            user_err.append('Username already exists')

        if user_err or pass_err:
            self.dict_to_json(dict(user=user_err, pw=pass_err))
            #XXX: This Needs Some Work
            raise tornado.web.HTTPError(400)


        pw_crypt = self.pw_encrpyt(data['password1'])
        self.db.insert('users', dict(username=data['username'],
                                     password=pw_crypt,
                                     created=datetime.datetime.utcnow()))

class UserFriendHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)
        self.db = Database()

    def get(self):
        friend_data = self.db.select('friends', dict(user_id=self.user_id))

        #XXX: Validation

        friends = {}
        for idx,friend in enumerate(friend_data):
            if self.db.select_one('friends', dict(user_id=friend['friend_id'],
                                                  friend_id=self.user_id)):
                friends[idx] = str(friend['friend_id'])

        self.write(friends)

    def post(self, friend_id):
        friend_id = ObjectId(friend_id)

        #XXX: Validation

        has_user = self.db.select_one('users', dict(_id = friend_id))
        has_friend = self.db.select_one('friends', dict(user_id = self.user_id,
                                                        friend_id = friend_id))
        if has_user and not has_friend:
            self.db.insert('friends', dict(user_id = self.user_id,
                                           friend_id = friend_id))

    def delete(self, friend_id):
        friend_id = ObjectId(friend_id)

        #XXX: Validation

        self.db.delete('friends', dict(user_id = self.user_id,
                                       friend_id = friend_id))

class UserInfoHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self, race_id):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)
        self.db = Database()

class UserRaceHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)
        self.db = Database()

    def get(self):
        pass
        #XXX: Return ID's
        #self.write(
