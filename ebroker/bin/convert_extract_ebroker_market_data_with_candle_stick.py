#!/usr/bin/python

import sys
import time
import re
import candlestick_generator
# Created by DT
# Updated by CCF
# Last update: 20140103, CCF
# Version v0.3
# Change:
# * Parse the line char by char instead of spliting "|"
# * Data structure change
# * New function: tokenizeLine(line)
# Version v0.2
# Change:
# Added deal src id list (deal_src_id_list). The list will be enabled if OMS (key = 110) is enabled.
######################################################################################################
# Convert RAW EBroker real time log file into the following formats:
# 091500,HSIH3,23330,44,B,23330,2,23306,3,23304,4,23301,1,23300,2,A,23336,3,23338,1,23345,1,23347,4,23350,6
#
# time  ,ID   ,last price,Accu Size,B,<Price, Size> x 5,A,<Price, Size> x 5
# Example: ./convert_extract_ebroker_market_data.py EBrokerSampleInput.log 080000 145900 No BidAskTradeOMS
#
# The 4th argument is used to toggle follow file
# Example: ./convert_extract_ebroker_market_data.py EBrokerSampleInput.log 080000 145900 Yes BidAskTradeOMS
#
# The 5th argument is used to specify what output we want to generate
# supported types are:
#	BidAsk		output line when there are Bid Ask changes
#	BidAskTrade	output line when there are Bid Ask or Trade (keyvalue 17,3) changes 
#	BidAskTrade_DH_DL_PC_TO output line when there are Bid Ask or Trade (keyvalue 17,3) changes
# e.g.
# 091500,HSIH3,23330,44,B,23330,2,23306,3,23304,4,23301,1,23300,2,A,23336,3,23338,1,23345,1,23347,4,23350,6,PC,23350,DH,24000,DL,23000,TO,0
#	BidAskTradeOMS	output line when there are Bid Ask or OMS Trade (110) changes
#
######################################################################################
### http://stackoverflow.com/questions/1475950/tail-f-in-python-with-no-time-sleep ### 
######################################################################################
deal_src_id_list = [1,7,36,43]
candlestick_period_size=2

def follow(thefile):
    thefile.seek(0,0)      # if change to (0,2) -> Go to the end of the file
    sleep = 0.00001
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(sleep)    # Sleep briefly
            if sleep < 1.0:
                sleep += 0.00001
            continue
        sleep = 0.00001
        yield line

def testfollow(filename):
	logfile = open(filename)
	loglines = follow(logfile)
	for line in loglines:
		print line,

### 

def myInt(fieldvalue) :
        if (len(fieldvalue)==0) :
                return 0
        else :
              	return int(fieldvalue)

def init():
	global datafile, currPrices
	if logfile == "stdin":
		datafile = sys.stdin
	else:
		datafile = open(logfile, "r")
	currPrices = {}

def initlib():
	global currPrices
	currPrices = {}

def initID(currID):
	global currPrices
	if (currID + "_" + "bid" in currPrices):
		return

	currPrices[currID + "_" + "bid"] = {}
	currPrices[currID + "_" + "ask"] = {}
	currPrices[currID + "_" + "bidSize"] = {}
	currPrices[currID + "_" + "askSize"] = {}
	currPrices[currID + "_" + "bidQueue"] = {}
	currPrices[currID + "_" + "askQueue"] = {}
	currPrices[currID] = {}
	currPrices[currID]["lastPrice"] = 999999
	currPrices[currID]["accSize"] = 0

        currPrices[currID]["previousClose"] = 999999
        currPrices[currID]["dayHigh"] = 999999
        currPrices[currID]["dayLow"] = 999999
        currPrices[currID]["turnOver"] = 999999
	feedcode=currID.split("_")[2]
	mydate=currID.split("_")[1]
	starttime="091500"
	currPrices[currID]["candlestick_generator"] = candlestick_generator.candlestick_generator(feedcode,candlestick_period_size,mydate,starttime)

	for i in range(5):
		currPrices[currID + "_bid"][i] = 999999
		currPrices[currID + "_bidSize"][i] = 999999
		currPrices[currID + "_bidQueue"][i] = 999999
		currPrices[currID + "_ask"][i] = 999999
		currPrices[currID + "_askSize"][i] = 999999
		currPrices[currID + "_askQueue"][i] = 999999

def updateDepthPrice(currID, isBid, depth, price):
	global currPrices
	if len(price) > 0:
		currPrices[currID + "_" + ["ask" , "bid"][isBid]][depth] = float(price)
	else:
		currPrices[currID + "_" + ["ask" , "bid"][isBid]][depth] = float(999999)

def updateDepthSize(currID, isBid, depth, size):
	global currPrices
	currPrices[currID + "_" + ["askSize" , "bidSize"][isBid]][depth] = myInt(size)

def updateDepthQueue(currID, isBid, depth, size):
	global currPrices
	currPrices[currID + "_" + ["askQueue" , "bidQueue"][isBid]][depth] = int(size)

def printDepthInfo(currID, updatetime):
	global currPrices
	global genType
	outstr = "%s,%s,%s,%s,"%(updatetime.replace(":",""), currID.split("_")[2],currPrices[currID]["lastPrice"],currPrices[currID]["accSize"])
	bidOutStr = ""
	askOutStr = ""
	for i in range(5):
		bidOutStr = bidOutStr + "%.3lf,%d%s"%(currPrices[currID + "_bid"][i], currPrices[currID + "_bidSize"][i], ["",","][i <4])
		askOutStr = askOutStr + "%.3lf,%d%s"%(currPrices[currID + "_ask"][i], currPrices[currID + "_askSize"][i], ["",","][i <4])
	
        pc_dh_dl_toStr =  ",PC," + "%.3lf"%(currPrices[currID]["previousClose"])
        pc_dh_dl_toStr = pc_dh_dl_toStr + ",DH," + "%.3lf"%(currPrices[currID]["dayHigh"])
        pc_dh_dl_toStr = pc_dh_dl_toStr + ",DL," + "%.3lf"%(currPrices[currID]["dayLow"])
        pc_dh_dl_toStr = pc_dh_dl_toStr + ",TO," + "%d"%(currPrices[currID]["turnOver"])

	if (genType == "BidAskTrade_DH_DL_PC_TO"):
       		return outstr + "B," + bidOutStr + ",A," + askOutStr + pc_dh_dl_toStr
	else:
		return outstr + "B," + bidOutStr + ",A," + askOutStr

def updateLastPrice(currID, lastPrice):
	global currPrices
	currPrices[currID]["lastPrice"] = lastPrice

def updateLastPriceOMS(currID, OMS):
#110| 09:14:00    46  20776  1  20|
	global currPrices
 	myfields = OMS.split(" ")
#	print "OMS",myfields
#	20131209 CCF
#	if int(myfields[5]) <= 2 or int(myfields[5]) == 43 or int(myfields[5]) == 7:
	if int(myfields[5]) in deal_src_id_list:
		currPrices[currID]["lastPrice"] = float(myfields[3])

def updateAccSize(currID, accSize):
	global currPrices
	currPrices[currID]["accSize"] = accSize

def updatePreviousClose(currID, previousClose):
        global currPrices
        currPrices[currID]["previousClose"] = float(previousClose)

def updateDayHigh(currID, dayHigh):
        global currPrices
        currPrices[currID]["dayHigh"] = float(dayHigh)

def updateDayLow(currID, dayLow):
        global currPrices
        currPrices[currID]["dayLow"] = float(dayLow)

def updateTurnOver(currID, turnOver):
        global currPrices
#	currPrices[currID]["turnOver"] = int(turnOver)
        currPrices[currID]["turnOver"] = float(turnOver)

def updateAccSizeOMS(currID, OMS):
#110| 09:14:00    46  20776  1  20|
	global currPrices
 	myfields = OMS.split(" ")
	#	20131209 CCF
#	if int(myfields[5]) <= 2 or int(myfields[5]) == 43 or int(myfields[5]) == 7:
	if int(myfields[5]) in deal_src_id_list:
		currPrices[currID]["accSize"] += int(myfields[2])
		return True
	else:
		return False
# Function: tokenizeLine
# input (line): Ebroker RAW data line
# input (delim): Delimiter
# output: key-value pair map
def tokenizeLine(raw_line, delim):
	keyvalue_map = {}
	line = raw_line.rstrip("\n")
#	print "line =", line
	header, next_pos = getNextField(line, delim, 0)
	subscription_id, next_pos = getNextField(line, delim, next_pos)
	keyvalue_map["header"] = header
	keyvalue_map["subscription_id"] = subscription_id
	for kv in getNextKeyValue(line, delim, next_pos):
		keyvalue_map[kv[0]] = kv[1]
#	print keyvalue_map
	return keyvalue_map
def getNextField(line, delim, current_pos):
	start_index = current_pos
	end_index = line.find(delim, start_index)
	return line[start_index:end_index],end_index+1

def getNextKeyValue(line, delim, current_pos):	
	while True:
		key, next_pos = getNextField(line, delim, current_pos)
		#print "current_pos = ", current_pos, key, next_pos
		if (next_pos == 0):
			return
		value_start_pos = next_pos
		value, value_end_pos = getNextField(line, delim,value_start_pos)
		#print "value = ", value, value_end_pos
		next_key = ""
		next_pos = value_end_pos
		while (not next_key.isdigit()):
			next_key, next_pos = getNextField(line, delim, next_pos)
			#print "next_key = ", next_key ,next_pos
			if (next_pos == 0):
				break
			if (not next_key.isdigit()):
				value_end_pos = next_pos 
		value = line[value_start_pos:value_end_pos-1]
		current_pos = value_end_pos
		yield key, value

def parseLine(line):
	global currPrices
	global genType
	global startTime, endTime
	if (len(genType)<=0):
		return ""
	keyvalue_map = tokenizeLine(line,"|")
	fields = line.rstrip("\n").split("|")
	updateInfo=""
	updatetime = ""
	#currID = fields[1]

#	if fields[0] == "image":
	currID = keyvalue_map["subscription_id"]
	if (keyvalue_map["header"] == "image"):
		initID(currID)
	hasOMSTrade = False
	deal_src_id = -1

#	for i in range(2,len(fields)-1,2):
	for keyf, value in keyvalue_map.items():
		if (keyf.isdigit()):
			keyf = int(keyf)
		else:
			continue
		if keyf == 1 or keyf == 81 or keyf == 82 or keyf == 83 or keyf == 84:
			updateDepthPrice(currID, True, [keyf-80, 0][keyf < 80], value)
			updateInfo = updateInfo + "bid_price %s " %(value)
		if keyf == 2 or keyf == 91 or keyf == 92 or keyf == 93 or keyf == 94:
			updateDepthPrice(currID, False, [keyf-90, 0][keyf < 90], value)
			updateInfo = updateInfo + "ask_price %s " %(value)
		if keyf == 16 or keyf == 51 or keyf == 52 or keyf == 53 or keyf == 54:
			updateDepthSize(currID, True, [keyf-50, 0][keyf < 50], value)
			updateInfo = updateInfo + "bid_size %s " %(value)
		if keyf == 19 or keyf == 61 or keyf == 62 or keyf == 63 or keyf == 64:
			updateDepthSize(currID, False, [keyf-60, 0][keyf < 60], value)
			updateInfo = updateInfo + "ask_size %s " %(value)

		if keyf == 17 and (genType == "BidAsk" or genType == "BidAskTrade" or genType == "BidAskTrade_DH_DL_PC_TO"):
			updateAccSize(currID,value)
			if (genType == "BidAskTrade" or genType == "BidAskTrade_DH_DL_PC_TO"):
				updateInfo = updateInfo + "acc_size %s " %(value)
		if keyf == 3 and (genType == "BidAsk" or genType == "BidAskTrade_DH_DL_PC_TO" or genType == "BidAskTrade"):
			updateLastPrice(currID,value)
			if (genType == "BidAskTrade_DH_DL_PC_TO" or genType == "BidAskTrade"):
	 			updateInfo = updateInfo + "last_traded %s " %(value)
#		if keyf == 41 and (genType == "BidAskTrade"):
#			updateLastPrice(currID,fields[i+1])
#			updateInfo = updateInfo + "last_traded %s " %(fields[i+1])
		if keyf == 110 and (genType == "BidAskTradeOMS"):
			OMS=re.sub(' +',' ',value)
			updateLastPriceOMS(currID,OMS)
			if not keyvalue_map["header"] == "image":
				notoffExchange=updateAccSizeOMS(currID,OMS)
				if (notoffExchange):
					updateInfo = updateInfo + "OMS %s " %(value)
					deal_src_id = OMS.split(" ")[5]
					hasOMSTrade = True
		if keyf == 33:
			updatetime = value

                if keyf == 31 and (genType=="BidAskTrade_DH_DL_PC_TO"):
                        updatePreviousClose(currID,value)
                        updateInfo = updateInfo + "previous_close %s " %(value)

                if keyf == 32 and (genType=="BidAskTrade_DH_DL_PC_TO"):
                        updateDayLow(currID,value)
                        updateInfo = updateInfo + "day_low %s " %(value)

                if keyf == 37 and (genType=="BidAskTrade_DH_DL_PC_TO"):
                        updateDayHigh(currID,value)
                        updateInfo = updateInfo + "day_high %s " %(value)

                if keyf == 38 and (genType=="BidAskTrade_DH_DL_PC_TO"):
                        updateTurnOver(currID,value)
                        updateInfo = updateInfo + "turnover %s " %(value)

	if (len(updateInfo)>0):
		currTime = updatetime.replace(":","")

		if startTime < currTime and endTime > currTime:
			#print "Updated : (%s) - %s - %s" %(updatetime, currID, updateInfo)
			resultstr=printDepthInfo(currID, updatetime) # + ","+ str(deal_src_id) + "," + str(hasOMSTrade)
			tick=resultstr.split(",")
			currPrices[currID]["candlestick_generator"].process_and_gen_period_from_market_data(tick)
			return resultstr
		else:
			return ""
	else:
		return ""
	return ""

def parseLogfile():
	global datafile
	global currPrices
	if (followFile):
		loglines = follow(datafile)
		for line in loglines:
			resultstr=parseLine(line)
			if not resultstr == "":
				print resultstr
	else:
		for line in datafile.readlines():
			resultstr=parseLine(line)
			if not resultstr == "":
				print resultstr
#testfollow(sys.argv[1])
if __name__ == "__main__":
	global genType
	logfile=sys.argv[1]
	#"EBrokerSample.log"
	
	startTime=sys.argv[2]
	#"080000"

	endTime=sys.argv[3]
	#"090000"

	genType="BidAskTradeOMS"

	if len(sys.argv) >= 6:
		genType=sys.argv[5]

	if len(sys.argv) >=5:
		followFile=(sys.argv[4] == "Yes")
	else:
		followFile = False
	init()
	parseLogfile()
	
