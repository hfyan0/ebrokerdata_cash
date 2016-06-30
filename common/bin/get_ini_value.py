#!/usr/bin/python
import sys
import os
import atu_ini_parser

default_config_filename = os.path.expanduser("~")+"/common/conf/atu_config.ini"

def init():
	if len(sys.argv) <= 1 or (len(sys.argv[1].split(".")) <= 1 and len(atu_ini_parser.default_section) == 0):
		print "Usage: " + sys.argv[0] + " " + "<section>.<key> [ini filename]"
		return False
	if len(sys.argv) >= 3:
		atu_ini_parser.loadconfig(sys.argv[2])
	else:
		atu_ini_parser.loadconfig(default_config_filename)
	return True

if __name__ == "__main__":	
	if init():
		#print getItem(sys.argv[1])
		sys.stdout.write(atu_ini_parser.getItem(sys.argv[1]))
