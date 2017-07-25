import os
from flask import Flask, request, render_template, redirect, send_from_directory, url_for, flash
import traceback
from werkzeug.utils import  secure_filename
from db import Mdb
import json
app = Flask(__name__)
mdb = Mdb()


@app.route('/')
def home():
    return 'Welcome to Spot The Ball'

#########################################
#              upload Image             #
#########################################
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = '%s/%s' % (dir_path, 'img')

UPLOAD_FOLDER = file_path
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/admin')
def admin():
    templateData = {'title': 'admin'}
    return render_template("admin.html", **templateData)


@app.route('/add_game', methods=['POST'])
def add_game():
    ret = {}
    try:
        file = request.files['pic']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pic = '%s/%s' % (file_path, filename)

            # return redirect(url_for('uploaded_file', filename=filename))

        x1 = request.form['x1']
        y1 = request.form['y1']
        x2 = request.form['x2']
        y2 = request.form['y2']
        x3 = request.form['x3']
        y3 = request.form['y3']
        x4 = request.form['x4']
        y4 = request.form['y4']
        x = request.form['x']
        y = request.form['y']
        mdb.add_game(pic, x1, y1, x2, y2, x3, y3, x4, y4, x, y)
        ret['error'] = 0
        ret['msg'] = 'Game is stored successfully'
    except Exception as exp:
        ret['error'] = 1
        ret['msg'] = exp
        print(traceback.format_exc())
    # return json.dumps(ret)
    return redirect(url_for('uploaded_file', filename=filename))


@app.route("/get_game", methods=['GET'])
def get_game():
    return mdb.get_game()


if __name__ == '__main__':
    app.run(debug=True)
