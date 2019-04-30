#! /bin/bash
#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        March 12, 2019
#######################################################

DataPath=~ee364/DataFolder/Prelab09
projfile=$DataPath"/maps/projects.dat"

stu_cirs=$(getCircuitsByStudent.bash $1)
grep -E "$stu_cirs" $projfile | tr -s " " | cut -f3 -d " " | sort -u
