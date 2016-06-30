#!/usr/bin/python
import sys
import os
import shutil
from glob import glob
def do_remove_date_list(dir):
	f=open(remove_date_list_file,"r")
	remove_date_list=[]
	for line in f.readlines():
		fields = line.split(" ")
		remove_date_list.append(fields[0])

	removedir=dir+"/remove_date_list"

	try:
    		os.stat(removedir)
	except:
    		os.mkdir(removedir)    

	for datestr in remove_date_list:
		srclist = glob(os.path.join(dir,"*"+datestr+"*"))
		for src in srclist:
			srcbasename=os.path.basename(src)
			tar=removedir+"/"+srcbasename
			if  os.path.exists(src) and os.path.exists(removedir):
				print src, tar
				shutil.move(src,tar)


remove_date_list_file="/home/marketdata/ebroker/conf/2013_remove_date_list.txt"
dirlistfile="/home/marketdata/ebroker/conf/list_of_directory_to_remove_date_list.txt"
f=open(dirlistfile,"r")
dirlist=[]
for line in f.readlines():
	line0=line.rstrip("\n")
	dir=line0.strip()
	do_remove_date_list(dir)	
