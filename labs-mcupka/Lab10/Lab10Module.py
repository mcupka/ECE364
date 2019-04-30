#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        3/27/19
#######################################################
import sys
import os
import re
from functools import total_ordering
from measurement import *

DataPath = os.path.expanduser('~ee364/DataFolder/Lab10')

def getCost(sourceZip, destinationZip):

    coord_file = open(os.path.join(DataPath, 'coordinates.dat'), 'r')
    data = coord_file.read()
    mat = re.search(r'"' + sourceZip + '", "\w+", "([\d\s.\-]+)", "([\d\s\-.]+)"', data)
    scord = (float(mat.group(1)), float(mat.group(2)))
    mat = re.search(r'"' + destinationZip + '", "\w+", "([\d\s.\-]+)", "([\d\s\-.]+)"', data)
    dcord = (float(mat.group(1)), float(mat.group(2)))

    miles = calculateDistance(scord, dcord)

    return round(miles * .01, 2)

@total_ordering
class Package:

    def __init__(self, source, destination):
        mat = re.search(r', [A-Z]{2} ([0-9]{5})', source)
        szip = mat.group(1)
        mat = re.search(r', [A-Z]{2} ([0-9]{5})', destination)
        dzip = mat.group(1)

        self.destination = destination
        self.source = source
        self.cost = round(getCost(szip, dzip), 2)

    def __str__(self):

        mat = re.search(r', [A-Z]{2} ([0-9]{5})', self.source)
        szip = mat.group(1)
        mat = re.search(r', [A-Z]{2} ([0-9]{5})', self.destination)
        dzip = mat.group(1)

        return szip + " => " + dzip + ", Cost = ${:.02f}".format(self.cost)

    def __repr__(self):

        mat = re.search(r', [A-Z]{2} ([0-9]{5})', self.source)
        szip = mat.group(1)
        mat = re.search(r', [A-Z]{2} ([0-9]{5})', self.destination)
        dzip = mat.group(1)

        return szip + " => " + dzip + ", Cost = ${:.02f}".format(self.cost)

    def __lt__(self, other):
        if not isinstance(other, Package):
            raise TypeError("Must compare packages")
        else:
            return self.cost > other.cost

    def __eq__(self, other):
        if not isinstance(other, Package):
            raise TypeError("Must compare packages")
        else:
            return self.cost == other.cost

    def getZips(self):
        mat = re.search(r', [A-Z]{2} ([0-9]{5})', self.source)
        szip = mat.group(1)
        mat = re.search(r', [A-Z]{2} ([0-9]{5})', self.destination)
        dzip = mat.group(1)

        return szip, dzip



class PackageGroup:

    def __init__(self, company, packages):
        self.company = company
        packages.sort()
        self.packages = packages

        cost = 0.0
        for p in packages:
            cost += p.cost

        self.cost = round(cost, 2)

    def __str__(self):
        return self.company + ', {:03} Shipments, Cost = ${:.02f}'.format(len(self.packages), self.cost)

    def __repr__(self):
        return self.company + ', {:03} Shipments, Cost = ${:.02f}'.format(len(self.packages), self.cost)

    def getByZip(self, zips):
        if zips == None:
            raise ValueError('Set must be filled')

        matches = []

        for p in self.packages:
            pzips = p.getZips()
            if pzips[0] in zips or pzips[1] in zips:
                matches.append(p)

        matches.sort()
        return matches


def getNumberPattern():

    return '[0-2][0-5][0-5].[0-2][0-5][0-5].[0-2][0-5][0-5]'


if __name__ == "__main__":
    szip = '99337'
    dzip = '35115'
    print(getCost(szip, dzip))
    p = Package('782 W. Purple Finch Street, Crystal Lake, IL 60014', '9328 West Railroad St., Wilson, NC 27893')
    q = Package('782 W. Purple Finch Street, Crystal Lake, IL 60014', '826 Winchester Ave., Grand Island, NE 68801')
    print(p)
    print(q > p)

    packs = [p, q]
    company = 'hi'
    pg = PackageGroup(company, packs)
    print(pg)
    print(pg.getByZip(set(['27893', '68801'])))

    ###RE

    pattern = getNumberPattern()
    m = re.search(pattern, 'The IP is 05.09.0.94')
    print(m[0])

