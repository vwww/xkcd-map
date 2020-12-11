# Generates the list of available tiles

from os import listdir
from os.path import isfile, join
import json

mypath = 'converted'
returned = {}

for f in listdir(mypath):
	if isfile(join(mypath,f)):
		f = f.split('-', 1)
		if f[0] not in returned:
			returned[f[0]] = []
		returned[f[0]].append(f[1][:-4])

with open("converted.js", "w") as f:
	f.write('var available=')
	f.write(json.dumps(returned, separators=(',',':')))
	#f.write(';')
