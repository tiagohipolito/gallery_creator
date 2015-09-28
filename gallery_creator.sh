#!/bin/bash

if [ -z "$1" ]; then
	echo "no directory found $1"
	exit;
fi
FILECOUNT=`ls $1[0-9]* | wc -l`
echo "$FILECOUNT file(s) found"

echo "creating backup pictures..."
mkdir -p $1/original/
cp $1/*.* $1/original/

echo "removing extension..."
for f in $1*.*; do mv $f ${f%.*}; done

echo "lpad (3 digits)"
declare -i counter=0
for f in $1[0-9]*; do 
	counter=$counter+1
	FILENAME=`basename "${f%.*}"`
	mv $f "$(dirname "${f}")/`printf %03d ${counter}`"; 
done

echo "add .jpg extension back" 
for f in $1[0-9]*; do mv $f ${f}.jpg; done

echo -ne "resize pictures\r"
counter=0
for f in $1/[0-9]*; do
	convert $f -resize 500x500 ${f}; 
	counter=$counter+1
	percent=$(( counter * 100 / FILECOUNT )) 
	echo -ne "resize pictures                 ( $percent %)\r"
done
echo -ne '\n'

echo -ne "create thumbnails\r"
counter=0
for f in $1/[0-9]*; do 
	FILENAME=`basename "${f%.*}"`
	
	convert $f -resize 75x75 -background white -gravity center -extent 75x75 -quality 75  "$(dirname "${f}")/s${FILENAME}.jpg"; 
	counter=$counter+1
	percent=$(( counter * 100 / FILECOUNT )) 
	echo -ne "create thumbnails                 ( $percent %)\r"
done
echo -ne '\n'

echo "Goodbye"











