#! /bin/bash
#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        March 12, 2019
#######################################################

DataPath=~ee364/DataFolder/Prelab09

projfile=$DataPath"/maps/projects.dat"
cir_ids=$(getCircuitsByProject.bash $1) # get the ids
cirdir=$DataPath"/circuits"
cir_files=$(for c in $cir_ids; do echo $cirdir/circuit_$c.dat; done)

# get a list of student ids
stu_ids=$(cat $cir_files | grep -E "[0-9]{5}-[0-9]{5}" -o | sort -u)

stu_file=$DataPath"/maps/students.dat"

names=$(for s in $stu_ids; do grep -E $s $stu_file | grep -E "[A-Za-z]+, [A-Za-z]+" -o; done)

echo $names | grep -E "[A-Za-z]+, [A-Za-z]+" -o | sort -u



