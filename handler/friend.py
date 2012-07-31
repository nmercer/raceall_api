import tornado.web

from basehandler import BaseHandler
from database.db import Database
from bson.objectid import ObjectId


class FriendsHandler(BaseHandler):
    @tornado.web.addslash
    def get(self):
        self.db = Database()

        token = self.request.headers.get('Authorization', 'http')
        user_id = self.token_check(token)

        friend_data = self.db.select('friends', dict(user_id = user_id))

        friends = []
        for friend in friend_data:
            if self.friend_check(user_id, friend['friend_id']):
                friend_data = self.db.select_one('users', dict(_id = friend['friend_id']))
                friends.append([friend_data['username'], str(friend_data['_id'])])

        friend_data = {}
        for idx,friend in enumerate(friends):
            friend_data[idx] = dict(username = friend[0],
                                    user_id = friend[1])

        self.write(friend_data)


class FriendHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)
        self.db = Database()

    def get(self, friend_id):
        friend_id = ObjectId(friend_id)

        if self.friend_check(self.user_id, friend_id):
            races = self.db.select('race_user', dict(user_id = friend_id))
            race_list = []

            for race in races:
                race_data = self.db.select_one('races', dict(_id = race['race_id']))
                race_data = dict(_id = str(race_data['_id']),
                                 name = race_data['name'],
                                 vehicle = race_data['vehicle'],
                                 private = race_data['private'])

                times = self.db.select('race_time', dict(race_id = race['race_id']))
                user_times = sorted([[x['time'],x['user_id']] for x in times])[-5:]

                time_data = {}
                for idx,time in enumerate(user_times):
                    name = self.db.select_one('users', dict(_id=time[1]))['username']
                    time_data[idx] = dict(time = time[0],
                                          user_id = str(time[1]),
                                          name = name)


                race_list.append(dict(times = time_data,
                                      race = race_data))

            race_data = {}
            for idx,race in enumerate(race_list):
                race_data[idx] = race

            self.write(race_data)

        else:
            raise tornado.web.HTTPError(400)


    def post(self, friend_id):
        friend_id = ObjectId(friend_id)

        has_user = self.db.select_one('users', dict(_id = friend_id))
        has_friend = self.db.select_one('friends', dict(user_id = self.user_id,
                                                        friend_id = friend_id))
        if has_user and not has_friend:
            self.db.insert('friends', dict(user_id = self.user_id,
                                           friend_id = friend_id))

    def delete(self, friend_id):
        friend_id = ObjectId(friend_id)

        self.db.delete('friends', dict(user_id = self.user_id,
                                       friend_id = friend_id))
