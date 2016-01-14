import json
import random

names = ["Imran", "Afiq", "Amier", "Hassan", "Fawwaz", "Naufal", "Amin", "Hafizul", "Hazwan", "Fiqri", "Arif", "Faris", "Eddy", "Afzym"]
titles = ["Cinta Rasulullah", "Solat", "Zakat", "Haji", "Beriman dengan Malaikat", "Sirah", "Dakwah", "Purification of the Heart", "Khilafah Uthmaniyah", "Puasa"]

if __name__=="__main__":
	
	speakrs = []
	for name in names:
		speakrs.append({
			"name" : name, 
			"title" : titles[int(random.random()*len(titles))]
			})

	ret = dict({"speakrs":speakrs})
	ret = json.dumps(ret, indent=4)
	print ret
	speakr_file = open("speakrs.json", "w")
	speakr_file.write(ret)