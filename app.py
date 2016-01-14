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

bottle.run(host='0.0.0.0', port=argv[1])
