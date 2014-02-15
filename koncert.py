#!/usr/bin/python2
# -*- coding: utf-8 -*-


import urllib
import string
import event


#sock = urllib.urlopen("http://www.koncert.hu/koncertek#kozeli:1")
#content = sock.readlines()
#sock.close()

file = open('downloaded_koncert.html','rt')
content = file.readlines()
file.close()


esemenyek = list()

for index in range(0,len(content)):
	line = content[index]
	if line.find('concertlistitem')>1:
		pic = ''
		date = ''
		name = ''
		eloado = ''
		varos = ''
		place = ''
		line2 = content[index+1]
		if line2.find('eventpic')>1:
			pic = line2[line2.find('<img src=\"http://')+9:line2.find('.jpg')+4]
			#print "Kep = "+pic
			line2 = content[index+3]
		if line2.find('eventdate')>1:
			line2 = content[index+4]
			year = line2[line2.find('<div class="year">')+len('<div class="year">'):line2.find('</div>')]
			line2 = content[index+5]
			month = line2[line2.find('<div class="month">')+len('<div class="month">'):line2.find('</div>')-1]
                        line2 = content[index+6]
			day = line2[line2.find('<div class="day">')+len('<div class="day">'):line2.find('</div>')]
			date=year+'-'+month+'-'+day
			line2 = content[index+10]
		if line2.find('eventinfo')>1:
			line2 = content[index+12]
			name = line2[line2.rfind('\">')+2:line2.find('</a></h2></div>')]
			line2 = content[index+14]
		if line2.find('evntartists')>1:
			line2=unicode(line2,"utf-8");
			eloado = line2[line2.find('<div class=\"evntartists\"><h3>')+len('<div class=\"evntartists\"><h3>'):line2.find('</h3></div>')].split(',')
			line2 = content[index+15]
		if line2.find('place')>1:
			sub1_line2=line2[0:line2.find('</a>')]
			varos=sub1_line2[sub1_line2.rfind('\">')+2:]
			sub2_line2=line2[sub1_line2.rfind('\">')+10:]	
			place=sub2_line2[sub2_line2.find('\">')+2:sub2_line2.rfind('</a></div>')]
		


		events=list()
	
		event = event.Event(name)
		#event.setDate(year+'-'+month+'-'+day)
		print "DATE:'"+date+"'"
		#event.setLocation(("city:"+varos))
		for artist in eloado:
			event.addArtist(artist.strip())
		events.append(event)





		if len(date)>1 and len(name)>1 and len(place)>1:
			print "__________________________________"
			print "Esemény: " + name
			print "Időpont: " + date
			print "Előadó: "
			for el in eloado:
				print "\t"+el.encode("utf-8").strip()
			print "Helyszín: " + varos + '\n\t\t' + place
