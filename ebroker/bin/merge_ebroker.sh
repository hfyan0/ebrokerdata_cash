#!/bin/sh
#For merging multiple ebroker raw log from the legacy EBroker (nc download)
targetprefix=$1
for filename in $@
do
	if [ -f $filename ]; then
		filelen=`expr length $filename` 
		prefixlen=`expr $filelen - 11`
		prefix=`expr substr $filename 1 $prefixlen`
		datestrstart=`expr $prefixlen - 7`
		datestr=`expr substr $prefix $datestrstart 8`
		echo $filename
		echo $filelen
		echo $prefixlen
		echo $prefix
		echo $datestrstart
		echo $datestr
		file1=${prefix}"_085501.log"
		file2=${prefix}"_120201.log"
		file3=${prefix}"_165501.log"

		targetfile=${targetprefix}"_"$datestr"_085501.log"
		sedstr='s/\(.*|ID_\)......_/\1'${datestr}'_/g'
		echo $sedstr
		if [ ! -f $targetfile ]; then
			echo $file1
			echo $file2
			echo $file3
			echo $targetfile

			sed "$sedstr" $file1 > $targetfile
			sed "$sedstr" $file2 >> $targetfile
			sed "$sedstr" $file3 >> $targetfile
		fi
		echo "-----------------------------------------"
	fi
done
