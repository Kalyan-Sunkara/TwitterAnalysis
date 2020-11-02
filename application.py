import os
from flask import Flask, session, request, redirect, render_template
from flask_socketio import SocketIO, emit
from flask_session import Session
import tweepy
import tweet
import json
import uuid

application = Flask(__name__)
application.config['SECRET_KEY'] = os.urandom(64)
application.config['SESSION_TYPE'] = 'filesystem'
application.config['SESSION_FILE_DIR'] = './.flask_session/'
socketio = SocketIO(application)

Session(application)

@application.route('/', methods=['GET','POST'])
def home():
    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4())
        twitter = twitterBot()
        session['twitter'] = twitter

    return render_template("home.html")

@application.route('/search')
def rate():
    return "search"

@application.route('/results')
def results():
    if not session.get('uuid'):
        return redirect('/')
    return "results"

if __name__ == '__main__':  # Script executed directly?
    application.run()
#
# @socketio.on('disconnect')
# def disconnect_user():
#     session.clear()
