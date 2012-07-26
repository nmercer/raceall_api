#!/usr/bin/env python

from pymongo import Connection
from config.parser import Config

class Database():
    def __init__(self):
        config = Config()
        self.host = config.parser['database']['host']
        self.port = int(config.parser['database']['port'])
        self.db_name = config.parser['database']['name']
        self.conn = Connection(self.host, self.port)
        self.db = self.conn[self.db_name]

    def insert(self, collection=None, *args):
        if collection:
            return self.db[collection].insert(args[0])

    def select(self, collection=None, *args):
        if collection:
            return self.db[collection].find(args[0])

    def select_one(self, collection=None, *args):
        if collection:
            return self.db[collection].find_one(args[0])

    def delete(self, collection=None, *args):
        if collection:
            return self.db[collection].remove(args[0])

    def update(self, collection=None, *args):
        if collection:
            return self.db[collection].update(args[0])

    def close(self):
        self.conn.disconnect()

    #Return database cursor
    def connect(self):
        return Connection(self.host, self.port)
