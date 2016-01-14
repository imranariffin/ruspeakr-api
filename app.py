#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv

import bottle
from bottle import default_app, request, route, response, get
from pymongo import MongoClient
import json

import api

bottle.debug(True)

def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

@get('/')
def home():
    return "welcome to the official api for rateurspkear!"

@get('/geek')
def geek():
    return api.__geek()

@route
def yo():
    return "yo"

@route('/login', method=["OPTIONS", "POST"])
@enable_cors
def post_login(**user):
    return api.__post_login(**user)

@route('/signup', method=["OPTIONS", "POST"])
@enable_cors
def post_signup():
    return api.__post_signup()

# --------------------------------------------- #
# speakrs api:
#   ready:
#      GET /speakrs
#   todo:
#       POST /me/set-speech-title
#       GET /speakr?id=id
# --------------------------------------------- #

@get('/speakrs')
@enable_cors
def get_speakrs():
    return api.__get_speakrs()

@get('/speakr')
@enable_cors
def get_speakr():
    speakr_id = int(request.query.speakrId)
    return api.__get_speakr_by_id(speakr_id)

# --------------------------------------------- #
# talks api:
#   ready:
#       GET /talks
#       GET /get-talk?talkId=talkId
#   todo:
#       POST /rate?talkId=talkId
# --------------------------------------------- #

@get('/talks')
@enable_cors
def get_talks():
    if request.query.speakrId != "":
        speakr_id = request.query.speakrId
        return api.__get_talks_by_speakrid(int(speakr_id))
    else:
        return api.__get_talks()

@get('/talk')
@enable_cors
def get_talk():
    talkId = int(request.query.talkId)
    return api.__get_talk_by_id(talkId)

bottle.run(host='0.0.0.0', port=argv[1])
