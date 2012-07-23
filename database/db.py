#!/usr/bin/env python

from pymongo import Connection
from config.parser import Config

class Database():
    def __init__(self):
        config = Config()
        self.host = config.parser['database']['host']
        self.port = int(config.parser['database']['port'])
        self.db_name = config.parser['database']['name']

    def insert(self, collection=None, *args):
        if collection:
            #Connect
            conn = Connection(self.host, self.port)
            db = conn[self.db_name]

            #Work
            data = db[collection].insert(args[0])

            #Disconnect
            conn.disconnect()
            return data

    def select(self, collection=None, *args):
        if collection:
            #Connect
            conn = Connection(self.host, self.port)
            db = conn[self.db_name]

            #Work
            data = db[collection].find(args[0])

            #Disconnect
            conn.disconnect()
            return data

    def select_one(self, collection=None, *args):
        if collection:
            #Connect
            conn = Connection(self.host, self.port)
            db = conn[self.db_name]

            #Work
            data = db[collection].find_one(args[0])

            #Disconnect
            conn.disconnect()
            return data


    def delete(self, collection=None, *args):
        if collection:
            #Connect
            conn = Connection(self.host, self.port)
            db = conn[self.db_name]

            #Work
            data = db[collection].remove(args[0])

            #Disconnect
            conn.disconnect()
            return data


    def update(self, collection=None, *args):
        if collection:
            #Connect
            conn = Connection(self.host, self.port)
            db = conn[self.db_name]

            #Work
            data = db[collection].update()

            #Disconnect
            conn.disconnect()
            return data

    #Return database cursor
    def connect(self):
        return Connection(self.host, self.port)

