#!/usr/bin/python2
# -*- coding: utf-8 -*-


import string
import database
import urllib
from BeautifulSoup import BeautifulSoup
import sys



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
			print "Mozi neve: %s" % (name)
			line2=content[index+4]
			addr=unicode(line2.replace('<span class=\"btxt\">','').replace('</span>','').strip(),'ISO-8859-2')
			print "Mozi cime:%s" % (addr)
			
			lat,lng = 0.0,0.0
			url = 'https://maps.googleapis.com/maps/api/geocode/xml?address=' + urllib.quote(addr.encode('utf-8')) + '&sensor=false&key=AIzaSyBD9GNHorbYXWYX5mS9OC-CzUHQyw_PfO0'
			print "Query google for lat, long '%s'" % (addr)
			xml = BeautifulSoup(urllib.urlopen(url).read())
			
			status="%s" % xml.geocoderesponse.status
			status=status[8:status.rfind("<")]
			print "Status=%s" % status

			if not status=='ZERO_RESULTS':
				lat = "%s" % xml.geocoderesponse.result.geometry.location.lat
				lat = lat[5:lat.rfind('<')]
				lng = "%s" % xml.geocoderesponse.result.geometry.location.lng
				lng = lng[5:lng.rfind('<')]


			print "Location: %s,%s" % (lat,lng)
			print "Addr: %s" % (addr)
			sys.stdout.write('Adding to database .. ')		
			#addPlace(self,name, url, lat, lon, addrr, email, tel):
			db.addPlace(name.encode('utf-8').replace(chr(39),""),"",lat,lng,addr,"","")



