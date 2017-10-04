import os
from flask import Flask, request, render_template, redirect, \
    send_from_directory, url_for, session, flash
from flask.ext.bcrypt import Bcrypt
from functools import wraps
import traceback
import jwt
import datetime
from werkzeug.utils import secure_filename
from db import Mdb
import json
import jsonify
from bson import ObjectId
from functools import wraps
from flask import g, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user,\
    current_user

app = Flask(__name__)
bcrypt = Bcrypt(app)
mdb = Mdb()

app.config['secretkey'] = 'some-strong+secret#key'
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'


#############################################
#                                           #
#                SESSION COUNTER            #
#                                           #
#############################################
def sumSessionCounter():
    try:
        session['counter'] += 1
    except KeyError:
        session['counter'] = 1

#
# def login_required(f):
#     @wrap(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#
#         else:
#             flash("you need to login first")
#             return redirect(url_for('admin'))
#
#     return wrap


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('admin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


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

# setup Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/admin_login/')


@app.route('/admin')
def home():
    return render_template("admin/admin_login.html", session=session)


#########################################
#              upload Image             #
#########################################
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = '%s/%s' % (dir_path, 'uploads')

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


@app.route('/admin/create_game', methods=['POST'])
def save_img():

    prefix = request.base_url[:-len('/admin/create_game')]

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

        print "file_path:", file_path

        save_file_url = "%s/uploads/%s" % (prefix, filename)

        print "save_file_url: ", save_file_url

        templateData = {'imgGame': save_file_url, 'title': 'Create Game'}
        return render_template("admin/create_game.html", **templateData)

    except Exception as exp:
        ret['error'] = 1
        ret['msg'] = exp
        print(traceback.format_exc())
    return json.dumps(ret)


###########################################
#          add game                       #
###########################################
@app.route('/add_game', methods=['POST'])
def add_game():
    ret = {}
    try:
        x1 = request.form['x1']
        y1 = request.form['y1']
        x2 = request.form['x2']
        y2 = request.form['y2']
        x3 = request.form['x3']
        y3 = request.form['y3']
        x4 = request.form['x4']
        y4 = request.form['y4']
        x5 = request.form['x5']
        y5 = request.form['y5']
        x6 = request.form['x6']
        y6 = request.form['y6']
        x7 = request.form['x7']
        y7 = request.form['y7']
        x8 = request.form['x8']
        y8 = request.form['y8']

        ball_x = request.form['ball_x']
        ball_y = request.form['ball_y']

        bg_img = request.form['bgImg']

        mdb.add_game(bg_img, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6,
                     x7, y7, x8, y8, ball_x, ball_y)
        ret['error'] = 0
        ret['msg'] = 'Game is stored successfully'
    except Exception as exp:
        ret['error'] = 1
        ret['msg'] = exp
        print(traceback.format_exc())
    tmpl_data = {'status': ret}
    return render_template('admin/game_saved.html', **tmpl_data)


###########################################
#            magnifying tool              #
###########################################
@app.route('/magnify')
def magnifying():
    return render_template("index.html", session=session)
###########################################
#                 get game                #
###########################################
# @app.route('/save_ball_position')
# def save_ball_position():
#     return mdb.save_ball_position()


###############################################################################
#                                                                             #
#                                                                             #
#                                 ADMIN PANNEL                                #
#                                                                             #
#                                                                             #
###############################################################################
@app.route('/admin_login/')
def admin1():
    return render_template("admin/admin_login.html", session=session)


@app.route('/admin/home')
@login_required
def admin():
    return render_template("admin/admin.html", session=session)


@app.route('/admin/add_game_img')
def add_game_img():
    return render_template("admin/add_game_img.html", session=session)


#############################################
#                GET GAME RESULT            #
#############################################
@app.route("/admin/game_result", methods=['GET'])
def get_games_result():
    bets = mdb.get_bet()
    templateData = {'title': 'Game Result', 'bets': bets}
    return render_template("admin/game_result.html", **templateData)


#############################################
#                GET ALL GAME               #
#############################################
@app.route("/admin/all_game", methods=['GET'])
def get_games():
    games = mdb.get_game()
    templateData = {'title': 'All Game', 'games': games}
    return render_template("admin/all_game.html", **templateData)


@app.route('/admin/work')
def work():
    return render_template("admin/work.html", session=session)


###############################################################################
#                                                                             #
#                                                                             #
#                                 USER PANNEL                                 #
#                                                                             #
#                                                                             #
###############################################################################
#############################################
#                 SIGNUP USER               #
#############################################
@app.route("/signup", methods=['POST'])
def add_user():
    try:
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password)
        passw = bcrypt.check_password_hash(pw_hash, password)
        mdb.add_user(username, name, email, pw_hash)
        print('User is added successfully')
    except Exception as exp:
        print('add_user() :: Got exception: %s' % exp)
        print(traceback.format_exc())
    return render_template('/user/login.html', session=session)


#############################################
#                 LOGIN ADMIN               #
#############################################
@app.route('/admin_login', methods=['POST'])
def admin_login():
    ret = {'err': 0}
    try:

        sumSessionCounter()
        email = request.form['email']
        password = request.form['password']

        if mdb.admin_exists(email, password):
            name = mdb.get_name(email)
            session['name'] = name
            expiry = datetime.datetime.utcnow() + datetime.\
                timedelta(minutes=30)
            token = jwt.encode({'user': email, 'exp': expiry},
                               app.config['secretkey'], algorithm='HS256')
            ret['msg'] = 'Login successful'
            ret['err'] = 0
            ret['token'] = token.decode('UTF-8')
            return render_template('admin/admin.html', session=session)
        else:
            templateData = {'title': 'singin page'}
            # Login Failed!
            return render_template('admin/admin.html', **templateData)
            # return "Login faild"
            ret['msg'] = 'Login Failed'
            ret['err'] = 1

    except Exception as exp:
        ret['msg'] = '%s' % exp
        ret['err'] = 1
        print(traceback.format_exc())
        # return jsonify(ret)
        return render_template('admin/admin_login.html', session=session)


#############################################
#                 LOGIN USER                #
#############################################
@app.route('/login', methods=['POST'])
def login():

    ret = {'err': 0}
    try:

        sumSessionCounter()
        email = request.form['email']
        password = request.form['password']

        pw_hash = mdb.get_password(email)
        print 'password in server, get from db class ', pw_hash
        passw = bcrypt.check_password_hash(pw_hash, password)

        if passw == True:
            name = mdb.get_name(email)
            # name = mdb.get_name(email)
            session['name'] = name
            # session['email'] = email

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
            return render_template('/user/login.html', **templateData)

            ret['msg'] = 'Login Failed'
            ret['err'] = 1

    except Exception as exp:
        ret['msg'] = '%s' % exp
        ret['err'] = 1
        print(traceback.format_exc())
    # return jsonify(ret)
    return render_template('user/user.html', session=session)


###########################################
#          session logout                 #
###########################################
@app.route('/clear')
def clearsession():
    session.clear()
    return render_template('/user/user.html', session=session)
    # return redirect(request.form('/signin'))


@app.route('/clear1')
def clearsession1():
    session.clear()
    return render_template('admin/admin_login.html', session=session)


#############################################
#                 ROUTING                   #
#############################################
@app.route('/user/')
def user1():
    return render_template("user/user.html", session=session)


@app.route('/user/home')
def user_home():
    return render_template("user/user.html", session=session)


@app.route('/admin/get_current_game')
def get_current_game():
    game = mdb.get_user_game()
    ret = []
    item = {}
    item['eyes'] = game['eyes']
    item['pic'] = game['pic']
    item['_id'] = game['_id']
    item['ball'] = game['ball']
    return JSONEncoder().encode({'game': item})


@app.route('/user/playgame')
def playgame():
    game = mdb.get_user_game()
    print ("game: %s" % game)
    templateData = {'title': 'playgame', 'game': game}
    return render_template("user/game.html", session=session, **templateData)


@app.route('/save_user_ball_position', methods=['POST'])
def get_ball_posisave_user_ball_positiontion():
    try:
        game_id = request.form['game_id']
        user = request.form['user']
        ball_x = request.form['ball_x']
        ball_y = request.form['ball_y']
        mdb.save_user_ball_position(game_id, user, ball_x, ball_y)
    except Exception as exp:
        print "save_user_ball_position() :: Got exception: %s" % exp
        print(traceback.format_exc())
    return render_template("user/save_game.html", session=session)


@app.route('/get_all_pos', methods=['POST'])
def get_all_pos():
    try:
        game_id = request.form['game_id']
        mdb.get_result()
    except Exception as exp:
        print "get_all_pos() :: Got exception: %s" % exp
        print(traceback.format_exc())
    return "json"


@app.route('/user/game_result')
def result1():
    return render_template("user/game_result.html", session=session)


@app.route('/user/work')
def work1():
    return render_template("user/work.html", session=session)


@app.route('/user/signup')
def user_signup():
    return render_template("user/signup.html", session=session)


@app.route('/user/login')
def user_login():
    return render_template("user/login.html", session=session)


if __name__ == '__main__':
    app.run(debug=True)
