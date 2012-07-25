#import nose
import requests
import json

from config.parser import Config
from pymongo.connection import Connection
from database.db import Database

#def setup_func():
#    #TearDown DB
#    conn = Database().connect()
#    conn.drop_database("raceall_test")
#    conn.disconnect()
    
#def teardown_func():
#    pass

#@nose.tools.with_setup(setup_func, teardown_func)
def testFull():
    conn = Database().connect()
    conn.drop_database("raceall_test")
    conn.disconnect()

    data = {}
    data['user0'] = dict(username="user0")
    data['user1'] = dict(username="user1")
    data['user2'] = dict(username="user2")
    data['user3'] = dict(username="user3")
    data['user4'] = dict(username="user4")

    print "Create Users"
    headers = {'content-type': 'application/json'}
    url = "http://localhost:8888/user/"
    for user in data:
        payload = dict(username = user,
                       password1 = user,
                       password2 = user)

        jdata = json.dumps(payload)
        r = requests.post(url, data=jdata, headers=headers)

    print "Login Users"
    headers = {'content-type': 'application/json'}
    url = "http://localhost:8888/user/login/"
    for user in data:
        payload = dict(username = user,
                       password = user)

        jdata = json.dumps(payload)
        r = requests.post(url, data=jdata, headers=headers)
        data[user]['token'] = r.json['token']

    print "Get all uuids"
    headers = {'content-type': 'application/json'}
    url = "http://localhost:8888/user/"
    r = requests.get(url)
    id_data = r.json

    print "Create Friendships"
    for user in ['user1', 'user3']:
        url = "http://localhost:8888/user/friend/" + id_data[user] + '/'
        headers = {'Authorization': data['user0']['token']}
        r = requests.post(url, data=None, headers=headers)

    for user in ['user0', 'user4']:
        url = "http://localhost:8888/user/friend/" + id_data[user] + '/'
        headers = {'Authorization': data['user1']['token']}
        r = requests.post(url, data=None, headers=headers)

    print "Get Friendships"
    url = "http://localhost:8888/user/friend/"
    headers = {'Authorization': data['user0']['token']}
    r = requests.get(url, data=None, headers=headers)
    print r.json

    #print "Delete Friendships"
    #url = "http://localhost:8888/user/friend/" + id_data['user1'] + '/'
    #headers = {'Authorization': data['user0']['token']}
    #r = requests.delete(url, data=None, headers=headers)

    #print "Get Friendships"
    #url = "http://localhost:8888/user/friend/"
    #headers = {'Authorization': data['user0']['token']}
    #r = requests.get(url, data=None, headers=headers)
    #print r.json

    print "Create Races"
    url = "http://localhost:8888/race/"
    headers = {'Authorization': data['user0']['token']}
    payload = dict(name="race0",
                   vehicle="Cars",
                   description="race0",
                   private=True,
                   time=160)
    jdata = json.dumps(payload)
    r = requests.post(url, data=jdata, headers=headers)


    print "Get Friends Races"
    url = "http://localhost:8888/friend/race/" + id_data['user0'] + '/'
    headers = {'Authorization': data['user1']['token']}
    r = requests.get(url, data=None, headers=headers)
    print r.json

    race_data = r.json['0']

    print "Get Race Data"
    url = "http://localhost:8888/race/" + race_data + '/'
    headers = {'Authorization': data['user1']['token']}
    r = requests.get(url, data=None, headers=headers)
    print r.json

    #print "Delete Entire Race"
    #url = "http://localhost:8888/race/" + race_data + '/'
    #headers = {'Authorization': data['user0']['token']}
    #r = requests.delete(url, data=None, headers=headers)

    #print "Get Friends Races"
    #url = "http://localhost:8888/friend/race/" + id_data['user0'] + '/'
    #headers = {'Authorization': data['user1']['token']}
    #r = requests.get(url, data=None, headers=headers)
    #print r.json

    print "Add yourslef to race"
    url = "http://localhost:8888/race/" + race_data + '/user/'
    headers = {'Authorization': data['user1']['token']}
    payload = dict(friend_id=id_data['user0'])
    #payload = {}
    jdata = json.dumps(payload)
    r = requests.post(url, data=jdata, headers=headers)

    #print "Delete Race User Data"
    #url = "http://localhost:8888/race/" + race_data + '/user/'
    #headers = {'Authorization': data['user1']['token']}
    #r = requests.delete(url, data=None, headers=headers)
    #print r.json

    print "Get Race User Data"
    url = "http://localhost:8888/race/" + race_data + '/user/'
    headers = {'Authorization': data['user0']['token']}
    r = requests.get(url, data=None, headers=headers)
    print r.json

    print "Create Race Times"
    url = "http://localhost:8888/race/" + race_data + '/time/'
    headers = {'Authorization': data['user0']['token']}
    for time in [9999, 1234, 4321, 1111, 2222, 3333, 20, 20, 15, 999999]:
        payload = dict(time=time)
        jdata = json.dumps(payload)
        r = requests.post(url, data=jdata, headers=headers)

    print "Get Race Times"
    url = "http://localhost:8888/race/" + race_data + '/time/'
    headers = {'Authorization': data['user0']['token']}
    r = requests.get(url, data=None, headers=headers)
    print r.json



testFull()
