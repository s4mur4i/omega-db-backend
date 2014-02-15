#!/usr/bin/python2
# -*- coding: utf-8 -*-


class Event:

	global artists
	artists = list()
	
	def __init__(self, name):
		self.name = name

	def getName():
		return self.name

	def setDate(date):
		self.date = date

	def getDate():
		return self.date

	def addArtist(self, name):
		artists.append(name)

	def getArtists():
		return self.artists

	def setLocation(string):
		if string.find('gps:')>1:
			#gps:47.5229137,19.0564539
			lat=string[string.find('gps:')+4:string.find(',')]
			lon=string[string.find(',')+1:]
			setGps(lat,lon)
		elif string.find('city:')>1:
			#city:Budapest
			setCity(string[5:])
			
	def setGps(lat,lon):
		self.lat=lat
		self.lon=lon
	
	def setCity(CityName):
		self.city=CityName

	def getGps():
		return self.lat+','+self.lon

	def getCity():
		return self.city

	def __str__(self):
		return_str="Name: "+getName()
		return_str+="Date: "+getDate()
		return_str+="City: "+getCity()
		

