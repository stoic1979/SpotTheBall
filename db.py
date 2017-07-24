#
# Database manager for handling transactions with mongodb
#

from pymongo import MongoClient
import traceback
import json
from config import *
from bson import ObjectId

######################################################
#                                                    #
# Note: _id of mongodb collection was not getting    #
# json encoded, so had to create this json encoder   #
#                                                    #
######################################################


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class Mdb:

    def __init__(self):
        #conn_str = "mongodb://%s:%s@%s:%d/%s" \
         #         % (DB_USER, DB_PASS, DB_HOST, DB_PORT, AUTH_DB_NAME)
        conn_str = 'mongodb://stbuser:stbpass@ds127531.mlab.com:27531/spottheball'

        client = MongoClient(conn_str)
        self.db = client['games']

        print "[Mdb] connected to database :: ", self.db

    def add_game(self, pic, x1, y1, x2, y2, x3, y3, x4, y4, x, y):
        try:
            rec = {
                'pic': pic,
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'x3': x3,
                'y3': y3,
                'x4': x4,
                'y4': y4,
                'x': x,
                'y': y,

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
            print "<<=====got the data====>> :: %s" % data
            ret.append(data)
        return JSONEncoder().encode({'game': ret})


if __name__ == "__main__":
    # quick test connecting to localdb
    mdb = Mdb()
    mdb.add_game('56', '65', '789', '56', '98', '123', '68', '57', '10', '11')
    # mdb.retrieve_data('LuminoGuru Pvt. Ltd.')
