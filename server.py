import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.options

from handler.user import *
from handler.login import *
from handler.race import *
from handler.friend import *

from tornado.options import define, options
define("port", default=8888, help="wth is this", type=int)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = application = tornado.web.Application([

        (r'/user/',                UsersHandler),
        (r'/user/login/',          LoginHandler),
        (r'/user/friend/',         UserFriendHandler),
        (r'/user/friend/(.*)/',    UserFriendHandler),
        (r'/user/race/',           UserRaceHandler),
        (r'/user/info/',           UserInfoHandler),

        (r'/race/',                RaceHandler),
        #(r'/race/(.*)/',           RaceHandler),
        (r'/race/(.*)/user/',      RaceUserHandler),
        (r'/race/(.*)/time/',      RaceTimeHandler),
        (r'/race/(.*)/gps/',       RaceGpsHandler),

        (r'/friend/info/(.*)/',    FriendInfoHandler),
        (r'/friend/race/(.*)/',    FriendRaceHandler)

    ], debug = True)


    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
