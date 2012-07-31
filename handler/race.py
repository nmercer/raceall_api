import datetime
import tornado.web

from basehandler import BaseHandler
from database.db import Database
from bson.objectid import ObjectId

class RaceHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)
        self.db = Database()

    def get(self, race_id):
        race_id = ObjectId(race_id)

        race_data = self.db.select_one('races', dict(_id=race_id))
        owner_id = race_data['user_id']

        if self.race_public_check(race_id) or owner_id == self.user_id or self.friend_check(self.user_id, owner_id):
            race_data = self.db.select_one('races', dict(_id = race_id))
            race_data['_id'] = str(race_data['_id'])
            race_data['user_id'] = str(race_data['user_id'])
            del race_data['created']
    
            times = self.db.select('race_time', dict(race_id = race_id))

            user_times = {}
            for time in times:
                time_id = str(time['user_id'])
                if user_times.has_key(time_id):
                    user_times[time_id].append(time['time'])
                else:
                    user_times[time_id] = [time['time']]

            race_list = dict(times = user_times,
                             race = race_data)

            self.write(race_list)
        else:
            raise tornado.web.HTTPError(403)
         
        
    def post(self):
        #Validation
        data = self.jsoncheck(self.request.body)
        try:
            name = self.validate_name(data['name'])
            vehicle = self.validate_string(data['vehicle'])
            description = self.validate_string(data['description'])
            private = self.validate_bool(data['private'])
        except KeyError:
            raise tornado.web.HTTPError(400)
        

        race_id = self.db.insert('races', dict(name=data['name'],
                                               vehicle=data['vehicle'],
                                               description = data['description'],
                                               user_id = self.user_id,
                                               created = datetime.datetime.utcnow(),
                                               private = data['private']))

        race_id = ObjectId(race_id)

        #XXX: Grab GPS data and unpack it into gps table

        self.db.insert('race_time', dict(user_id = self.user_id,
                                         race_id = race_id,
                                         time = data['time']))

        self.db.insert('race_user', dict(user_id = self.user_id,
                                         race_id = race_id))

    #XXX: Need update method for race data
    def put(self, race_id):
        #Validate
        data = self.jsoncheck(self.request.body)

        race_data = self.db.select_one('races', dict(_id=ObjectId(race_id)))
        owner_id = race_data['user_id']
        if owner_id == self.user_id:
            #XXX: Need to create update method
            self.db.update('races')
            #XXX: If updating GPS data will need to unpack and update gps
        else:
            raise tornado.web.HTTPError(403)


    def delete(self, race_id):
        race_id = ObjectId(race_id)
        race_data = self.db.select_one('races', dict(_id=race_id))
        owner_id = race_data['user_id']

        if owner_id == self.user_id:
            self.db.delete('race_user', dict(race_id = race_id))
            self.db.delete('race_times', dict(race_id = race_id))
            self.db.delete('race_gps', dict(race_id = race_id))
            self.db.delete('races', dict(_id = race_id))
        else:
            raise tornado.web.HTTPError(403)
        

class RaceUserHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)
        self.db = Database()

    def get(self, race_id):
        race_id = ObjectId(race_id)

        if not self.race_user_check(self.user_id, race_id):
            raise tornado.web.HTTPError(403)

        race_data = self.db.select('race_user', dict(race_id = race_id))

        users = {}
        for idx,user in enumerate(race_data):
            users[idx] = str(user['user_id'])

        self.write(users)

    def post(self, race_id):
        #Check JSON
        data = self.jsoncheck(self.request.body)

        #Check data
        race_id = ObjectId(race_id)

        if data.has_key('friend_id'):
            friend_id = ObjectId(data['friend_id'])
        else:
            friend_id = None

        if (not self.race_user_check(self.user_id, race_id) and 
           (self.friend_check(self.user_id, friend_id) or 
           self.race_public_check(race_id))):
            self.db.insert('race_user', dict(race_id=race_id,
                                             user_id=self.user_id))
        else:
            raise tornado.web.HTTPError(403)


    def delete(self, race_id):
        race_id = ObjectId(race_id)
        if not (self.race_user_check(self.user_id, race_id) or
                self.race_owner_check(user_id, race_id)):
            raise tornado.web.HTTPError(403)

        self.db.delete('race_user', dict(race_id = ObjectId(race_id),
                                         user_id = self.user_id))


class RaceTimeHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)

    #def get(self, race_id):
    #    race_id = ObjectId(race_id)
    #
    #    #Check Data
    #    if self.race_user_check(self.user_id, race_id):
    #        race_data = self.db.select('race_time', dict(race_id = race_id))
    #        times = sorted([x['time'] for x in race_data])
    #
    #        data = {}
    #        for idx,time in enumerate(times):
    #            data[idx] = time
    # 
    #        self.write(data)
    #    else:
    #        raise tornado.web.HTTPError(403)

    def post(self, race_id):
        #Validate input
        data = self.jsoncheck(self.request.body)
        try:
            self.validate_time(data['time'])
        except KeyError:
           raise tornado.web.HTTPError(400)

        race_id = ObjectId(race_id)
        if self.race_user_check(self.user_id, race_id):
            race_data = self.db.select('race_time', dict(race_id = race_id, user_id = self.user_id))
            times = [[x['time'],x['_id']] for x in race_data]
            
            if len(times) > 4:
                if data['time'] > min(times)[0]:
                    self.db.delete('race_time', dict(_id=min(times)[1]))
                else:
                    raise tornado.web.HTTPError(400)
                
            self.db.insert('race_time', dict(user_id = self.user_id,
                                             race_id = race_id,
                                             time = data['time']))
        else:
            raise tornado.web.HTTPError(403)

class RaceGpsHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self, race_id):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)

    def get(self):
        pass

    def put(self):
        pass

