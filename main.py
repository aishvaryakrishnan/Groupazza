import flask
import urllib2
from cookielib import CookieJar
from flask import Flask, render_template, request, url_for
import json

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))


# Create the application.
APP = Flask(__name__)

@APP.route('/')
def index():
    return flask.render_template('index.html')

@APP.route('/login')
def login():
    return flask.render_template('login.html')

@APP.route('/submit/', methods=['POST'])
def submit():
    email = request.form["email"]
    password = request.form["password"]

    # login to Piazza.
    login_url = 'https://piazza.com/logic/api?method=user.login'
    login_data = '{"method":"user.login","params":{"email":"'+email+'","pass":"'+password+'"}}'

    login_resp = opener.open(login_url, login_data)

    info = json.loads(login_resp.read())

    #render dashboard
    if info:
       return render_template('dashboard.html', info=info)
    else:
       return render_template('chat.html', info="Error!"+ info)

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

if __name__ == '__main__':
    APP.debug=True
    APP.run()
