import os
from os import environ as env
from sys import argv

from bottle import default_app, request, route, response, get
import json
from pymongo import MongoClient

def __post_login():
	"""
	handles user login, fetch user from db
	if succcessful, return {"status":"1", "user" : user}
	else, return {"status" : "-1", "error":errMessage}
	"""

	response.headers['Content-type'] = 'application/json'

	forms = dict()
	if len(request.forms.keys()) == 1:
		forms = json.loads(request.forms.keys()[0])
	else:
		forms = dict((k,v) for k,v in request.forms.items())

	assert("username" in forms.keys())
	assert("password" in forms.keys())

	forms['loginSuccess'] = "false"

	# add user to db if not yet exist
	client = MongoClient()
	db = client.utdb
	users = db.users
	# add user
	user = dict(forms)
	res = ""
	if users.find_one({"username" : user['username']}) != None:
		print "good: user is in db"
		user['loginSuccess'] = "true"
		res = json.dumps(user)
	else:
		print "err: user not found"
		res = json.dumps({
			"status" : "-1",
			"err" : "user not found"
			})

	client.close()
	return res

def __post_signup():
    response.headers['Content-type'] = 'application/json'
    # collect POST request forms in dict
    if len(request.forms.keys()) == 1:
        forms = json.loads(request.forms.keys()[0])
    else:
        forms = dict((k,v) for k,v in request.forms.items())

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
        return json.dumps({
        	"status" : "-1",
        	"err" : "user oredy in db"
        	})
    else:
        # user not yet in db, insert
        user = forms
        userid = user_collections.insert_one(user).inserted_id
        user['_id'] = str(userid)
        # return user
        return json.dumps({"status":"success", "user":user})

def __get_speakrs():
	# mock
	f_speakrs = open("speakrs.json")
	speakrs = json.loads(f_speakrs.read())['speakrs']

	return speakrs

def __geek():
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
# --------------------------------------------- #
# speakrs api:
# 	ready:
# 		__get_speakrs() 				=> [{speakrs}]
# 		__get_speakr_by_id(speakr_id) 	=> {speakr}
# --------------------------------------------- #

def __get_speakrs_dict():
	f_speakrs = open("./pyscripts/speakrs.json")
	speakrs = json.loads(f_speakrs.read())['speakrs']
	return speakrs

def __get_speakrs():
	# mock
	speakrs = __get_speakrs_dict()
	return json.dumps(speakrs)

def __get_speakr_by_id(speakr_id):
	# mock

	# ASSERTS
	assert(type(speakr_id) == type(int()))

	speakrs = __get_speakrs_dict()
	def find_speakr(speakr):
		if int(speakr['_id']) == speakr_id:
			return True
		return False

	speakrs = __get_speakrs_dict()
	speakrs = filter(find_speakr, speakrs)
	if speakrs != []:
		return speakrs[0]
	else:
		return {}

# --------------------------------------------- #
# speakrs api:
# 	ready:
# 		__get_talks()				=> [{talks}]
# 	todo:
# 		__get_talk_by_id(talk_id)	=> {talk}
# 		__rate_talk() 				=> {status}
# 		__get_talks_by_speakrid		=> [{talks}]
# --------------------------------------------- #

def __get_talks_dict():
	# mock
	f_talks = open("./pyscripts/talks.json")
	talks = json.loads(f_talks.read())['talks']
	return talks

def __get_talks():
	talks = __get_talks_dict()
	return json.dumps(talks)

def __get_talk_by_id(talk_id):
	# ASSERTS
	assert(type(talk_id)==type(int()))

	def find_talk(talk):
		if int(talk['_id']) == talk_id:
			return True
		return False

	talks = __get_talks_dict()
	talk = filter(find_talk, talks)[0]
	return talk

def __get_talks_by_speakrid(speakr_id):
	# ASSERTS
	assert(type(speakr_id) == type(int()))

	talk_ids = map(int, __get_speakr_by_id(speakr_id)['talk_ids'])
	def find_talks(talk):
		if int(talk['_id']) in talk_ids:
			return True
	talks = __get_talks_dict()
	talks =  filter(find_talks, talks)
	print talks
	return json.dumps(talks)

# if __name__=="__main__":
# 	print __get_speakrs()