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
from flask_login import login_user, login_required, logout_user, current_user

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


@app.route('/admin')
def home():
    templateData = {'title': 'admin home'}
    return render_template("admin/admin_login.html", **templateData)


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
        ball_x = request.form['ball_x']
        ball_y = request.form['ball_y']

        bg_img = request.form['bgImg']

        mdb.add_game(bg_img, x1, y1, x2, y2,
                     x3, y3, x4, y4, ball_x, ball_y)
        ret['error'] = 0
        ret['msg'] = 'Game is stored successfully'
    except Exception as exp:
        ret['error'] = 1
        ret['msg'] = exp
        print(traceback.format_exc())
    tmpl_data = {'status': ret}
    return render_template('admin/game_saved.html', **tmpl_data)


###########################################
#                 get game                #
###########################################
@app.route('/save_ball_position')
def save_ball_position():
    return mdb.save_ball_position()


###############################################################################
#                                                                             #
#                                                                             #
#                                 ADMIN PANNEL                                #
#                                                                             #
#                                                                             #
###############################################################################
@app.route('/admin_login/')
def admin1():
    templateData = {'title': 'admin home'}
    return render_template("admin/admin_login.html", **templateData)


@app.route('/admin/test_page')
def test_page():
    templateData = {'title': 'admin home'}
    return render_template("admin/test_page.html", **templateData)


@app.route('/admin/home')
def admin():
    templateData = {'title': 'admin home'}
    return render_template("admin/admin.html", **templateData)


@app.route('/admin/add_game_img')
def add_game_img():
    templateData = {'title': 'Add game image'}
    return render_template("admin/add_game_img.html", **templateData)

@app.route('/admin/create_game1111')
def create_game():
    templateData = {'title': 'create game'}
    return render_template("admin/create_game.html", **templateData)


@app.route('/admin/game_result')
def result():
    templateData = {'title': 'game result'}
    return render_template("admin/game_result.html", **templateData)


@app.route('/admin/work')
def work():
    templateData = {'title': 'how it work'}
    return render_template("admin/work.html", **templateData)


@app.route('/admin/login', methods=['POST'])
def admin_login():
    email = request.form['email']
    password = request.form['password']
    templateData = {'title': 'admin_dashboard'}
    return render_template("works.html", **templateData)


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
        templateData = {'title': 'Signup Page'}
    except Exception as exp:
        print('add_user() :: Got exception: %s' % exp)
        print(traceback.format_exc())
    return render_template('/user/login.html', session=session)


#############################################
#                 LOGIN ADMIN                #
#############################################
@app.route('/login1', methods=['POST'])
def login1():

    ret = {'err': 0}
    try:
        email = request.form['email']
        password = request.form['password']
        mail = 'tom@gmail.com'
        pswd = '123'
        # pw_hash = mdb.get_password(email)
        # print 'password in server, get from db class ', pw_hash
        # passw = bcrypt.check_password_hash(pw_hash, password)

        if email == mail and password == pswd:
            # return 'login successfull'
            return render_template('admin/admin.html', session=session)
        else:
            return render_template('admin/admin_login.html', session=session)
            # return 'login failed'


    except Exception as exp:
        ret['msg'] = '%s' % exp
        ret['err'] = 1
        print(traceback.format_exc())
        # return jsonify(ret)



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
    return render_template('admin/admin_login.html', session=session)


#############################################
#                 ROUTING                   #
#############################################
@app.route('/user/')
def user1():
    templateData = {'title': 'user home'}
    return render_template("user/user.html", session=session)


@app.route('/user/home')
def user_home():
    templateData = {'title': 'user home'}
    return render_template("user/user.html", session=session)


@app.route('/user/playgame')
def playgame():
    templateData = {'title': 'playgame'}
    return render_template("user/game.html", session=session)


@app.route('/user/game_result')
def result1():
    templateData = {'title': 'result'}
    return render_template("user/game_result.html", session=session)


@app.route('/user/work')
def work1():
    templateData = {'title': 'work'}
    return render_template("user/work.html", session=session)


@app.route('/user/signup')
def user_signup():
    templateData = {'title': 'signup'}
    return render_template("user/signup.html", session=session)


@app.route('/user/login')
def user_login():
    templateData = {'title': 'login'}
    return render_template("user/login.html", session=session)


if __name__ == '__main__':
    app.run(debug=True)
