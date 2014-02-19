#!/usr/bin/python2
# -*- coding: utf-8 -*-


import string
import database
import urllib
from BeautifulSoup import BeautifulSoup
import sys
from decimal import *



db=database.Db()

for id in range(1,8):
	f_url="mozi%d.html" % id
	print "File="+f_url
	file = open(f_url,'rt')
	content = file.readlines()
	file.close()

	for index in range(0,len(content)):
		line = content[index]
		if line.find('class=\"navs\"')>1:
			name=unicode(line[line.find("target=\"_top\">")+14:line.find("</a>")].strip(),'ISO-8859-2')
			name = name.encode('utf-8').replace(chr(39),"")
			print "Mozi neve: %s" % (name)
			line2=content[index+4]
			addr=unicode(line2.replace('<span class=\"btxt\">','').replace('</span>','').strip(),'ISO-8859-2')
			print "Mozi cime:%s" % (addr)
		


			url = 'https://maps.googleapis.com/maps/api/geocode/xml?address=' + urllib.quote(addr.encode('utf-8')) + '&sensor=false&key=AIzaSyBD9GNHorbYXWYX5mS9OC-CzUHQyw_PfO0'
			if not db.placeExistByName(name):
				lat,lng = 0.0,0.0
				print "Query google for lat, long '%s'" % (addr)
				xml = BeautifulSoup(urllib.urlopen(url).read())
			
				status="%s" % xml.geocoderesponse.status
				status=status[8:status.rfind("<")]
				print "Status=%s" % status

				if status=='OK':
					lat = "%s" % xml.geocoderesponse.result.geometry.location.lat
					lat = lat[5:lat.rfind('<')]
					lng = "%s" % xml.geocoderesponse.result.geometry.location.lng
					lng = lng[5:lng.rfind('<')]
				print "_______________________________________________________________"
				print "Location: %s,%s" % (lat,lng)
				print "Addr: %s" % (addr)
				sys.stdout.write('Adding to database .. ')		
				#addPlace(self,name, url, lat, lon, addrr, email, tel):
				db.addPlace(name,"",lat,lng,addr,"","")
			else:
				print "Place %s exist in database SKIP from process" % (name)
				id = int(db.getPlaceId(name))
				sql="SELECT lat,lon FROM Place WHERE id=%d" % (id)
				row =  db.runQuery(sql)[0]
				db_lat=row[0]
				db_lon=row[1]
				print "Location in db LAT=%s, LON=%s" % (db_lat,db_lon)
			
				if Decimal(db_lat)<1.0 and Decimal(db_lon)<1.0:
					print "Cooridnates need to be upgrade !"
					print "Query google for lat, long '%s'" % (addr)
					xml = BeautifulSoup(urllib.urlopen(url).read())
	                                status="%s" % xml.geocoderesponse.status
        	                        status=status[8:status.rfind("<")]
                	                print "Status=%s" % status
					if status=='OK':
						lat = "%s" % xml.geocoderesponse.result.geometry.location.lat
	                                        lat = lat[5:lat.rfind('<')]
        	                                lng = "%s" % xml.geocoderesponse.result.geometry.location.lng
                	                        lng = lng[5:lng.rfind('<')]
						sys.stdout.write('Update database .. ')
						sql="UPDATE Place SET lat=%s, lon=%s WHERE id=%d" % (lat,lng,id)
						print "\n%s" % (sql)
						db.runQuery(sql)
						
			print "__________________________________________________________"
			print ""


