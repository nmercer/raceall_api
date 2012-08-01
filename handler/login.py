import tornado.web

from basehandler import BaseHandler
from database.db import Database
from bcrypt import hashpw
from validate import Validate


class LoginHandler(BaseHandler):
    @tornado.web.addslash
    def post(self):
        data = Validate(self.request.body).login()

        user_data = self.db.select_one('users', dict(username=data['username']))

        if user_data and hashpw(data['password'], user_data['password']) == user_data['password']:
            self.token_new(data['username'])
        else:
            raise tornado.web.HTTPError(401)
