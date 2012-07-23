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
        race_data = self.db.select_one('races', dict(_id=ObjectId(race_id)))
        owner_id = race_data['user_id']

        if self.race_public_check(ObjectId(race_id)) or owner_id == self.user_id or self.friend_check(self.user_id, owner_id):
            del race_data['_id']
            del race_data['created']
            race_data['user_id'] = str(race_data['user_id'])
            self.write(race_data)
        else:
            raise tornado.web.HTTPError(403)
         
        
    def post(self):
        data = self.jsoncheck(self.request.body)

        #XXX: Validation

        race_id = self.db.insert('races', dict(name=data['name'],
                                               vehicle=data['vehicle'],
                                               description = data['description'],
                                               user_id = self.user_id,
                                               created = datetime.datetime.utcnow(),
                                               private = data['private']))

        #XXX: Grab GPS data and unpack it into gps table

        self.db.insert('race_time', dict(user_id = self.user_id,
                                         race_id = ObjectId(race_id),
                                         time = data['time']))

        self.db.insert('race_user', dict(user_id = self.user_id,
                                         race_id = ObjectId(race_id)))
        #XXX: Return code or data

    def put(self, race_id):
        data = self.jsoncheck(self.request.body)

        #XXX: Validation

        race_data = self.db.select_one('races', dict(_id=ObjectId(race_id)))
        owner_id = race_data['user_id']
        if owner_id == self.user_id:
            #XXX: Need to create update method
            db.update('races')

            #XXX: If updating GPS data will need to unpack and update gps

            #XXX: Return code or data
        else:
            raise tornado.web.HTTPError(403)


    def delete(self, race_id):
        #XXX: Validation

        race_data = self.db.select_one('races', dict(_id=ObjectId(race_id)))
        owner_id = race_data['user_id']
        if owner_id == self.user_id:
            self.db.delete('race_user', dict(race_id = ObjectId(race_id)))
            self.db.delete('race_times', dict(race_id = ObjectId(race_id)))
            self.db.delete('race_gps', dict(race_id = ObjectId(race_id)))
            self.db.delete('races', dict(_id = ObjectId(race_id)))
            #XXX: Return code or data

        else:
            raise tornado.web.HTTPError(403)
        

class RaceUserHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)
        self.db = Database()

    #XXX: Do we need race_id in this or can it go in initialize?
    def get(self, race_id):
        #XXX: Validation

        if not self.race_user_check(self.user_id, ObjectId(race_id)):
            raise tornado.web.HTTPError(403)

        race_data = self.db.select('race_user', dict(race_id = ObjectId(race_id)))

        users = {}
        for idx,user in enumerate(race_data):
            users[idx] = str(user['user_id'])

        self.write(users)

    def post(self, race_id):
        data = self.jsoncheck(self.request.body)

        #XXX: Validation

        #XXX: Make sure use is not already in race
        if self.race_user_check(self.user_id, ObjectId(race_id)):
            raise tornado.web.HTTPError(403)

        #XXX: These to functions are calling the same insert
        if data.has_key('friend_id'):
            self.friend_check(self.user_id, ObjectId(data['friend_id']))
            if not self.race_user_check(ObjectId(data['friend_id']), ObjectId(race_id)):
                raise tornado.web.HTTPError(403)
            self.db.insert('race_user', dict(race_id=ObjectId(race_id),
                                             user_id=self.user_id))
            #XXX: Return code or data

        elif self.race_public_check(ObjectId(race_id)):
            self.db.insert('race_user', dict(race_id=ObjectId(race_id),
                                             user_id=self.user_id))
            #XXX: Return code or data

        else:
            raise tornado.web.HTTPError(403)

    def delete(self, race_id):
        #XXX: Validation
        if not self.race_user_check(self.user_id, ObjectId(race_id)):
            raise tornado.web.HTTPError(403)
            
        #XXX: Delete User from race
        self.db.delete('race_user', dict(race_id = ObjectId(race_id),
                                         user_id = self.user_id))

        #XXX Return code or data


class RaceTimeHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self, race_id):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)
        self.db = Database()

    def get(self):
        #XXX: Validation

        self.race_user_check(self.user_id, ObjectId(race_id))

        race_data = self.db.select('race_time', dict(race_id = ObjectId(race_id)))

        times = {}
        #XXX: Need to return dict of id's dict of top five times organized!
        #for time in race_data:
        #    if times.has_key(str(time['user_id'])):
        #        times[str(time['user_id'])].append(time['time']) 
        #    else:
        #        times[str(time['user_id'])] = [time['time']]

        #for time in times:
        #    for idx,data in enumerate(times[time]):
        #        times[time][idx] = data

        self.write(times)

    def post(self):
        data = self.jsoncheck(self.request.body)

        #XXX: Validation

        self.race_user_check(self.user_id, ObjectId(race_id))

        #XXX: If we have 5 times for this race already, drop lowest time.
        #race_data = self.db.select('race_time', dict(race_id = ObjectId(race_id),
        #                                             user_id = self.user_id))
        #if len(race_data) > 4:
        #    user_id = None
        #    for time in race_data:

        db.insert('race_time', dict(user_id = self.user_id,
                                race_id = ObjectId(race_id),
                                time = data['time']))

        #XXX Return code or data

class RaceGpsHandler(BaseHandler):
    @tornado.web.addslash
    def initialize(self, race_id):
        token = self.request.headers.get('Authorization', 'http')
        self.user_id = self.token_check(token)
        self.db = Database()

    def get(self):
        pass

    def put(self):
        pass

