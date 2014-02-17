#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys

global conn
global c

class Db:
	def __init__(self):
		try:
			self.conn = sqlite3.connect('database.sqlite')
		except:
			print "Can not connect to database"
			sys.exit(-1)
		self.conn.text_factory=str
		self.c = self.conn.cursor()
			

	def init(self):
		conn = sqlite3.connect('database.sqlite')
		c = conn.cursor()
		try:
			self.c.execute('''DROP TABLE Event''')
		except:
		        print "Table Event does not exist can not be DROPed"
		self.c.execute('''CREATE TABLE IF NOT EXISTS Event 
			 (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name varchar COLLATE NOCASE, place_id INTEGER NOT NULL, pic varchar COLLATE NOCASE, url varchar COLLATE NOCASE, date DATETIME DEFAULT CURRENT_TIMESTAMP, category_id INTEGER NULL, besorolas INTEGER NULL)''')

		try: 
			self.c.execute('''DROP TABLE Place''')
		except:
		        print "Table Place does not exist can not be DROPed"
		self.c.execute('''CREATE TABLE IF NOT EXISTS Place
			(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name varchar COLLATE NOCASE UNIQUE ,url varchar COLLATE NOCASE, lat FLOAT, lon FLOAT, addrr varchar COLLATE NOCASE ,email varchar COLLATE NOCASE,tel varchar COLLATE NOCASE)''')

		try:
			self.c.execute('''DROP TABLE Category''')
		except:
			print "Table Category does not exist can not be DROPed"
		self.c.execute('''CREATE  TABLE  IF NOT EXISTS Category ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR COLLATE NOCASE UNIQUE)''')

		try:
			self.c.execute('''DROP TABLE Artist''')
		except:
			print "Table Artist does not exist can not be DROPed"
		self.c.execute('''CREATE  TABLE  IF NOT EXISTS Artist (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR COLLATE NOCASE UNIQUE, url VARCHAR COLLATE NOCASE )''')

		try:
			self.c.execute('''DROP TABLE EventArtist''')
		except:
			print "Table EventArtist does not exist can not be DROPed"
		self.c.execute('''CREATE  TABLE  IF NOT EXISTS EventArtist (event_id INTEGER NOT NULL, artist_id INTEGER NOT NULL)''')


	def addEvent(self,name, place, pic, url, date, category, besorolas):
		try:
			category=int(category)
		except:
			sys.stderr.write("WARNING: The Category is not an INTEGER\n")
			sys.stderr.write("I check if the '"+category+"' category exist\n")
			if self.categoryExist(category):
				cat_name=category
		                category=self.getCategoryId(category)
				sys.stderr.write("The '"+cat_name+"' category exist and has ID="+category+"\n")
			else:
				sys.stderr.write("The '"+category+"' does not exist I create them\n")
				self.addCategory(category)

		try:
			place=int(place)
		except ValueError:
			sys.stderr.write("ERROR: The placeID is not an INTEGER\n")
			sys.exit(-1)
		
		if not self.eventExist(place,date,name):
			self.c.execute("INSERT INTO Event (name,place_id,pic,url,date,category_id,besorolas) VALUES (?,?,?,?,?,?,?)",(name,place,pic,url,date,category,besorolas))
			self.conn.commit()
			print "Added"
		else:
			print "Not added"


	def addPlace(self,name, url, lat, lon, addrr, email, tel):
		if len(name)>=2 and not self.placeExist(name):
			self.c.execute("INSERT INTO Place (name,url,lat,lon,addrr,email,tel) VALUES (?,?,?,?,?,?,?)",(name,url,lat,lon,addrr,email,tel))
			self.conn.commit()
			print "Added"
		else:
			print "Not added"

	def addArtist(self,name):
		if len(name)>=2 and not self.artistExist(name):
			self.c.execute("INSERT INTO Artist (name) VALUES (?)",[name])
			self.conn.commit()
			print "Added"
		else:
			print "Not added"

	def addCategory(self,name):
		if not self.categoryExist(name):
			self.c.execute("INSERT INTO Category (name) VALUES (?)",[name])
			self.conn.commit()
			print "Added"
		else:
			print "Not added"

	def addEventArtist(self, event_id, artist_id):
		if not self.eventArtistExist(event_id,artist_id):
			self.c.execute("INSERT INTO EventArtist (event_id,artist_id) VALUES (?,?)",(event_id,artist_id))
			self.conn.commit()
			print "Added"
		else:
			print "Not added"

	def categoryExist(self,name):
		sql="SELECT count(id) FROM Category WHERE name='%s'" % name
		self.c.execute(sql)
		ret=self.c.fetchone()[0]
		if int(ret)>=1:		
		        return True
		else:
		        return False
	
	def artistExist(self,name):
		sql="SELECT count(id) FROM Artist WHERE name='%s'" % name
		self.c.execute(sql)
		ret=self.c.fetchone()[0]
		if int(ret)>=1:		
		        return True
		else:
		        return False

	def placeExist(self,name):
		sql="SELECT count(id) FROM Place WHERE name='%s'" % name
		self.c.execute(sql)
		ret=self.c.fetchone()[0]
		if int(ret)>=1:		
		        return True
		else:
		        return False

	def getPlaceId(self,name):
		try:
			return self.c.execute("SELECT id FROM Place WHERE name=?",[name]).fetchone()[0];
		except:
			return 0

	def getPlaceName(self,p_id):
		return self.c.execute("SELECT name FROM Place WHERE id=?",[p_id]).fetchone()[0]

	def getArtistId(self,name):
		try:
			return self.c.execute("SELECT id FROM Artist WHERE name=?",[name]).fetchone()[0]
		except:
			return 0		

	def getArtistName(self,a_id):
		return self.c.execute("SELECT name FROM Artist WHERE id=?",[a_id]).fetchone()[0]

	def getCategoryId(self,name):
		return self.c.execute("SELECT id FROM Category WHERE name=?",[name]).fetchone()[0]

	def getCategoryName(self,c_id):
		return self.c.execute("SELECT name FROM Artist WHERE id=?",[c_id]).fetchone()[0]

	def eventArtistExist(self,event_id, artist_id):
		sql = "SELECT count(event_id) FROM EventArtist WHERE event_id=%d AND artist_id=%d" % (event_id,artist_id)
		self.c.execute(sql)
		ret = self.c.fetchone()[0]
		if int(ret)>=1:
			return True
		else:
			return False

	def eventExist(self,place,date,name):
		sql="SELECT count(id) FROM Event WHERE name='%s' AND date='%s' AND place_id=%d" % (name ,date, place)
		self.c.execute(sql)
		ret=self.c.fetchone()[0]
		if int(ret)>=1:
		        return True
		else:
		        return False

	def getEventId(self,place,date,name):
		return	self.c.execute('''SELECT id FROM Event WHERE name=? AND date=? AND place_id=?''',(name ,date, self.getPlaceId(place))).fetchone()[0]

