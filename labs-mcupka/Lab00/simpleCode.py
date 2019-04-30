#!/usr/bin/env python3.7

#######################################################
#   Author:     Alex Gheith
#   email:      gheith@purdue.edu
#   ID:         ee364j20
#   Date:       01/07/2019
#######################################################

import os
import math
from operator import itemgetter


def getVectorNorm(vector):
    """
    Calculates and returns the norm of the vector passed.

    :param vector: Vector of size 'n', containing floats.
    :return: Second Geometric Norm of the input vector.
    """
    # Get the vector norm, which is the square-root of the sum of the elements squared.

    squaredVector = [i ** 2 for i in vector]

    squaredSum = sum(squaredVector)

    vectorNorm = math.sqrt(squaredSum)

    return vectorNorm


def getMaxFrequency(numbers):
    """
    Finds the value with maximum number of occurrences in the list of integers passed.

    :param numbers: List of integers containing duplicates.
    :return: The value that occurs most frequently.
    """

    distinct = set(numbers)

    frequencies = [(n, numbers.count(n)) for n in distinct]

    result, _ = max(frequencies, key=itemgetter(1))

    return result


if __name__ == "__main__":

    values = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    norm = getVectorNorm(values)

    randomIDs = [8420, 9251, 7591, 5283, 6523, 5116, 6406, 5029,
                 2887, 7591, 5116, 7254, 6523, 8228, 4340, 4340,
                 5116, 5283, 7254, 9251, 4097, 7805, 5029, 5283,
                 7254, 7591, 6523, 9251, 4340, 4097, 5339, 7805,
                 8228, 5116, 9285, 7591, 4097, 8420, 5283, 7796,
                 5028, 3451, 5430, 5339, 7591, 5283, 6406, 7591,
                 5116, 4340, 6523, 7796, 5116, 8420, 5029, 8228,
                 2887, 7796, 8420, 7805, 6523, 8420, 7254, 5283,
                 2887, 9285, 2887, 6406, 8420, 5283, 5029, 9251]
    print("Done!")

    mostFrequent = getMaxFrequency(randomIDs)