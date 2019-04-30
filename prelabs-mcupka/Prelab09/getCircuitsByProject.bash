#! /bin/bash
#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        March 12, 2019
#######################################################

DataPath=~ee364/DataFolder/Prelab09

projfile=$DataPath"/maps/projects.dat"
grep -E $1 $projfile | grep -E "[0-9]{2}-[0-9]-[0-9]{2}" -o | sort -u #get lines that contain a proj id, output the circuit ids, sorted, without duplicates


