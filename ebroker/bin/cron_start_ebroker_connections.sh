#!/bin/bash
TIMESTAMP=$(date +'%Y%m%d_%H%M%S')

# daytype=`~/common/bin/holidaycheck.py`
# if [ $daytype == "holiday" ]; then
#         exit
# fi

atul=~/marketdata_cash/common/bin/get_ini_list.py
atuv=~/marketdata_cash/common/bin/get_ini_value.py

if [[ -f $atul && -f $atuv ]]
then
    ebroker_bin_path=`dirname $0`
    echo $ebroker_bin_path
    cd $ebroker_bin_path 
    ebroker_marketdata_conf="../conf/ebroker_market_data.ini"
    ebroker_connector="./ebroker_connector.py"
    ebroker_bin_path=$($atuv DEFAULT.ebroker_bin_path $ebroker_marketdata_conf)
    for market_data_group_name in $($atul market_data_group_name $ebroker_marketdata_conf)
    do
    	echo $market_data_group_name
    	echo $ebroker_connector
      $ebroker_connector $market_data_group_name > ../log/"$market_data_group_name"_"$TIMESTAMP".log 2>&1 &
    done
else
    echo "$atul not exist."
    echo "$atuv not exist."
fi
