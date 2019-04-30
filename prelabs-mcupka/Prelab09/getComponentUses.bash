#! /bin/bash
#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        March 12, 2019
#######################################################

# very simple grep command

DataPath=~ee364/DataFolder/Prelab09
cirdir=$DataPath"/circuits"

grep -E -l "$1" $cirdir/* | sort -u | wc -l
