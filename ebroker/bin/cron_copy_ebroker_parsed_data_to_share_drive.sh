#!/bin/sh
##cd /mnt/mbs-g-temp3/Share/market_data_log/ebroker/data
##cp -r -u /home/marketdata/ebroker/data/parsed ./ &
#modify to copy only todays data
alias atul='~/common/bin/get_ini_list.py'
alias atuv='~/common/bin/get_ini_value.py'
tbasepath=`atuv DEFAULT.market_data_target_share_drive`
targetdir=$tbasepath"/ebroker/data/parsed"
ebroker_bin_path=`dirname $0`
#echo $ebroker_bin_path
cd $ebroker_bin_path
ebroker_marketdata_conf="../conf/ebroker_market_data.ini"
ebroker_connector="./ebroker_connector.py"
ebroker_bin_path=`atuv DEFAULT.ebroker_bin_path $ebroker_marketdata_conf`
curdate=`date +"%Y%m%d"`
if [ $1 != "" ]; then
	curdate=$1
fi
echo $1
for market_data_group_name in `atul market_data_group_name $ebroker_marketdata_conf`
do
        echo $market_data_group_name
        source=`atuv $market_data_group_name".ebroker_parsed_market_data_filename_prefix" $ebroker_marketdata_conf`"/$curdate"".csv"
        target=$targetdir"/$market_data_group_name/$curdate"".csv"
	echo $source
	echo $target
	cp $source $target
        #$ebroker_connector $market_data_group_name &
done

