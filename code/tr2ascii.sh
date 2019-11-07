#!/bin/bash

#NEWFILE=`echo $1 | sed -e 's/\(.*\).txt/\1.asc/g'` 
NEWFILE=$1.asc

sed s/ğ/#g/g < $1 | sed s/ü/#u/g | sed s/ç/#c/g | sed s/ö/#o/g | sed s/ş/#s/g | sed s/ı/#i/g | sed s/Ü/#U/g | sed s/Ğ/#G/g | sed s/Ç/#C/g | sed s/Ö/#O/g | sed s/Ş/#S/g | sed s/İ/#I/g | sed s/ğ/#g/g | sed s/ö/#o/g | sed s/Ö/#O/g > $NEWFILE

