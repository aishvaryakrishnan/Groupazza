import flask
import urllib2
from flask import Flask, render_template, request, url_for
import json
from firebase import firebase
from piazza_api import Piazza
import urllib
import simplejson as json

p = Piazza()
user_login = ""

fb = firebase.FirebaseApplication('https://fpr-app.firebaseio.com/', None)

# Create the application.
APP = Flask(__name__)

user_id = ""

@APP.route('/')
def index():
    return flask.render_template('index.html')

@APP.route('/login')
def login():
    return flask.render_template('login.html')

@APP.route('/submit', methods=['POST'])
def submit():
    email = request.form["email"]
    password = request.form["password"]

    global user_login
    user_login = p.user_login(email=email, password=password)
    user_info = p.get_user_profile()

    #render dashboard
    if user_info:
        new_user = { "user": user_info["email"], "p_user_id": user_info["user_id"], "classes": user_info["all_classes"]}
        result = fb.post('/users', new_user)
        user_id = new_user["p_user_id"]
        return render_template('dashboard.html', result=new_user)
    if info:
       return render_template('chat.html', info=info)
    else:
       return render_template('dashboard.html', info="Error!")

@APP.route('/new_chat')
def dash():
    users = json.loads(json.dumps(fb.get('/users', None)))
    u = ""
    mlist = []
    for user in users:
        for u in users[user]:
            if u == "classes":
              mlist.append(users[user][u])
             # class1 = p.network(mlist[0])
    li = []
    for index, item in enumerate(mlist):
        if isinstance(item, dict):
            for key in item:
                for i in item[key]:
                    if "name" == i:
                        li.append(item[key][i])


    return flask.render_template('new_chat.html', result=li)





if __name__ == '__main__':
    APP.debug=True
    APP.run()
