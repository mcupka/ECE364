#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        1/16/19
#######################################################
import os
import sys
import operator

# Module  level  Variables. (Write  this  statement  verbatim .)
#######################################################

def findLongest() -> int:
    seqLengths = []
    currSeq = []

    for i in range(1000000):
        currNum = i + 1
        currSeq = []
        currSeq.append(currNum)
        while(currNum > 1):
            if (currNum % 2 == 0):
                #Value is even
                currNum = currNum / 2
            else:
                #number is odd
                currNum = 3 * currNum + 1
            currSeq.append(currNum)

        seqLengths.append(len(currSeq))
    return operator.indexOf(seqLengths, max(seqLengths)) + 1



def findSmallest() -> int:
    a = 1
    found = False
    arePermutations = True
    currSet = []

    while (not found):
        currSet = []
        currSet.append(a)
        for i in range(2, 7):
            currSet.append(i * a) #get 2n 3n 4n 5n 6n
        #Now check to see if all are permutations
        arePermutations = True

        correctNums = list(str(currSet[0]))
        correctNums.sort()

        for j in range(5):
            test = list(str(currSet[j + 1]))
            test.sort()
            if (test != correctNums):
                arePermutations = False
                break

        if arePermutations:
            found = True
        else:
            a += 1

    return a


if __name__  == "__main__":
    pass