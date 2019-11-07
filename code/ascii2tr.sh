#!/bin/bash

NEWFILE=`echo $1 | sed -e 's/\(.*\).asc/\1/g'` 

sed s/#g/ğ/g < $1 | sed s/#u/ü/g | sed s/#c/ç/g | sed s/#o/ö/g | sed s/#s/ş/g | sed s/#i/ı/g | sed s/#U/Ü/g | sed s/#G/Ğ/g | sed s/#C/Ç/g | sed s/#O/Ö/g | sed s/#S/Ş/g | sed s/#I/İ/g > $NEWFILE
