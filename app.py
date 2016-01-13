#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import environ as env
from sys import argv

import bottle
from bottle import default_app, request, route, response, get
from pymongo import MongoClient
import json

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
def index():
    response.content_type = 'text/plain; charset=utf-8'
    ret =  'Hello world, I\'m %s!\n\n' % os.getpid()
    ret += 'Request vars:\n'
    for k, v in request.environ.iteritems():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    ret += '\n'
    ret += 'Environment vars:\n'

    for k, v in env.iteritems():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    return ret

@route
def yo():
    return "yo"

@route('/login', method=["OPTIONS", "POST"])
@enable_cors
def post_login(**user):

    # from customs.usermongo import add_user

    response.headers['Content-type'] = 'application/json'
    res = json.loads(request.forms.keys()[0])
    print res
    print dir(request.POST)
    res['loginSuccess'] = "false"

    # add user to db if not yet exist
    client = MongoClient()
    db = client.utdb
    users = db.users
    # add user
    user = dict(res)
    if users.find_one({"username" : user['username']}) != None:
        print "user oredy in db, dont add"
    else:
        print "user not yet in db, add user"
        print "user:"
        print user
        userid = users.insert_one(user).inserted_id
        user['_id'] = userid.__str__()
        print user
        res = json.dumps(user)

    return json.dumps(res)

@route('/signup', method=["OPTIONS", "POST"])
@enable_cors
def post_signup():
    response.headers['Content-type'] = 'application/json'
    # collect POST request forms in dict
    if len(request.forms.keys()) == 1:
        forms = json.loads(request.forms.keys()[0])
    else:
        forms = dict((k,v) for k,v in request.forms.items())

    # print request.forms.items()
    # forms = dict((k,v) for k,v in request.forms.items())
    # print forms

    # return json.dumps({"status":"yo"})
    # return json.dumps('{"status":"success json loads"}')

    # # add user if not exists yet
    client = MongoClient()
    db = client.utdb
    user_collections = db.users

    # TEST
    assert('username' in forms.keys())

    username = forms['username']
    user = user_collections.find_one({'username':username})
    if user != None:
        # user oredy exist, send err
        return json.dumps({"status" : "failed"})
    else:
        # user not yet in db, insert
        user = forms
        userid = user_collections.insert_one(user).inserted_id
        user['_id'] = str(userid)
        # return user
        return json.dumps({"status":"success", "user":user})

bottle.run(host='0.0.0.0', port=argv[1])
