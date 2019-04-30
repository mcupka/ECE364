#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        2/20/19
#######################################################
import os
import sys
import re

# Module  level  Variables.
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Lab06')


def extractArguments(commandLine: str) -> list:
    pattern = r' *[+\\]([a-z]) +([^\\+\s][^ ]*) *'
    search = re.findall(pattern, commandLine)
    return search


def extractNumerics(sentence: str) -> list:
    all_pattern = r'\s*([+-]?\d+(?:.?\d+)(?:[eE][+-]\d*)?)\s*'
    search = re.findall(all_pattern, sentence)
    return search


if __name__ == "__main__":
    print(extractArguments('myScript.bash +v  \i 2    +p /local/bin/somefolder +A fjkdsla; \k jfdk sla'))
    print(extractNumerics('With the electron\'s charge being -1.6022e-19, some choices you have are -110, -32.0 and +55. Asssume that pi equals 3.1415, \'e\' equals 2.7 and Na is +6.0221E+023'))