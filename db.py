#
# Database manager for handling transactions with mongodb
#

from pymongo import MongoClient
from bson import ObjectId
from config import *
import traceback
import datetime

class Mdb:

    def __init__(self):

        # conn_str = "mongodb://%s:%s@%s:%d/%s" \
        #           % (DB_USER, DB_PASS, DB_HOST, DB_PORT, AUTH_DB_NAME)

        conn_str = 'mongodb://stbuser:stbpass@ds127531.' \
                  'mlab.com:27531/spottheball'
        client = MongoClient(conn_str)
        self.db = client['spottheball']

        print "[Mdb] connected to database :: ", self.db

    def add_game(self, pic, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6,
                 x7, y7, x8, y8, ball_x, ball_y):
        try:
            ts = datetime.datetime.now().strftime("%d-%m-%y, %H:%M:%S")

            rec = {
                'pic': pic,

                'eyes': [
                    {'x': x1, 'y': y1},
                    {'x': x2, 'y': y2},
                    {'x': x3, 'y': y3},
                    {'x': x4, 'y': y4},
                    {'x': x5, 'y': y5},
                    {'x': x6, 'y': y6},
                    {'x': x7, 'y': y7},
                    {'x': x8, 'y': y8}
                ],

                'ball': [
                    {'x': ball_x, 'y': ball_y}
                ],
                'timestamp': ts
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
            ret.append(data)

        return ret

    def get_bet(self):
        collection = self.db["bet"]
        result = collection.find({})

        ret = []
        for data in result:
            ret.append(data)

        return ret
    #
    # def get_survey(self, _id):
    #     collection = self.db["survey"]
    #     result = collection.find( { '_id': ObjectId(_id) } )
    #     for data in result:
    #         return data

    def get_user_game(self):
        collection = self.db['game']
        result = collection.find().skip(self.db.game.count()-1)
        ret = None
        for data in result:
            ret = data
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
#          Add User in database           #
###########################################
    def add_admin(self, email, password):
        try:
            rec = {
                'email': email,
                'password': password
            }
            self.db.admin.insert(rec)
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

    def admin_exists(self, email, password):
        """
        function checks if a user with given email and password
        exists in database
        :param email: email of the user
        :param password: password of the user
        :return: True, if user exists,
                 False, otherwise
        """
        return self.db.admin.find({'email': email,
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

    def save_user_ball_position(self, game_id, user, ball_x, ball_y):
        try:
            ts = datetime.datetime.utcnow()
            rec = {
                'game_id': game_id,
                'user': user,
                'ball': [
                    {'x': ball_x, 'y': ball_y}
                ],
                'timestamp': ts
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
                email = data['email']
        return name

    def get_password(self, email):
        result = self.db.user.find({'email': email})
        name = ''
        password = ''
        if result:
            for data in result:
                name = data['username']
                password = data['password']
        return password

    def get_result(self, game_id):
        result = self.db.game.find({'game_id': game_id})
        for data in result:
            print "", data



if __name__ == "__main__":
    # quick test connecting to localdb
    mdb = Mdb()
    mdb.get_user_game()
    mdb.add_admin('tom@gmail.com', '123')
    # mdb.add_game('56', '65', '789', '56', '98',
    # '123', '68', '57', '10', '11')
    # mdb.save_ball_position('1', '22', '33')
    # mdb.get_ball_position('1')
    # mdb.get_password('tom@gmail.com')
    mdb.get_result("599d5c9fc2ba7031917ce142")
