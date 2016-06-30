#!/usr/bin/python
import atu_tcp_client
from socket import socket
import datetime
import time
import convert_extract_ebroker_market_data
import atu_ini_parser
import sys

config_ini = "../conf/ebroker_market_data.ini"

now_time = datetime.datetime.now()
rawEBrokerFile_file = None
parsedMarketDataFile_file = None

def readTime(key):
	strtime=atu_ini_parser.getItem(key)
	datetimevalue = datetime.time(int(strtime[0:2]),int(strtime[2:4]),int(strtime[4:6]))
	return datetimevalue

	
# From MarketCondition
def isMarketOpen(cur_time):
	if (cur_time >= para_morning_start_time and cur_time < para_morning_end_time) or \
		(cur_time >= para_afternoon_start_time and cur_time < para_afternoon_end_time) or \
		(cur_time >= para_afterhour_start_time and cur_time < para_afterhour_end_time):
		return True
	else:
		return False

def isMarketOpenNow():
	cur_time = datetime.datetime.now().time()
	return isMarketOpen(cur_time)

# Can optimize with sleep n sec, where n = next market open time - now()
def waitUntilMarketOpen():
	print "Waiting market to open..."
	while not isMarketOpenNow():
		time.sleep(0.5)

def saveLinetoFile(filename_file, line):
	filename_file.write(line)
	filename_file.flush()

def convertParsedMarketData(line):
	return convert_extract_ebroker_market_data.parseLine(line)


def processEbrokerUpdate(line):
	global rawEBrokerFile_file
#	print "processUpdate=", line
	saveLinetoFile(rawEBrokerFile_file, line+"\n")
	pmdline = convertParsedMarketData(line+"\n")
	if (len(pmdline) > 0):
		saveLinetoFile(parsedMarketDataFile_file, pmdline+"\n")

def init():
	global rawEBrokerFile_file, parsedMarketDataFile_file
	global para_morning_start_time,para_morning_end_time,para_afternoon_start_time,para_afternoon_end_time,para_afterhour_start_time,para_afterhour_end_time
	global para_ebroker_server_address_str,	para_ebroker_server_port_str, para_feedcodes_str
	market_data_group_name = sys.argv[1]
	atu_ini_parser.loadconfig(config_ini)
	para_morning_start_time = readTime(market_data_group_name+".morning_start_time")
	para_morning_end_time = readTime(market_data_group_name+".morning_end_time")
	para_afternoon_start_time = readTime(market_data_group_name+".afternoon_start_time")
	para_afternoon_end_time = readTime(market_data_group_name+".afternoon_end_time")
	para_afterhour_start_time = readTime(market_data_group_name+".afterhour_start_time")
	para_afterhour_end_time = readTime(market_data_group_name+".afterhour_end_time")
	para_ebroker_server_address_str = atu_ini_parser.getItem(market_data_group_name+".ebroker_server_address")
	para_ebroker_server_port_str = atu_ini_parser.getItem(market_data_group_name+".ebroker_server_port")
	para_feedcodes_str = atu_ini_parser.getFileItem(market_data_group_name+".list_of_feedcodes_filename")
	print para_morning_start_time
	print para_morning_end_time
	print para_afternoon_start_time
	print para_afternoon_end_time
	print para_afterhour_start_time
	print para_afterhour_end_time
	print para_ebroker_server_address_str
	print para_ebroker_server_port_str
	print para_feedcodes_str

	curtimestr=	str(now_time.date().year).zfill(2) + \
			str(now_time.date().month).zfill(2) + \
			str(now_time.date().day).zfill(2) + "_" + \
			str(now_time.time().hour).zfill(2) + \
			str(now_time.time().minute).zfill(2) + \
			str(now_time.time().second).zfill(2)
	curdatestr=	str(now_time.date().year).zfill(2) + \
			str(now_time.date().month).zfill(2) + \
			str(now_time.date().day).zfill(2)
		
	para_ebroker_market_data_filename_prefix = atu_ini_parser.getItem(market_data_group_name+".ebroker_market_data_filename_prefix")
	para_ebroker_parsed_market_data_filename_prefix = atu_ini_parser.getItem(market_data_group_name+".ebroker_parsed_market_data_filename_prefix")
	rawEBrokerFilename_str = para_ebroker_market_data_filename_prefix + "_" + curtimestr + ".log"
	parsedMarketDataFilename_str = para_ebroker_parsed_market_data_filename_prefix + "/" + curdatestr + ".csv"

	print parsedMarketDataFilename_str
	print rawEBrokerFilename_str
  ###################################################
  # Sunny modified # [start]
  ###################################################
	rawEBrokerFile_file = open(rawEBrokerFilename_str, "a")
	parsedMarketDataFile_file = open(parsedMarketDataFilename_str, "a")
  ###################################################
  # Sunny modified # [end]
  ###################################################

	convert_extract_ebroker_market_data.startTime="000000"
	convert_extract_ebroker_market_data.endTime="230000"
	convert_extract_ebroker_market_data.genType=atu_ini_parser.getItem(market_data_group_name+".convert_extract_ebroker_gen_type")
  ###################################################
  # Sunny added # [start]
  ###################################################
	convert_extract_ebroker_market_data.stkCodePadLeadingZero=atu_ini_parser.getItem(market_data_group_name+".convert_stock_code_pad_leading_zero")
	convert_extract_ebroker_market_data.useFullTimestamp=atu_ini_parser.getItem(market_data_group_name+".useFullTimestamp")
  ###################################################
  # Sunny added # [end]
  ###################################################
	convert_extract_ebroker_market_data.initlib()

def finish():
	rawEBrokerFile_file.close()
	parsedMarketDataFile_file.close()

def connectEBroker(server, port, feedcodes, processEbrokerUpdate):
	sock = socket()
	sock.connect((server, port))
	for feedcode in feedcodes.split(','):
		feedcode = feedcode.strip()
		curdatestr=	str(now_time.date().year).zfill(2) + \
				str(now_time.date().month).zfill(2) + \
				str(now_time.date().day).zfill(2)
		ebroker_command = "open|ID_" + curdatestr + "_" + feedcode + "|" + feedcode + "|mode|both|\n"
		sock.send(ebroker_command)

	for line in atu_tcp_client.non_blocking_readlines(sock, isMarketOpenNow):
		line = line.strip()
		processEbrokerUpdate(line)

if __name__ == "__main__":
	print "--- Start ---"
	init()	
	connectEBroker(para_ebroker_server_address_str, int(para_ebroker_server_port_str), para_feedcodes_str, processEbrokerUpdate)
	print "LunchTime"
	waitUntilMarketOpen()
	connectEBroker(para_ebroker_server_address_str, int(para_ebroker_server_port_str), para_feedcodes_str, processEbrokerUpdate)
	print "DayMarketClose"
	waitUntilMarketOpen()
	connectEBroker(para_ebroker_server_address_str, int(para_ebroker_server_port_str), para_feedcodes_str, processEbrokerUpdate)
	print "NightMarketClose"
	finish()
	print "---  End  ---"


