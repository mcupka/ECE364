#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        1/23/19
#######################################################
import os
import sys
import operator

# Module  level  Variables.
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Lab02')

def getCodeFor(stateName: str) -> list:

    #Get the data from the file
    data_file = open(os.path.join(DataPath, 'zip.dat'), 'r')
    all_data = data_file.read().split('\n')
    del all_data[0:2]



    #find matches
    matching_zips = []
    for zipCode in all_data:
        split_data = zipCode.split(' ')
        if split_data[0] == stateName:
            matching_zips.append(split_data[-1])
        else:
             if split_data[0] + ' ' + split_data[1] == stateName:
                matching_zips.append(split_data[-1])

    #sort
    matching_zips.sort()

    return matching_zips

def getMinLatitude(stateName: str) -> float:
    data_file = open(os.path.join(DataPath, 'coordinates.dat'), 'r')
    all_data = data_file.read().split('\n')
    del all_data[0:2]

    codes_for_state = getCodeFor(stateName)

    matching_lats = []
    for zip in all_data:
        remove_ws = ' '.join(zip.split())
        split_data = remove_ws.split(' ')
        if split_data[-1] in codes_for_state:
            matching_lats.append(split_data[0])

    # convert to floats for sorting
    float_list = []
    for lat in matching_lats:
        float_list.append(float(lat))

    #sort latitudes
    float_list.sort()
    return float_list[0]

def getMaxLongitude(stateName: str) -> float:
    data_file = open(os.path.join(DataPath, 'coordinates.dat'), 'r')
    all_data = data_file.read().split('\n')
    del all_data[0:2]

    codes_for_state = getCodeFor(stateName)

    matching_longs = []
    for zip in all_data:
        remove_ws = ' '.join(zip.split())
        split_data = remove_ws.split(' ')
        if split_data[-1] in codes_for_state:
            matching_longs.append(split_data[1])

    # convert list to floats so sorting works correctly
    float_list = []
    for long in matching_longs:
        float_list.append(float(long))
    #sort latitudes
    float_list.sort()
    return float_list[-1]

def getSubMatrixSum(startRowIndex: int, endRowIndex: int, startColumnIndex: int, endColumnIndex: int) -> int:
    data_file = open(os.path.join(DataPath, 'matrix.dat'), 'r')
    all_data = data_file.read().split('\n')

    matching_rows = all_data[startRowIndex: endRowIndex + 1]
    matching_matrix = []

    sum = 0

    for row in matching_rows:
        split_data = row.split(' ')
        for col in range(100):
            if (col >= startColumnIndex and col <= endColumnIndex):
                sum += int(split_data[col])

    return sum

if __name__ == "__main__":
    a = getCodeFor('New York')
    print(a)
    b = getMinLatitude('New York')
    print(b)
    c = getMaxLongitude('New York')
    print(c)
    d = getSubMatrixSum(0, 99, 0, 99)
    print(d)