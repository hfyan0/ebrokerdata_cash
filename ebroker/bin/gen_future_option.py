#!/usr/bin/python

import sys
import time
#####################################################
# gen_future_option.py <start Strike> <end Strike> <step> <postfix for term 1 call> <postfix for term 1 put> <postfix for term 2 call> <postfix for term 2 put> 
# e.g.
# gen_future_option.py 17800 25000 200 B3 N3 C3 O3
#####################################################
# Jan A,M
# Feb B,N
# Mar C,O
# Apr D,P
# May E,Q
# Jun F,R
# Jul G,S
# Aug H,T
# Sep I,U
# OCT J,V
# NOV K,W
# Dec L,X
startStrike = int(sys.argv[1])
endStrike = int(sys.argv[2])
step = int(sys.argv[3])
postfix = sys.argv[4]
postfix2 = sys.argv[5]
postfix3 = sys.argv[6]
postfix4 = sys.argv[7]
futurefilename = "../conf/hsi_future_feedcodes_list.txt"
f=open(futurefilename)
for line in f.readlines():
	print line.rstrip("\n").strip()

currStrike = startStrike
while currStrike <= endStrike:
	print "HSI" + str(currStrike) + postfix 
	print "HSI" + str(currStrike) + postfix2
	print "HSI" + str(currStrike) + postfix3
	print "HSI" + str(currStrike) + postfix4
	currStrike = currStrike + step

