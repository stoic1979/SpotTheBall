from flask import Flask, request, render_template
import traceback
from db import Mdb
import json
app = Flask(__name__)
mdb = Mdb()


@app.route('/')
def home():
    return 'Welcome to Spot The Ball'

@app.route('/admin')
def admin():
    templateData = {'title': 'admin'}
    return render_template("admin.html", **templateData)


@app.route('/add_game', methods=['POST'])
def add_game():
    ret = {}
    try:
        pic = request.form['pic']
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
    return json.dumps(ret)


@app.route("/get_game", methods=['GET'])
def get_game():
    return mdb.get_game()


if __name__ == '__main__':
    app.run(debug=True)
