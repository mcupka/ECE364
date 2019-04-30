#! /bin/bash
#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        March 12, 2019
#######################################################

uses1=$(getComponentUses.bash $1)
uses2=$(getComponentUses.bash $2)

if [[ $uses1 > $uses2 ]]
then
	echo "$1"
else
	echo "$2"
fi

