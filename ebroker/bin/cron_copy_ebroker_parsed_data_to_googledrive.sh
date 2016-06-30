#!/bin/sh
cd /home/marketdata/ebroker/bin
alias atul='~/common/bin/get_ini_list.py'
alias atuv='~/common/bin/get_ini_value.py'
ebroker_marketdata_conf="../conf/ebroker_market_data.ini"
ebroker_parsed_dir="/home/marketdata/ebroker/data/parsed"
tmp_ebroker_parsed="/tmp/ebroker_parsed"
targetmountdrivedir="/mnt/mbs-g-temp1/GoogleDrive/Google_Drive/Historical Data/EBroker/parsed"
mkdir $tmp_ebroker_parsed
today=`date +%Y%m%d`
#today="20131022"
echo $today
for market_data_group_name in `atul market_data_group_name $ebroker_marketdata_conf`
do
	echo $market_data_group_name
	targetdir=$targetmountdrivedir"/"$market_data_group_name
	echo "Creating $targetdir"
	mkdir "$targetdir"
	market_data_directory=$ebroker_parsed_dir"/"$market_data_group_name
	for filename in $market_data_directory/*.csv
	do
		basefilename=`basename $filename`
		tmptargetfile=$tmp_ebroker_parsed"/"$basefilename
		targetfile="$targetdir/"$basefilename".gz"
			
		if [ -f $filename ]; then
			todayfile=$today".csv"
			if [ ! -f "$targetfile" -o $todayfile = $basefilename ]; then
				echo "Preparing $filename to $tmptargetfile"
				cp $filename $tmptargetfile
				gzip $tmptargetfile
				echo "Prepared file "$tmptargetfile".gz"
				echo "Copying $tmptargetfile to $targetfile"
				cp $tmptargetfile".gz" "$targetfile"
				echo "Removing "$tmptargetfile
				rm $tmptargetfile".gz"
			else
				echo "Skipped $filename to $targetfile"
			fi
		fi
		echo "--------------------------------------------------"
	done
done

