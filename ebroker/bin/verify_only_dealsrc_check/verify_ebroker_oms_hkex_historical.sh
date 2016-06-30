#!/bin/sh
filenamelist=`ls /home/marketdata/ebroker/data/raw/hsi_future/hsi_future_201310*`
for f in ${filenamelist}
do
	echo ${f}
#	echo 1_7_43_`basename ${f}`
	./convert_extract_ebroker_market_data_addin_1_7_43_ccf.py ${f} 080000 161555 No BidAskTradeOMS > /tmp/1_7_43_`basename ${f}`
	tail /tmp/1_7_43_`basename ${f}`
done
