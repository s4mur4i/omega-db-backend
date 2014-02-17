#!/usr/bin/python2
# -*- coding: utf-8 -*-


import urllib
import string
import event
import database
import sys
import time

honapok = {"jan":1,"febr":2,"márc":3,"ápr":4,"máj":5,"jún":6,"júl":7,"aug":8,"szept":9,"okt":10,"nov":11,"dec":12}
db=database.Db()
#db.init()

sys.stdout.write("Dumping data from koncert.hu ")
for id in range(1,5):
#	url="http://www.koncert.hu/koncertek#kozeli:%d" % id
#	print "URL:"+url
#	sock = urllib.urlopen(url)
#	content = sock.readlines()
#	sock.close()
	f_url="downloaded_koncert%d.html" % id
	print "File="+f_url
	file = open(f_url,'rt')
	content = file.readlines()
	file.close()

	for index in range(0,len(content)):
		sys.stdout.write('.')
		line = content[index]
		if line.find('concertlistitem')>1:
			sys.stdout.write('*')
			pic = ''
			date = ''
			name = ''
			eloado = ''
			varos = ''
			place = ''
			line2 = content[index+1]
			sys.stdout.write('.')
			if line2.find('eventpic')>1:
				sys.stdout.write('.')
				pic = "http://www.koncert.hu/"+line2[line2.find('<img src=\"')+10:line2.find('.jpg')+4]
				line2 = content[index+3]
			if line2.find('eventdate')>1:
				sys.stdout.write('.')
				line2 = content[index+4]
				year = line2[line2.find('<div class="year">')+len('<div class="year">'):line2.find('</div>')]
				line2 = content[index+5]
				month = line2[line2.find('<div class="month">')+len('<div class="month">'):line2.find('</div>')-1]
		                line2 = content[index+6]
				day = line2[line2.find('<div class="day">')+len('<div class="day">'):line2.find('</div>')]
				date="%04d-%02d-%02d 00:00:00" % (int(year), int(honapok[month]), int(day))
				line2 = content[index+10]
			if line2.find('eventinfo')>1:
				sys.stdout.write('.')
				line2 = content[index+12]
				name = line2[line2.rfind('\">')+2:line2.find('</a></h2></div>')]
				line2 = content[index+14]
			if line2.find('evntartists')>1:
				sys.stdout.write('.')
				line2=unicode(line2,"utf-8");
				eloado = line2[line2.find('<div class=\"evntartists\"><h3>')+len('<div class=\"evntartists\"><h3>'):line2.find('</h3></div>')].split(',')
				line2 = content[index+15]
			if line2.find('place')>1:
				sys.stdout.write('.')
				sub1_line2=line2[0:line2.find('</a>')]
				varos=sub1_line2[sub1_line2.rfind('\">')+2:]
				sub2_line2=line2[sub1_line2.rfind('\">')+10:]	
				place=sub2_line2[sub2_line2.find('\">')+2:sub2_line2.rfind('</a></div>')]
			print ""

			for artist in eloado:
				sys.stdout.write("Adding '"+artist.strip()+"' artist to database = ")
				db.addArtist(artist.strip())

			sys.stdout.write("Adding "+place+" place to database = ")
			#addPlace(name, url, lat, lon, addrr, email, tel):
			db.addPlace(place, "", "", "", varos, "", "")
			db.addCategory("Koncert")
			sys.stdout.write("Adding event "+name+" = ")
			db.addEvent(name, db.getPlaceId(place), pic, "", date, 1, 18)

			sys.stdout.write("Pairing artists and events = ")
			for artist in eloado:
				sys.stdout.write('.')
				db.addEventArtist(db.getEventId(place,date,name),db.getArtistId(artist))
			print ""
