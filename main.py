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
       return render_template('dashboard.html', info=cj)
    else:
       return render_template('dashboard.html', info="Error!"+ info)

@APP.route('/dashboard')
def dash():
    flask.render_template('dashboard.html')

    content_url = 'https://piazza.com/logic/api?method=user.user_info'
    content_data = '{"method":"content.get"'
    content_resp = opener.open(content_url, content_data)
    user = content_resp.read()



if __name__ == '__main__':
    APP.debug=True
    APP.run()
