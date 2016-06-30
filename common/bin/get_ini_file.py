#!/usr/bin/python
import os
import sys
import atu_ini_parser

default_config_filename = os.path.expanduser("~")+"/common/conf/atu_config.ini"

def init():
	if len(sys.argv) <= 1:
		print "Usage: " + sys.argv[0] + " " + "<key> [ini filename]"
		return False
	if len(sys.argv) >= 3:
		atu_ini_parser.loadconfig(sys.argv[2])
	else:
		atu_ini_parser.loadconfig(default_config_filename)
	return True
if __name__ == "__main__":	
	if init():
		sys.stdout.write(atu_ini_parser.getFileItem(sys.argv[1]))
