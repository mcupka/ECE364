
from math import *


def calculateDistance(zip1, zip2):
    """
    Calculates the distance between two zip codes and returns the result as a float in miles.
    :param zip1: A tuple holding the (latitude, longitude) values of the first zip code.
    :param zip2: A tuple holding the (latitude, longitude) values of the second zip code.
    :return: The distance between the two zip codes in miles.
    :raise: A ValueError if either of the zip codes is not a 2-tuple of floats.
    """

    if not isinstance(zip1, tuple) or not isinstance(zip2, tuple) or len(zip1) != 2 or len(zip2) != 2:
        raise ValueError("One or more input argument does not follow the right format.")

    lat_A, long_A, lat_B, long_B = [radians(v) for v in zip1 + zip2]
    distance = sin(lat_A) * sin(lat_B) + cos(lat_A) * cos(lat_B) * cos(long_A - long_B)

    distance = (degrees(acos(distance))) * 69.09

    return distance

