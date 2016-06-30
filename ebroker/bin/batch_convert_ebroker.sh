#!/bin/sh
#batch convert ebroker raw data to parsed market data
#need to chnage outputpath to specify where to save the converted data
productgroup=$1
genType=$2
#convertor="/home/marketdata/ebroker/bin/convert_extract_ebroker_market_data.py"
convertor="./convert_extract_ebroker_market_data_addin_1_7_43_ccf.py"
outputpath="/home/marketdata/EBrokerData/tmpconverted/"${productgroup}
for filename in $@
do
	if [ -f $filename ]; then
		filelen=`expr length $filename` 
		prefixlen=`expr $filelen - 11`
		prefix=`expr substr $filename 1 $prefixlen`
		datestrstart=`expr $prefixlen - 7`
		datestr=`expr substr $prefix $datestrstart 8`
		echo $filename
		$convertor $filename 000000 230000 No $genType > $outputpath"/"$datestr".csv"
	fi
done
