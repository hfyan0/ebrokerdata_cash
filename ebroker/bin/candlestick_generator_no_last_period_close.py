#!/usr/local/bin/python
import datetime
import sys
import types
class candlestick_generator:
        def __init__ (self,feedcode,period_size,period_date,start_period_timestamp_str):
                self.feedcode = feedcode
		self.all_volume_sum=0
                self.prev_traded_avolume = 0
                self.cur_period_datetime = 0
                self.cur_period_price_sum = 0
                self.cur_period_volume_sum = 0
		self.invalid_value=999999		
                self.cur_period_high=-self.invalid_value
                self.cur_period_low=self.invalid_value
                self.cur_period_open=self.invalid_value
                self.cur_period_close=self.invalid_value
                self.cur_period_lastprice=self.invalid_value
                self.period_size=period_size
		self.cur_period_date=period_date
		self.start_period_datetime=self.convert_str_to_datetime(start_period_timestamp_str)
		self.last_valid_period_close=self.invalid_value
		self.period_count=0
		self.tick_datetime=0
		return

	def convertStr2Sec(self,str):
                if len(str)<10:
                        hr=int(str)/10000
                        min=(int(str) - hr * 10000)/100
                        sec=int(str) - hr * 10000 - min*100
                        msec=0
#                       print "HHMMSS",hr,min,sec
                else:
                     	hr=int(str[9:11])
                        min=int(str[11:13])
                        sec=int(str[13:15])
                        msec=float(str[16:21])
                tsec=float(hr*60*60+min*60+sec)+(msec/100000)
#               print hr,min,sec,msec,tsec
                return tsec

        def convert_str_to_datetime(self,secstr):
		return self.convertStr2Sec(secstr)
                self.timestamp_str = secstr
		if (len(secstr) > 10):
	                self.tick_time_in_sec_str = self.timestamp_str.split("_")[1]
        	        self.tick_date_str = self.timestamp_str.split("_")[0]
                else:	
	                self.tick_time_in_sec_str = self.timestamp_str
                        self.tick_date_str = self.cur_period_date
		self.tick_datetime = datetime.datetime(int(self.tick_date_str[0:4]), int(self.tick_date_str[4:6]),int(self.tick_date_str[6:8]), int(self.tick_time_in_sec_str[0:2]), int(self.tick_time_in_sec_str[2:4]), int(self.tick_time_in_sec_str[4:6]))
                return self.tick_datetime

	def gen_last_period(self):
                if (self.cur_period_datetime != 0):
                        yield self.gen_period()

	def same_period_update(self):
                self.cur_period_volume_sum += self.cur_traded_volume
                self.cur_period_price_sum += self.cur_period_price * self.cur_traded_volume 
                if self.cur_period_high < self.cur_period_price:
                      self.cur_period_high = self.cur_period_price	
                if self.cur_period_low > self.cur_period_price:
                      self.cur_period_low = self.cur_period_price
		self.cur_period_lastprice= self.cur_period_price
		self.cur_period_close = self.cur_period_price
		self.last_traded_volume = self.cur_traded_volume
		if (self.cur_period_open==self.invalid_value):
			self.cur_period_open = self.cur_period_price
		return

	def new_period_update(self):
                self.new_period_datetime = int((self.tick_datetime - self.start_period_datetime) / self.period_size) * self.period_size + self.start_period_datetime

		while (self.new_period_datetime > self.cur_period_datetime):
                	yield self.gen_period()
	                self.cur_period_datetime += self.period_size
                	self.cur_period_price_sum = self.cur_period_lastprice
	                self.cur_period_volume_sum = 0
                	self.cur_period_high = self.cur_period_lastprice
                	self.cur_period_low = self.cur_period_lastprice
                	self.cur_period_open = self.cur_period_lastprice
			self.cur_period_close = self.cur_period_lastprice
			self.last_valid_period_close=self.cur_period_lastprice
		
                self.cur_period_price_sum = self.cur_period_price * self.cur_traded_volume
                self.cur_period_volume_sum = self.cur_traded_volume
                self.cur_period_high = self.cur_period_price
                self.cur_period_low = self.cur_period_price
                self.cur_period_open = self.cur_period_price
                self.cur_period_close = self.cur_period_price
		self.last_valid_period_close=self.cur_period_lastprice
		self.cur_period_lastprice = self.cur_period_price
#		yield None

	def process_and_gen_period_from_market_data(self,tick):
		to_process=True
                if (not tick[1] == self.feedcode):
                        to_process=False
                newdatetime=self.convert_str_to_datetime(tick[0])
                if self.tick_datetime > newdatetime:
                        to_process=False
                if to_process:
                   self.tick_datetime=newdatetime
                   price=float(tick[2])
                   avol=int(tick[3])
                   if (self.cur_period_datetime == 0):
                        self.cur_period_datetime = self.start_period_datetime
                        self.prev_traded_avolume = 0
                   self.cur_traded_volume = avol - self.prev_traded_avolume
                   if (self.cur_traded_volume == 0):
                         to_process=False
 #                       print self.printtime(self.convertSec2Str(self.tick_datetime)),self.feedcode, avol, self.prev_traded_avolume ,"WHY"
                   else:
			pass
 #                       print self.printtime(self.convertSec2Str(self.tick_datetime)),self.feedcode, avol, self.prev_traded_avolume
                   if to_process:
                      self.prev_traded_avolume = avol
                      self.cur_period_price = price
                      if ((self.tick_datetime - self.cur_period_datetime) < self.period_size): # same period
                         self.same_period_update()
                      else: # new period
                         yield self.new_period_update()	
#                yield None
        def printdate(self,mydate):
                return mydate[0:4]+"-"+mydate[4:6]+"-"+mydate[6:8]
	def printtime(self,mytime):
                return mytime[0:2]+":"+mytime[2:4]+":"+mytime[4:6]
        def convertSec2Str(self,sec):
                hr=int(sec/3600)
                min=int((sec-3600*hr)/60)
                sec=int((sec-3600*hr-min*60))
                return "%02d%02d%02d"%(hr,min,sec)

        def gen_period(self):
		self.all_volume_sum+=self.cur_period_volume_sum
		if (self.cur_period_volume_sum!=0):
#	                outstr=self.printdate(self.cur_period_date)+" "+self.printtime(self.convertSec2Str(self.cur_period_datetime))+","+self.feedcode+","+str(self.cur_period_open)+","+str(self.cur_period_high)+","+str(self.cur_period_low)+","+str(self.cur_period_close)+","+str(self.cur_period_volume_sum)+","+str(self.last_valid_period_close)
	                outstr=self.printdate(self.cur_period_date)+" "+self.printtime(self.convertSec2Str(self.cur_period_datetime))+","+self.feedcode+","+str(self.cur_period_open)+","+str(self.cur_period_high)+","+str(self.cur_period_low)+","+str(self.cur_period_close)+","+str(self.cur_period_volume_sum)
		else:
#	                outstr=self.printdate(self.cur_period_date)+" "+self.printtime(self.convertSec2Str(self.cur_period_datetime))+","+self.feedcode+","+str(self.invalid_value)+","+str(self.invalid_value)+","+str(self.invalid_value)+","+str(self.invalid_value)+","+str(self.cur_period_volume_sum)+","+str(self.last_valid_period_close)
	                outstr=self.printdate(self.cur_period_date)+" "+self.printtime(self.convertSec2Str(self.cur_period_datetime))+","+self.feedcode+","+str(self.invalid_value)+","+str(self.invalid_value)+","+str(self.invalid_value)+","+str(self.invalid_value)+","+str(self.cur_period_volume_sum)
                yield outstr
def init():
	global candlestick_period_size,candlestick_generator_map,mydate,starttime,isinited
	if not 'isinited' in globals():
	    candlestick_period_size=2
	    mydate="20130819"
	    starttime="091500"
            candlestick_generator_map={}
            isinited=True

def convertor(pmdline):
        global candlestick_period_size,candlestick_generator_map,mydate,starttime
        init()
	if pmdline == "end":
           for feedcode in candlestick_generator_map:
                yield candlestick_generator_map[feedcode].gen_last_period()
#                print feedcode+","+str(candlestick_generator_map[feedcode].all_volume_sum)
        else:
           tick=pmdline.split(",")
           if not tick[1] in candlestick_generator_map:
#		print "create_candlestick_generator for "+tick[1]
                candlestick_generator_map[tick[1]] = candlestick_generator(tick[1],candlestick_period_size,mydate,starttime)	
           else:
                yield candlestick_generator_map[tick[1]].process_and_gen_period_from_market_data(tick)


def read_and_convert_stdin():
        for line in sys.stdin:
#		print line
                yield convertor(line)
        yield convertor("end")

def recursive_expand_generator(gen):
        if isinstance(gen,types.GeneratorType):
            for genout in gen:
               recursive_expand_generator(genout)
        else:
            print gen

if __name__ == "__main__":
	candlestick_gen=read_and_convert_stdin()
        recursive_expand_generator(candlestick_gen)
