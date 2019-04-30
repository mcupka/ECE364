#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        4/17/19
#######################################################
import os
import sys
from enum import Enum
from measurement import *
import re
from functools import total_ordering

DataPath = os.path.expanduser('~ee364/DataFolder/Lab14')


class Direction(Enum):
    Incoming = 0
    Outgoing = 1
    Both = 2

def getZip(addr):
    mat = re.search(r', \w{2} ([0-9A-Za-z]{5})', addr)
    return mat.group(1)

def getState(addr):
    mat = re.search(r', (\w{2}) [0-9A-Za-z]{5}', addr)
    return mat.group(1)


class Leg:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def __str__(self):
        return getZip(self.source) + ' => ' + getZip(self.destination)

    def __repr__(self):
        return getZip(self.source) + ' => ' + getZip(self.destination)

    def calculateLength(self, locationMap):
        src_coord = locationMap[getZip(self.source)]
        dest_coord = locationMap[getZip(self.destination)]
        dist = calculateDistance(src_coord, dest_coord)
        return round(dist, 2)

@total_ordering
class Trip:
    def __init__(self, person, legs):
        self.person = person
        self.legs = legs

    def calculateLength(self, locationMap):
        dist = 0
        for l in self.legs:
            dist += l.calculateLength(locationMap)
        dist = round(dist, 2)
        return dist

    def getLegsByZip(self, zipc, direction):
        matches = []
        for l in self.legs:
            if (direction == Direction.Incoming):
                if getZip(l.destination) == zipc: matches.append(l)
            elif (direction == Direction.Outgoing):
                if getZip(l.source) == zipc: matches.append(l)
            elif (direction == Direction.Both):
                if (getZip(l.destination) == zipc or getZip(l.source) == zipc): matches.append(l)
        return matches

    def getLegsByState(self, state, direction):
        matches = []
        for l in self.legs:
            if (direction == Direction.Incoming):
                if getState(l.destination) == state: matches.append(l)
            elif (direction == Direction.Outgoing):
                if getState(l.source) == state: matches.append(l)
            elif (direction == Direction.Both):
                if (getState(l.destination) == state or getZip(l.source) == state): matches.append(l)
        return matches

    def __radd__(self, other):
        return self + other

    def __add__(self, other):
        if (isinstance(other, Leg)):
            if (other.source == self.legs[-1].destination):
                ls = self.legs
                ls.append(other)
                return Trip(self.person, ls)
            else:
                raise ValueError('Leg must match current legs')
        elif (isinstance(other, Trip)):
            if (self.person == other.person):
                legs = []
                for l in other.legs:
                    legs.append(l)
                return Trip(self.person, l)
            else:
                raise ValueError('Person must be the same')
        else:
            raise TypeError('Invalid types')

    def __gt__(self, other):
        locationMap = getLMap()
        return self.calculateLength(locationMap) > other.calculateLength(locationMap)
    def __eq__(self, other):
        locationMap = getLMap()
        return self.calculateLength(locationMap) == other.calculateLength(locationMap)



class RoundTrip(Trip):

    def __init__(self, person, legs):
        if (len(legs) > 1 and legs[-1].destination == legs[0].source):
            super().__init__(person, legs)
        else:
            raise ValueError('Trip must be round')



def getShortestTrip(source, destination, stops):
    trip_list = []
    for a in stops:
        trip_list.append(Trip('', [Leg(source, a), Leg(a, destination)]))
    trip_list.sort()
    return trip_list[0]

def getLMap():
    l_file = open(os.path.join(DataPath, f'locations.dat'))
    data = l_file.read().split('\n')
    data = data [1:]
    data = data[:-1]
    locationMap = {}
    for line in data:
        lzip = re.search("[0-9A-Za-z]{5}", line).group(0)
        lat = re.search('".+", ".+", "([\s\d\.-]+)", "[\s\d\.-]+"', line).group(1)
        long = re.search('".+", ".+", "[\s\d\.-]+", "([\s\d\.-]+)"', line).group(1)
        locationMap[lzip] = (float(lat), float(long))
    return locationMap

def getTotalDistanceFor(person):
    l_file = open(os.path.join(DataPath, f'trips.dat'))
    data = l_file.read().split('\n')
    trips = []
    dist = 0.0
    lmap = getLMap()
    for line in data:
        name = re.search('"(\w+, \w+)"', line).group(1)
        if (name == person):
            addrs = re.findall('"([\w\s\d]+,\s\w{2}\s[\w\d]{5})"', line)
            legs = []
            for i in range(len(addrs) - 1):
                legs.append(Leg(addrs[i], addrs[i+1]))
            trips.append(Trip(person, legs))
    for t in trips:
        dist += t.calculateLength(lmap)
    return dist

def getRoundTripCount():
    l_file = open(os.path.join(DataPath, f'trips.dat'))
    data = l_file.read().split('\n')
    trips = []
    count = 0
    for line in data:
        addrs = re.findall('"([\w\s\d]+,\s\w{2}\s[\w\d]{5})"', line)
        if addrs[-1] == addrs[0]:
            count += 1
    return count

if __name__ == '__main__':
    l = Leg('Hilliard, FL 32046', 'Putnam Station, NY 12861')
    l2 = Leg('Putnam Station, NY 12861', 'Hilliard, FL 32046')
    print(l)
    print(getState(l.source))
    ls = [l, l2]
    t = Trip('me', ls)
    t = RoundTrip('me', ls)
    print(t.legs)
    stps = ['Kensington, KS 66951', 'Petersburg, MI 49270', 'Perryville, MO 63775']
    print(getRoundTripCount())
    #print(getShortestTrip('Putnam Station, NY 12861', 'Hilliard, FL 32046', stps).legs)
    #print(getTotalDistanceFor('Hughes, James'))

