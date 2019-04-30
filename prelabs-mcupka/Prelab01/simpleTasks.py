#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        January 10, 2019
#######################################################
import os      # List of  module  import  statements
import sys     # Each  one on a line

# Module  level  Variables. (Write  this  statement  verbatim .)
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab01')

def find(pattern: str) -> list:
    input_file = open(os.path.join(DataPath,'sequence.txt'), 'r') #Open the input file
    seq = str(input_file.read()) #load sequence into memory
    test_list = [] #initialize empty lists
    final_list = []

    for i in range(len(pattern), len(seq) + 1):
        test_list.append(seq[i-len(pattern): i]) #Add each possible match to the test list

    #now test each value to see if it matches the given pattern
    for value in test_list:
        val_matches = True
        for k in range(len(pattern)):
            if pattern[k] == 'X':
                continue
            elif pattern[k] != value[k]:
                val_matches = False
                break
        if val_matches:
            final_list.append(value) #add matches to the final list

    input_file.close()
    return final_list


def getStreakProduct(sequence: str, maxSize: int, product: int) -> list:
    test_list = []
    final_list = []

    for i in range(len(sequence) - 1):
        for j in range(1, maxSize):
            if i+j == len(sequence):
                break
            else:
                test_list.append(sequence[i:i+j+1]) #add to test list

    for test_value in test_list:
        #get mathcing products and place them in the final list
        test_product = int(test_value[0]) * int(test_value[1])
        for k in range(2, len(test_value)):
            test_product *= int(test_value[k])
        if test_product == product:
            final_list.append(test_value)

    return final_list

def writePyramids(filePath: str, baseSize: int, count: int, char: str):
    output_file = open(filePath, 'w')
    one_line = list(' ' * baseSize) #create a list of space characters

    for i in range(int(baseSize / 2) + 1):
        one_line[int(baseSize / 2) + i] = char #add the characters starting at the middle for the top line
        one_line[int(baseSize / 2) - i] = char
        output_file.write(''.join(one_line))    #print to the file for each pyramid after creating the string
        for j in range(count - 1):
            output_file.write(' ' + ''.join(one_line))
        output_file.write('\n')

    output_file.close()

def getStreaks(sequence: str, letters: str) -> list:
    #start scanning the sequence for a matching character

    final_list = []     #final return list
    test_list = []      #list of all streaks, will be tested for matches to the given letters
    streak_list = []    #list used to construct streak strings

    for i in range(len(sequence)):
        if not streak_list: #if streak list is empty, start it
            streak_list.append(sequence[i])
        elif streak_list[0] == sequence[i]: #if not empty, check to see if it matches the current character
            streak_list.append(sequence[i])
        else: #if it doesn't match, place current streak in the test_list and clear it
            test_list.append(''.join(streak_list))
            streak_list = []
            streak_list.append(sequence[i])

    test_list.append(''.join(streak_list)) #place last streak in the test_list

    for value in test_list:
        if value[0] in letters: #test each streak to see if they match the letters provided
            final_list.append(value)

    return final_list

def findNames(nameList: list, part: str, name: str) -> list:

    final_list = []

    for test_name in nameList:
        first_matches = False
        last_matches = False
        test_list = test_name.split(' ') #Split the name into first and last

        #see if first and last match
        if test_list[0].upper() == name.upper():
            first_matches = True
        if test_list[1].upper() == name.upper():
            last_matches = True

        #Place into final_list if the correct part is matched
        if 'F' in part and first_matches:
            final_list.append(test_name)
        elif 'L' in part and last_matches:
            final_list.append(test_name)

    return final_list

def convertToBoolean(num: int, size: int) -> list:

    #input validation
    if (not isinstance(num, int) or not isinstance(size, int)):
        return []

    binary_list = list(bin(num)[2:]) #convert to binary string representation using bin() and remove the 0b from the beginning
    boolean_list = []

    for i in range(size - len(binary_list)): #pad with zeros until it is the correct length
        binary_list.insert(0, '0')
    for j in range(len(binary_list)):
        boolean_list.append(bool(int(binary_list[j]))) #convert the integer string list to a boolean list

    return boolean_list

def convertToInteger(boolList: list) -> int:

    #input validation
    if (not isinstance(boolList, list)):
        return None
    elif (len(boolList) == 0):
        return None
    else:
        for val in boolList:
            if not isinstance(val, bool):
                return None

    final_value = 0
    bit_num = 0
    boolList.reverse() #reverse list to process lsb first
    for boolVal in boolList:
        final_value += pow(2, bit_num) * int(boolVal)
        bit_num += 1

    return final_value

if __name__ == "__main__" :
    find('1XX3')
    #print(getStreakProduct('1212141', 4, 4))
    #writePyramids('/home/ecegridfs/a/ee364d22/Documents/prelabs-mcupka/Prelab01/testPry.txt', 15, 5, '*'# )
    #sequence = "AAASSSSSSAPPPSSPPBBCCCSSS"
    #print(getStreaks(sequence, "PAZ"))
    #names = ["George Smith", "Mark Johnson", "Cordell Theodore", "Maria Satterfield", "Johnson Cadence"]
    #print(findNames(names, 'FL', 'Maria'))
    #a = convertToBoolean(1326868, 100)
    #b = convertToInteger(a)
    #print(b)