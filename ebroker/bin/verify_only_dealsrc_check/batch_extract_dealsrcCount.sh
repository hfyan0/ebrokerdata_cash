#!/bin/sh
#batch convert ebroker raw data to parsed market data and show the count of the deal source and count of the deal source volume
# and redirect output to /tmp/ebrokeralldealsrc.log
convertor="./convert_extract_ebroker_market_data_addin_all_dealsrc_count.py"
for filename in $@
do
	if [ -f $filename ]; then
		echo $filename
		$convertor $filename 000000 230000 No BidAskTradeOMS > /tmp/ebrokeroms.log
		grep "ID" /tmp/ebrokeroms.log
	fi
done
