#!/usr/bin/env python

from pymongo import Connection
from config.parser import Config
from validatish import validate

class Validate():
    def __init__(self, data=None):
        #XXX: Decode it and make sure its JSON
        if not data:
            pass #XXX: Raise validation error

        self.data = data

    def new_user(self):
        errors = dict(username=[], password=[])
        if self.data.has_key('username'):
            username = self.data['username']
            if len(username) > 20 or len(username) < 3:
                errors['username'].append("Username must be between 3 and 20 characters")
            if not _plain(username):
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

        return _error(errors)

    def new_race(self):
        errors = dict(name=[], description=[], vehicle=[], private=[])
        if self.data.has_key('name'):
            name = self.data['name']
            if len(name) > 20 or len(name) < 3:
                errors['name'].append("Name must be between 3 and 20 characters")
            if not _string(name):
                errors['name'].append("Name must be a string")
        else:
            errors['name'].append("Name cannot be blank")

        if self.data.has_key('vehicle'):
            vehicle = self.data['vehicle']
            if len(vehicle) > 20 or len(vehicle) < 3:
                errors['name'].append("Vehicle name must be between 3 and 20 characters")
            if not _string(name):
                errors['name'].append("Vehicle mame must be a string")
        else:
            errors['name'].append("Vehicle name cannot be blank")

        if self.data.has_key('description'):
            desc = self.data['description']
            if len(desc) > 200:
                errors['name'].append("Description cannot be greater then 200 characters")
            if not _string(name):
                errors['name'].append("Description mame must be a string")
        else:
            errors['name'].append("Description cannot be blank")

        if self.data.has_key('private'):
            private = self.data['private']
            if not _bool(name):
                errors['name'].append("Privacy must be boolean")
        else:   
            errors['name'].append("Description cannot be blank")


    def _error(self, errors):
        for error in errors:
            if not error:
                del errors[error]

        return errors

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
