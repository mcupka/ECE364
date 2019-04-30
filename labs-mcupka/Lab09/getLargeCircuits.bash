#! /bin/bash
#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        March 20, 2019
#######################################################

DataPath=~ee364/DataFolder/Lab09
cirdir=$DataPath"/circuits"

circ_names=$(ls $cirdir)

for c in $circ_names
do
	name=$(echo $c | head -n 1 | tail -c +9 | head -c -5)
	size=$(wc $cirdir"/"$c | tr -s " " | cut -f4 -d " ")
	if [[ $size -gt 200 ]]; then echo $name; fi
done

