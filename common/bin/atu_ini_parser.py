#!/usr/bin/python
import ConfigParser
import sys
import os

default_section = os.getenv('ATU_CONFIG_SECTION',"")
config = ConfigParser.ConfigParser()

def loadconfig(ini_filename):
	global config
	config.read(ini_filename)	
def getItem(section_and_key):
	global config
	global default_section
	if len(section_and_key.split(".")) != 2:
		section = default_section
		key = section_and_key
	else:
		section = section_and_key.split(".")[0]
		key = section_and_key.split(".")[1]
	return config.get(section, key)
def getList(key):
	global config
	ll = ""
	for section in config.sections():
		if len(key) == 0:
			ll += section + " "
		else:
			ll += config.get(section,key) + " "
	return ll.strip()

def getFileItem(section_and_key):
	filename=getItem(section_and_key)
	datafile = open(filename,"r")
	data=""
	isfirstline=True
	for line in datafile.readlines():
		strippedline=line.rstrip("\n").strip()
		if (isfirstline):
			data+=strippedline
		else:
			data+=","+strippedline
		isfirstline=False
	return data
	
