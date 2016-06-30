#!/bin/sh
curdate_filename=`date "+%Y%m%d.csv"`
daytype=`~/common/bin/holidaycheck.py`
if [ $daytype == "holiday" ]; then
        exit
fi
alias atul='~/common/bin/get_ini_list.py'
alias atuv='~/common/bin/get_ini_value.py'
ebroker_bin_path=`dirname $0`
cd $ebroker_bin_path
ebroker_marketdata_conf="../conf/ebroker_market_data.ini"
ebroker_bin_path=`atuv DEFAULT.ebroker_bin_path $ebroker_marketdata_conf`
hsi_filename=`atuv "hsi_components.ebroker_parsed_market_data_filename_prefix" ${ebroker_marketdata_conf}`/${curdate_filename}
hsif_filename=`atuv "hsi_mhi_hhi_mch_future.ebroker_parsed_market_data_filename_prefix" ${ebroker_marketdata_conf}`/${curdate_filename}
#echo $hsi_filename
#echo $hsif_filename
tail -q -s 0.001 -F ${hsi_filename} -F ${hsif_filename} > `atuv DEFAULT.ebroker_parsed_market_data_path ${ebroker_marketdata_conf}`"/hsi_components_hsi_mhi_hhi_mch_future/${curdate_filename}"
