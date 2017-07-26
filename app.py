import os
from flask import Flask, request, render_template, redirect, send_from_directory, url_for, session, flash
from functools import wraps
import traceback
import jwt
import datetime
from werkzeug.utils import  secure_filename
from db import Mdb
import json
import jsonify
app = Flask(__name__)
mdb = Mdb()

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


@app.route('/')
def home():
    return 'Welcome to Spot The Ball'


#########################################
#              upload Image             #
#########################################
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = '%s/%s' % (dir_path, 'uploads')

app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'


def sumSessionCounter():
    try:
        session['counter'] += 1
    except KeyError:
        session['counter'] = 1


UPLOAD_FOLDER = file_path
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#########################################
#              token required           #
#########################################
app.config['secretkey'] = 'some-strong+secret#key'

def token_required(f):
    @wraps(f)
    def decoated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'missing token!!'})

        try:
            data = jwt.decode(token, app.config['secretkey'])
        except:
            return jsonify({'message': 'invaild token!'})
        return f(*args, **kwargs)
    return decoated


###################################################
#                                                 #
# specify the path here to server uploaded images #
#                                                 #
###################################################
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/admin')
def admin():
    templateData = {'title': 'admin'}
    return render_template("admin.html", **templateData)


@app.route('/user')
def user():
    templateData = {'title': 'user'}
    return render_template("user.html", **templateData)


@app.route('/signin')
def signin():
    templateData = {'title': 'Sign In'}
    return render_template("signin.html", **templateData)


@app.route('/game', methods=['GET'])
def load_game():
    templateData = {'title': 'Spot The Ball'}
    return render_template("game.html", **templateData)



###########################################
#          add game                       #
###########################################
@app.route('/add_game', methods=['POST'])
def add_game():
    ret = {}
    try:
        file = request.files['pic']

        filename = ""

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pic = '%s/%s' % (file_path, filename)

        x1 = request.form['x1']
        y1 = request.form['y1']
        x2 = request.form['x2']
        y2 = request.form['y2']
        x3 = request.form['x3']
        y3 = request.form['y3']
        x4 = request.form['x4']
        y4 = request.form['y4']
        ball_x = request.form['ball_x']
        ball_y = request.form['ball_y']

        print "file_path:", file_path

        mdb.add_game(filename, x1, y1, x2, y2, x3, y3, x4, y4, ball_x, ball_y)
        ret['error'] = 0
        ret['msg'] = 'Game is stored successfully'
    except Exception as exp:
        ret['error'] = 1
        ret['msg'] = exp
        print(traceback.format_exc())
    return json.dumps(ret)


###########################################
#          add user                       #
###########################################
@app.route("/add_user", methods=['POST'])
def add_user():
    try:
        user = request.form['user']
        email = request.form['email']
        password = request.form['password']
        mdb.add_user(user, email, password)
        print('User is added successfully')
        templateData = {'title': 'Signin Page'}
    except Exception as exp:
        print('add_user() :: Got exception: %s' % exp)
        print(traceback.format_exc())
    return render_template('user.html', session=session)


###########################################
#          login user                     #
###########################################
@app.route('/login', methods=['POST'])
def login():
    ret = {'err': 0}
    try:
        sumSessionCounter()
        email = request.form['email']
        password = request.form['password']
        if mdb.user_exists(email, password):
            session['name'] = email

            # Login Successful!

            expiry = datetime.datetime.utcnow() + datetime.\
                timedelta(minutes=30)
            token = jwt.encode({'user': email, 'exp': expiry},
                               app.config['secretkey'], algorithm='HS256')

            ret['msg'] = 'Login successful'
            ret['err'] = 0
            ret['token'] = token.decode('UTF-8')
            templateData = {'title': 'singin page'}
        else:
            # Login Failed!
            # return render_template('game.html', session=session)

            ret['msg'] = 'Login Failed'
            ret['err'] = 1

    except Exception as exp:
        ret['msg'] = '%s' % exp
        ret['err'] = 1
        print(traceback.format_exc())
    return json.dumps(ret)


###########################################
#          session logout                 #
###########################################
@app.route('/clear')
def clearsession():
    session.clear()
    return render_template('index.html', session=session)
    # return redirect(request.form('/signin'))


###########################################
#              get game                   #
###########################################
@app.route("/get_game", methods=['GET'])
def get_game():

    ret = {'err': 0, 'msg': 'Success'}

    try:
        ret["game"] = mdb.get_game()
    except Exception as exp:
        ret["msg"] = "Exceptiion: %s" % exp
        ret['err'] = 1
        print(traceback.format_exc())
    return JSONEncoder().encode(ret)




###########################################
#           save ball position            #
###########################################
@app.route('/save_ball_position')
def save_ball_position():
    return mdb.save_ball_position()

if __name__ == '__main__':
    app.run(debug=True)
