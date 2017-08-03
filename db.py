#
# Database manager for handling transactions with mongodb
#

from pymongo import MongoClient
from config import *
import traceback


class Mdb:

    def __init__(self):

        # conn_str = "mongodb://%s:%s@%s:%d/%s" \
          #          % (DB_USER, DB_PASS, DB_HOST, DB_PORT, AUTH_DB_NAME)

        conn_str = 'mongodb://stbuser:stbpass@ds127531.mlab.com:27531/spottheball'
        client = MongoClient(conn_str)
        self.db = client['spottheball']

        print "[Mdb] connected to database :: ", self.db

    def add_game(self, pic, x1, y1, x2, y2, x3, y3, x4, y4, ball_x, ball_y):
        try:
            rec = {
                'pic': pic,
                'eyes': [
                    {'x': x1, 'y': y1},
                    {'x': x2, 'y': y2},
                    {'x': x3, 'y': y3},
                    {'x': x4, 'y': y4}
                ],
                'ball': [
                    {'x': ball_x, 'y': ball_y}
                ]
            }
            self.db.game.insert(rec)
            return True, "Success"
        except Exception as exp:
            print 'add_game() :: Got exception: %s' % exp
            print(traceback.format_exc())
            return False, "Exception: %s" % exp

    def get_game(self):
        collection = self.db["game"]
        result = collection.find({})

        ret = []
        for data in result:
            # print "<<=====got the data====>> :: %s" % data
            ret.append(data)

        return ret




###########################################
#          Add User in database           #
###########################################
    def add_user(self, username, name, email, password):
        try:
            rec = {
                'username': username,
                'name': name,
                'email': email,
                'password': password
            }
            self.db.user.insert(rec)

        except Exception as exp:
            print "login() :: Got exception: %s", exp
            print(traceback.format_exc())


###########################################
#          check User in database         #
###########################################
    def user_exists(self, email, password):
        """
        function checks if a user with given email and password
        exists in database
        :param email: email of the user
        :param password: password of the user
        :return: True, if user exists,
                 False, otherwise
        """
        return self.db.user.find({'email': email,
                                  'password': password}).count() > 0

###########################################
#              save ball position         #
###########################################
    def save_ball_position(self, game_id, ball_x, ball_y):
        try:
            rec = {
                'game_id': game_id,
                'ball': [
                    {'x': ball_x, 'y': ball_y}
                ]
            }
            self.db.bet.insert(rec)
        except Exception as exp:
            print "login() :: Got exception: %s", exp
            print(traceback.format_exc())


###########################################
#               get ball position         #
###########################################
    def get_ball_position(self, game_id):
        collection = self.db['bet']
        result = collection.find({'game_id': game_id})
        ret = []
        item = {}
        for data in result:
            item['game_id'] = data['_id']
            item['ball'] = data['ball']
            print 'id: ', item['game_id']
            print 'ball: ', item['ball']
            ret.append(item)
        # return JSONEncoder().encode({'ball position': ret})
            return ret


    def get_name(self, email):
        result = self.db.user.find({'email': email})
        name = ''
        email = ''
        if result:
            for data in result:
                name = data['name']
                print '', name
                email = data['email']
        return name


    def get_password(self, email):
        result = self.db.user.find({'email': email})
        name = ''
        password = ''
        if result:
            for data in result:
                print '', data
                name = data['username']
                print '', name
                password = data['password']
                print 'password in db class', password
        return password

if __name__ == "__main__":
    # quick test connecting to localdb
    mdb = Mdb()
    # mdb.add_game('56', '65', '789', '56', '98',
    # '123', '68', '57', '10', '11')
    # mdb.save_ball_position('1', '22', '33')
    # mdb.get_ball_position('1')
    mdb.get_password('tom@gmail.com')
