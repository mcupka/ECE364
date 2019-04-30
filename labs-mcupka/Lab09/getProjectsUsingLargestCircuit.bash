#! /bin/bash
#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        March 20, 2019
#######################################################

DataPath=~ee364/DataFolder/Lab09
cirdir=$DataPath"/circuits"
projfile=$DataPath"/maps/projects.dat"

largest_cname=$(ls $cirdir --sort=size | head -n 1 | tail -c +9 | head -c -5)

grep $largest_cname $projfile | tr -s " " | cut -f3 -d " " | sort -u
