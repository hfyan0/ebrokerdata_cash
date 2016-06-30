#!/usr/bin/python
# -*- encoding: UTF-8 -*-
'''
Created on 26 Mar 2014

@author: boreas.law
'''

import csv
import time
import re

def getFuturesContracts(f):
    retVal = list()
    for line in f:
        if line[0] == '[' and line[len(line) - 8:].strip('\n') == 'future]':
                # Handling futures
                targetValue = line[1:len(line) - 9]
                retVal.append(targetValue.upper())
    return retVal

def getOptionContracts(f):
    retVal = list()
    for line in f:
        if line[0] == '[' and line[len(line) - 15:].strip('\n') == 'future_option]':
                # Handling options
                targetValue = line[1:len(line) - 16]
                retVal.append(targetValue.upper())
    return retVal

def getTargetDateContracts(f, targetDate):
    for row in csv.DictReader(f):
        # Find target date's column of found contracts
        if row['Date'] == targetDate:
            return row

def main(targetDate):
    inputFilename           = 'ebroker_market_data.ini'
    csvFilename             = 'Settlement_and_Clearing_Dates.csv'
    futuresOutputFilenameSuffix   = '_future_feedcodes_list.txt'
    optionOutputFilenameSuffix    = '_future_option_feedcodes_list.txt'
    lowestOptionStrike      = 17000
    highestOptionStrike     = 25000
    strikeStep              = 200

    # Read in ebroker_market_data.ini
    with open(inputFilename, 'r') as inputFile:
        # Get all contracts shown in ebroker_market_data.ini with suffix [*future]
        futuresContractList = getFuturesContracts(inputFile)
        inputFile.seek(0)
        optionContractList = getOptionContracts(inputFile)

    # Load in Settlement_and_clearing_Dates.csv
    with open(csvFilename, 'r') as csvFile:
        contracts = getTargetDateContracts(csvFile, targetDate)
    
    # Output to *_future_feedcodes_list.txt
    for contract in futuresContractList:
        with open(contract.lower() + futuresOutputFilenameSuffix, 'w') as outputFile:
            outputFile.write(contracts[contract] + '\n')

    # Output to *_future_option_feedcodes_list.txt
    for contract in optionContractList:
        with open(contract.lower() + optionOutputFilenameSuffix, 'w') as outputFile:
            outputFile.write(contracts[contract] + '\n')
        
            callCode = contracts[contract + 'CALLPATTERN'] 
            putCode  = contracts[contract + 'PUTPATTERN']
        
            strikePrice = lowestOptionStrike
            while strikePrice <= highestOptionStrike:
                # Replace <STRIKE> in callCode with strikes
                outputFile.write(re.sub('<STRIKE>', str(strikePrice), callCode) + '\n')
                # Replace <STRIKE> in putCode with strikes
                outputFile.write(re.sub('<STRIKE>', str(strikePrice), putCode) + '\n')
                strikePrice += strikeStep

    # Output to *****_future_feedcodes_list.txt
    with open('_'.join(futuresContractList).lower() + futuresOutputFilenameSuffix, 'w') as outputFile:
        for contract in futuresContractList:
            outputFile.write(contracts[contract] + '\n')
            
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] != '':
        targetDate = sys.argv[1]
    else:
        targetDate = time.strftime('%Y-%m-%d')
    main(targetDate)
