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
fire_user_id = ""

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
        user_info["all_classes"]["group"]=["CS fun group","Discrete math group", "Adv. operating group"]
        new_user = { "user": user_info["email"], "p_user_id": user_info["user_id"], "classes": user_info["all_classes"]}
        result = fb.post('/users', new_user)
        user_id = new_user["p_user_id"]
        users = json.loads(json.dumps(fb.get('/users', None)))
        u = ""
        mlist = []
        users1 = json.loads(json.dumps(fb.get('/users', fire_user_id)))
        classes = ""
        li = []
        if users1:
            for class1 in users1:
                if 'classes' in users[class1]:
                    classes = users[class1]['classes']['group']
            for user in users:
                global fire_user_id
                fire_user_id = user
                for u in users[user]:
                    if u == "classes":
                        mlist.append(users[user][u])
                 # class1 = p.network(mlist[0])
            for index, item in enumerate(mlist):
                if isinstance(item, dict):
                    for key in item:
                        for i in item[key]:
                            if "name" == i:
                                li.append(item[key][i])
        return render_template('dashboard.html', user=new_user, courses=li, u_classes=classes)

@APP.route('/new_chat')
def dash():
    users = json.loads(json.dumps(fb.get('/users', fire_user_id)))
    classes = []
    for class1 in users:
        for class2 in users[class1]['classes']:
            classes.append(users[class1]['classes'][class2]['group'])


    return flask.render_template('new_chat.html', result=classes)


@APP.route('/dashboard/', methods=['POST'])
def dashboard():
    return flask.render_template('dashboard.html')

@APP.route('/chat/', methods=['POST'])
def chat():
    return flask.render_template('chat.html')

@APP.route('/create/', methods=['POST'])
def create():
    # returns some action that updates chat.html
    pass

@APP.route('/statistics/', methods=['POST'])
def statistics():
    return flask.render_template('statistics.html')

if __name__ == '__main__':
    APP.debug=True
    APP.run()
