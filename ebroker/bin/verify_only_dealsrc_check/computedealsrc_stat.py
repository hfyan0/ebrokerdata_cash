#!/usr/bin/python
# count the deal source occurrence and deal source volume count for each of the deal source
# on dealsrcfile="/tmp/ebrokeralldealsrc.log"
import re
def readCalendar(filename):
	global calendardict
 	f = open(filename,'r')
        line = f.readline() #dump the first line
        calendardict = {}
        while line:
                line = f.readline()
                tokens= line.split(',')
                if len(tokens)>1:
                        calendardict[tokens[0]] = tokens[3]

        f.close()


readCalendar("HKEx_Clearing_Dates_Contract_Use_Month_Before_Clearing_2009-2013_v5.csv")
dealsrcfile="/tmp/ebrokeralldealsrc.log"
f=open(dealsrcfile,'r')
line=f.readline()
dealsrcCountTotal={}
dealsrcCountDays={}
dealsrcVolCountTotal={}
dealsrcVolCountDays={}
while line:
	line=f.readline()
	line0=line.rstrip()
	line2=re.sub("'","",line0)
	line3=re.sub(":","",line2)
	line4=re.sub(",","",line3)
	line5=re.sub("{","",line4)
	line6=re.sub("}","",line5)
	fields=line6.split(" ")
	if "dealsrc" in fields[0]:
		date=fields[1].split("_")[1]
		date2=date[0:4]+"-"+date[4:6]+"-"+date[6:8]
		#print date2,calendardict[date2]
		if calendardict[date2]==fields[1].split("_")[2]:
			curindex=2
			print fields
			while curindex < len(fields):
			#	print fields[curindex],fields[curindex+1]
				dealsrc=fields[curindex]
				if not dealsrc in dealsrcCountTotal.keys():
					dealsrcCountTotal[dealsrc]=0
					dealsrcCountDays[dealsrc]=0
					dealsrcVolCountTotal[dealsrc]=0
					dealsrcVolCountDays[dealsrc]=0
				value=int(fields[curindex+1])
				if fields[0]=="dealsrcCount":
					dealsrcCountTotal[dealsrc]+=value
					dealsrcCountDays[dealsrc]+=1
				if fields[0]=="dealsrcVolCount":
					dealsrcVolCountTotal[dealsrc]+=value
					dealsrcVolCountDays[dealsrc]+=1

				curindex+=2

for dealsrc in dealsrcCountTotal.keys():
	print "dealsrc=",dealsrc,"avercount=",float(dealsrcCountTotal[dealsrc])/float(dealsrcCountDays[dealsrc]),"totalcount=",dealsrcCountTotal[dealsrc],"days=",dealsrcCountDays[dealsrc]
	print "dealsrc=",dealsrc,"avervol=",float(dealsrcVolCountTotal[dealsrc])/float(dealsrcVolCountDays[dealsrc]),"totalvol=",dealsrcVolCountTotal[dealsrc],"days=",dealsrcVolCountDays[dealsrc]
