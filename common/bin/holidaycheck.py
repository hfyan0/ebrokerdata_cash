#!/usr/local/bin/python
import sys
from datetime import date

#Usage:
#holidayCheck.py
#print holiday if it is a holiday
#print normal if it is not a holiday
#infile="~/common/conf/HKEx_Clearing_Dates_Contract_Use_Month_Before_Clearing_2009-2014_v6.csv"
infile="~/common/conf/Settlement_and_Clearing_Dates.csv"

def check(date,cal):
        if cal[date]=='H':
                return False
        else:
             	return True

def process_calendar(infile):
	global caldict
        f = open(infile,'r')
        line = f.readline() #dump the first line
        caldict = {}
        while line:
                line = f.readline()
                tokens= line.split(',')
                if len(tokens)>1:
                        caldict[tokens[0]] = tokens[1]

        f.close()
	toCheck = date.today().isoformat()

checkToday = True
if __name__ == "__main__":
	process_calendar(infile)
        if checkToday:
                toCheck = date.today().isoformat()
        else:
             	toCheck = '2013-12-21'

        if check(toCheck,caldict):
#		print ("normal",end="")
		sys.stdout.write("normal")
                sys.exit(0)
        else:
#		print ("holiday",end="")
		sys.stdout.write("holiday")
             	sys.exit(1)

