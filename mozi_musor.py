#!/usr/bin/python2
# -*- coding: utf-8 -*-


import urllib
import string
from datetime import date, timedelta
import sys
import database




sys.stdout.write("Open database")
db=database.Db()
print " ... Done"

for single_date in (date.today() + timedelta((26+n)) for n in range(30)):
	url="http://port.hu/pls/ci/cinema.list_days?i_city_id=3372&i_county_id=1&i_country_id=44&i_dist_id=-1&i_time_intervall=0&i_selected_date=%s-%s&i_view_date=2014-04-01-2014-04-30"% (single_date,single_date)
        sys.stdout.write("Opening url")	
        sock = urllib.urlopen(url)
        content = sock.readlines()
        sock.close()
	print " ... Done"
	sys.stdout.write("Dumping data ")
	for index in range(0,len(content)):
		line=content[index]
		place=0
                sys.stdout.write(".")
		if line.find("itemscope itemtype=\"http://schema.org/Event\"")>2:
			sys.stdout.write("*")
			substr=line[line.find("<a itemprop=\"url\" class=\"e_title1 event"):line.find("</a>")]
			event=substr[substr.find(">")+1:]
			substr=line[line.find('itemprop=\"startDate\" content=\"'):line.find('\"/></td><td class=\"e_title_box1\"')]
			besorolas=line[line.rfind('img alt=\"(')+10:line.rfind(')\" title')]
			ido=substr[substr.find('T')+1:substr.find('\"/>')].split(':')
			ora=ido[0]
			perc=ido[1]
			perc=int(perc)
			if perc<10:
				perc=perc*10
			event_date="%s %s:%02d:00" % (single_date,ora,perc)

			line = content[index+1];
			event_place=line[line.find('=\">')+3:line.rfind('</a>')]
                        place=db.getPlaceId(unicode(event_place,'iso-8859-2'))
			try:
                                event=unicode(event,'iso-8859-2')
                        except:
                                print "Unicode error"

			if place<1:
				#                        #db.addPlace(place, "", "", "", varos, "", "")
				print "NINCS ilyen hely az adatbazisban: "+event_place
				if event_place=="Corvin Budapest Filmpalota":
					event_place="Corvin"
					place=db.getPlaceId(unicode(event_place,'iso-8859-2'))
				else:
				        print "NINCS ilyen hely az adatbazisban: "+event_place
	                db.addEvent(event, place, "", "", event_date, 2, besorolas)
			print ""	
			print " ... Done"

