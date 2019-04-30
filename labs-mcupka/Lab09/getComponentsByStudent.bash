#! /bin/bash
#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        March 20, 2019
#######################################################

DataPath=~ee364/DataFolder/Lab09
stufile=$DataPath"/maps/students.dat"
cirdir=$DataPath"/circuits"

id=$(grep -E "$1" $stufile | grep -E "[0-9]{5}-[0-9]{5}" -o)
all_cirs=$(ls $cirdir | grep -E "[0-9]{2}-[0-9]-[0-9]{2}" -o)

match=$(for cir in $all_cirs
do
	if grep -E -q $id $cirdir/circuit_$cir.dat; then echo $cir; fi
done)

circs=$(for m in $(echo $match| sort -u); do echo $m; done)

circ_filenames=$(for c in $circs; do echo $cirdir"/circuit_"$c".dat"|cat; done)
cat $circ_filenames | grep -E "[A-Z]{3}-[0-9]{3}" -o | sort -u
