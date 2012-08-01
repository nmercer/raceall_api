import tornado.web
import tornado.httpserver

from pymongo import Connection
from config.parser import Config
from validatish import validate

class Validate():
    def __init__(self, data=None):
        try:
            self.data = tornado.escape.json_decode(data)
        except ValueError:
            raise tornado.httpserver._BadRequestException("Invalid JSON structure.")

        if type(self.data) != dict:
            raise tornado.httpserver._BadRequestException("Invalid key value objects")

    def new_user(self):
        errors = dict(username=[], password=[])
        if self.data.has_key('username'):
            username = self.data['username']
            if len(username) > 20 or len(username) < 3:
                errors['username'].append("Username must be between 3 and 20 characters")
            if not self._plain(username):
                errors['username'].append("Username must be plain text")
        else:
            errors['username'].append("Username must not be blank")

        if self.data.has_key('password1') or self.data.has_key('password2'):
            pass1 = self.data['password1']
            pass2 = self.data['password2']

            if pass1 != pass2:
                errors['password'].append("Passwords must match")
            if len(pass1) < 5 or len(pass2) < 5:
                errors['password'].append("Passwords must be larger then 5 characters")
        else:
            errors['password'].append("Passwords cannot be blank")

        self._check_errors(errors)
        return self.data

    def new_race(self):
        errors = dict(name=[], description=[], vehicle=[], private=[])
        if self.data.has_key('name'):
            name = self.data['name']
            if len(name) > 20 or len(name) < 3:
                errors['name'].append("Name must be between 3 and 20 characters")
            if not self._string(name):
                errors['name'].append("Name must be a string")
        else:
            errors['name'].append("Name cannot be blank")

        if self.data.has_key('vehicle'):
            vehicle = self.data['vehicle']
            if len(vehicle) > 20 or len(vehicle) < 3:
                errors['name'].append("Vehicle name must be between 3 and 20 characters")
            if not self._string(name):
                errors['name'].append("Vehicle mame must be a string")
        else:
            errors['name'].append("Vehicle name cannot be blank")

        if self.data.has_key('description'):
            desc = self.data['description']
            if len(desc) > 200:
                errors['name'].append("Description cannot be greater then 200 characters")
            if not self._string(name):
                errors['name'].append("Description mame must be a string")
        else:
            errors['name'].append("Description cannot be blank")

        if self.data.has_key('private'):
            private = self.data['private']
            if not self._bool(name):
                errors['name'].append("Privacy must be boolean")
        else:   
            errors['name'].append("Description cannot be blank")

        self._check_errors(errors)
        return self.data

    def new_time(self):
        errors = dict(time=[])
        if self.data.has_key('time'):
            time = self.data['time']
            if self._int(time):
                errors['time'].append("Time must be an integer")
            if time <= 0:
                errors['time'].append("Time must be greater then 0")
                
        else:
            errors['time'].append("Time cannot be blank")

        self._check_errors(errors)
        return self.data

    #XXX: Need some sort of validation
    def new_race_user(self):
        return self.data

    def login(self):
        errors = dict(uername=[], password=[])
        if not self.data.has_key('username'):
            errors['username'].append("Username cannot be blank")

        if not self.data.has_key('password'):
            errors['time'].append("Password cannot be blank")

        self._check_errors(errors)
        return self.data



    def _check_errors(self, errors):
        error_dict = {}
        for error in errors:
            if not error:
                #XXX: Set json return for errors
                raise tornado.web.HTTPError(400)

        return

    def _plain(self, val):
        try:
            validate.is_plaintext(val)
        except:
            return False
        return True

    def _int(self, val):
        try:
            validate.is_integer(val)
        except:
            return False
        return True

    def _string(self, val):
        try:
            validate.is_string(val)
        except:
            return False
        return True

    def _bool(self, val):
        try:
            validate.is_one_of(val, [True, False])
        except:
            return False
        return True
