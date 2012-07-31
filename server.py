import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options

from handler.user import *
from handler.login import *
from handler.race import *
from handler.friend import *

from tornado.options import define, options
define("port", default=8888, help="help", type=int)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = application = tornado.web.Application([

        (r'/user/',                          UsersHandler),
        (r'/user/login/',                    LoginHandler),
        (r'/user/races/',                    UserRaceHandler),

        (r'/friend/',                        FriendsHandler),
        (r'/friend/([0-9A-Za-z]+)/',         FriendHandler),

        #(r'/user/friend/',                   UserFriendHandler),
        #(r'/user/friend/([0-9A-Za-z]+)/',    UserFriendHandler),
        #(r'/user/races/',                    UserRaceHandler),
        #(r'/user/info/',                     UserInfoHandler),

        (r'/race/',                          RaceHandler),
        (r'/race/([0-9A-Za-z]+)/',           RaceHandler),
        (r'/race/([0-9A-Za-z]+)/user/',      RaceUserHandler),
        (r'/race/([0-9A-Za-z]+)/time/',      RaceTimeHandler),
        (r'/race/([0-9A-Za-z]+)/gps/',       RaceGpsHandler),
        #(r'/race/([0-9A-Za-z]+)/info/',      RaceInfoHandler),

        #(r'/friend/info/([0-9A-Za-z]+)/',    FriendInfoHandler),
        #(r'/friend/race/([0-9A-Za-z]+)/',    FriendRaceHandler)

    ], debug = True)


    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
