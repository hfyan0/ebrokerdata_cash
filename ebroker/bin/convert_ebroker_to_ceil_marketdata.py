#!/usr/bin/python
# -*- encoding: UTF-8 -*-
import csv
import time
import re
import os.path


def convertFromToDate(path,outpath,filename, begindate, enddate):
    f=open(filename,'r')	
    for line in f.readlines():
       fields=line.rstrip().split(",")
       if (fields[0] >= begindate) and (fields[0] <= enddate) and fields[1]!='H':
	   mydate=fields[0][0:4]+fields[0][5:7]+fields[0][8:11]
           filetoconvert=path+"/"+mydate+".csv"
           filetooutput=outpath+"/"+mydate+".csv"
           print mydate,fields[1]
           if (os.path.isfile(filetoconvert)):	
              convertFileDate(mydate,filetoconvert,fields,filetooutput)
              pass
    f.close()

def convertFileDate(date,filename,contractlist,outfilename):
    print outfilename
    f=open(filename,'r')
    lasttradevol={}
    fout=open(outfilename,'w')
    for line in f.readlines():
        fields=line.split(",")
	#only filter feedcode in the contractlist
	if fields[1] in contractlist:
            if not fields[1] in lasttradevol:
                lasttradevol[fields[1]]=0
	    thistradevol=int(fields[3])-int(lasttradevol[fields[1]])
            lasttradevol[fields[1]]=fields[3]
	    fields[3]=str(thistradevol)
	    fields[0]=date+"_"+fields[0]+"_"+"000000"	
	    outline=','.join(fields)
            fout.write(outline)
    f.close()
    fout.close()

def main():
    settlementDateFileName             = '../../common/conf/Settlement_and_Clearing_Dates.csv'
    path = "../data/parsed/hsi_mhi_hhi_mch_future"
    outpath= "../data/parsed/hsi_mhi_hhi_mch_future/to_ea"
    convertFromToDate(path,outpath,settlementDateFileName,"2013-11-01","2014-04-31")    

if __name__ == '__main__':
    import sys
    main()
