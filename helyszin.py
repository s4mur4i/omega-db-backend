#!/usr/bin/python2
# -*- coding: utf-8 -*-


import urllib
import string
import event
import database
import sys
import time
from geopy import geocoders
from decimal import Decimal
from xml.dom import minidom
from BeautifulSoup import BeautifulSoup

db=database.Db()

print "Dumping place data "

for id in range(40,44):
#	url="http://www.koncert.hu/helyszinek#:%d" % id
#	print "URL="+url
#	sock=""
#	sock = urllib.urlopen(url)
#	content = ""
#	content = sock.readlines()
	
	file_url="downloaded_helyszinek%d.html" % id

	file = open(file_url,'rt')
	content = file.readlines()
	file.close()

	print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>"+file_url+"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
	for index in range(0,len(content)):
		line = content[index]
		name = ''
		city = ''
		if line.find('smallboxlistitem')>1:
			line2 = content[index+3]
			if line2.find('smallboxname')>1:
				name = line2[line2.rfind('\">')+2:line2.find('</a></h2></div>')]
				name = name.replace("&amp;","&")
				line2 = content[index+4]
			if line2.find('smallboxsub') and line2.find('</b>'):
				city = line2[line2.find('<b>')+3:line2.find('</b>')]
				city = city[0:city.find(" ")]

#				city = city.replace("<spen style=\"text-transform:uppercase\">(fr)</spen>","",1)
#				city = city.replace("<spen style=\"text-transform:uppercase\">(sk)</spen>","",1)

			addr=name+", "+city.strip()+", HU"
	
			if name.find(" - ")>1:
				addr=name[0:name.find(' - ')]+", "+city.strip()+", HU"

			if name.find("(")>1:
				addr=name[0:name.find("(")]+", "+city.strip()+", HU"

			if not city.find('dapest')>1:
				addr=name+", "+city.strip()

			lat,lng = 0.0,0.0
			url = 'https://maps.googleapis.com/maps/api/geocode/xml?address=' + urllib.quote(addr) + '&sensor=false&key=AIzaSyBD9GNHorbYXWYX5mS9OC-CzUHQyw_PfO0'
			print "Query google for lat, long '%s'" % (addr)
			xml = BeautifulSoup(urllib.urlopen(url).read())
			
			status="%s" % xml.geocoderesponse.status
			status=status[8:status.rfind("<")]
			print "Status=%s" % status

			if status=='ZERO_RESULTS':
				url = 'https://maps.googleapis.com/maps/api/geocode/xml?address=' + urllib.quote(city.strip()) + '&sensor=false&key=AIzaSyBD9GNHorbYXWYX5mS9OC-CzUHQyw_PfO0'
	                        xml = BeautifulSoup(urllib.urlopen(url).read())
				addr = city.strip()

				status="%s" % xml.geocoderesponse.status
	                        status=status[8:status.rfind("<")]

				if not status=='ZERO_RESULTS':
					lat = "%s" % xml.geocoderesponse.result.geometry.location.lat
        	                        lat = lat[5:lat.rfind('<')]
                	                lng = "%s" % xml.geocoderesponse.result.geometry.location.lng
                        	        lng = lng[5:lng.rfind('<')]
			else:
		
				addr = "%s" % (xml.geocoderesponse.result.formatted_address)
				addr = addr[addr.find(',')+1:addr.rfind('<')]
				addr = addr.strip()

				if len(addr)<10:
					addr = city.strip()

				lat = "%s" % xml.geocoderesponse.result.geometry.location.lat
				lat = lat[5:lat.rfind('<')]
				lng = "%s" % xml.geocoderesponse.result.geometry.location.lng
				lng = lng[5:lng.rfind('<')]


			print "Location: %s,%s" % (lat,lng)
			print "Addr: %s" % (addr)
			if name.find('\'')>1:
                        	name=name.replace('\'','').replace("'","").replace(chr(37),"")
				print "TALALAT"+name
			print "Add "+name.strip()+" place to database"
			#addPlace(name, url, lat, lon, addrr, email, tel):
			db.addPlace(name.strip(), "",lat, lng, addr, "", "")
	#sock.close()



