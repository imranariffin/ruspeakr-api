import json
import random

names = ["Imran", "Afiq", "Amier", "Hassan", "Fawwaz", "Naufal", "Amin", "Hafizul", "Hazwan", "Fiqri", "Arif", "Faris", "Eddy", "Afzym"]
titles = ["Cinta Rasulullah", "Solat", "Zakat", "Haji", "Beriman dengan Malaikat", "Sirah", "Dakwah", "Purification of the Heart", "Khilafah Uthmaniyah", "Puasa"]

if __name__=="__main__":
	
	# create random speakrs
	speakrs = []
	_id = 1
	for name in names:
		speakrs.append({
			"name" : name,
			"talks" : [int(random.random()*len(titles))+1],
			"_id"	: _id
			})
		_id += 1

	ret = dict({"speakrs":speakrs})
	ret = json.dumps(ret, indent=4)
	print ret
	speakrs_file = open("speakrs.json", "w")
	speakrs_file.write(ret)

	# create random talks
	talks = []
	_id = 1
	for title in titles:
		talks.append({
			"title" : title,
			"_id"	: _id,
			"rating" : 0
			})
		_id += 1

	ret = dict({"talks":talks})
	ret = json.dumps(ret, indent=4)
	print ret
	talks_file = open("talks.json", "w")
	talks_file.write(ret)