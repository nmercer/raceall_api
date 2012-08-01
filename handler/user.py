import datetime
import tornado.web

from basehandler import BaseHandler
from database.db import Database
from bson.objectid import ObjectId
from validate import Validate

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
        data = Validate(self.request.body).new_user()

        pw_crypt = self.pw_encrpyt(data['password1'])
        self.db.insert('users', dict(username=data['username'],
                                     password=pw_crypt,
                                     created=datetime.datetime.utcnow()))


class UserRaceHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)
        self.db = Database()

    def get(self):
        race_list = []
        races = self.db.select('race_user', dict(user_id=self.user_id))
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
