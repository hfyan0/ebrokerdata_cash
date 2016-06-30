#!/bin/bash

UNDLYSYM="HSI"
OPTIONCTRT="A B C D E F G H I J K L M N O P Q R S T U V W X"
YEAR="6"

FROMSTRIKE=18000
TOSTRIKE=25000
STRIKEINTERVAL=200

STRIKE=$FROMSTRIKE

while [[ $STRIKE -le $TOSTRIKE ]]
do
    for o in $OPTIONCTRT
    do
        for y in $YEAR
        do
            echo "$UNDLYSYM""$STRIKE""$o""$y"
        done
    done
    STRIKE=$(expr $STRIKE + $STRIKEINTERVAL)
done
