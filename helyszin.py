#!/usr/bin/python2
# -*- coding: utf-8 -*-


import urllib
import string
import event
import database
import sys
import time

db=database.Db()

print "Dumping place data "

for id in range(1,44):
	url="http://www.koncert.hu/helyszinek#:%d" % id
	print "URL="+url
	sock=""
	sock = urllib.urlopen(url)
	content = ""
	content = sock.readlines()

	#file = open('downloaded_koncert.html','rt')
	#content = file.readlines()
	#file.close()

	for index in range(0,len(content)):
		line = content[index]
		name = ''
		city = ''
		if line.find('smallboxlistitem')>1:
			line2 = content[index+3]
			if line2.find('smallboxname')>1:
				name = line2[line2.rfind('\">')+2:line2.find('</a></h2></div>')]
				line2 = content[index+4]
			if line2.find('smallboxsub') and line2.find('</b>'):
				city = line2[line2.find('<b>')+3:line2.find('</b>')]

			print "Add "+name.strip()+" place to database"
			#addPlace(name, url, lat, lon, addrr, email, tel):
			db.addPlace(name.strip(), "", "", "", city.strip(), "", "")
	sock.close()
	time.sleep(60)



