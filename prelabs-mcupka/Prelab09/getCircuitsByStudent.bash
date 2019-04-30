#! /bin/bash
#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        March 12, 2019
#######################################################

# get student ID
# get list of all circuit IDs
# grep each circuit for the student's ID
# if match is found, output cir id

DataPath=~ee364/DataFolder/Prelab09
stufile=$DataPath"/maps/students.dat"
cirdir=$DataPath"/circuits"

id=$(grep -E "$1" $stufile | grep -E "[0-9]{5}-[0-9]{5}" -o)
all_cirs=$(ls $cirdir | grep -E "[0-9]{2}-[0-9]-[0-9]{2}" -o)

match=$(for cir in $all_cirs
do
	if grep -E -q $id $cirdir/circuit_$cir.dat; then echo $cir; fi
done)

for m in $(echo $match| sort -u); do echo $m; done

