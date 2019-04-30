#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        4/10/19
#######################################################
import sys
import os
import re
from functools import total_ordering
from measurement import *

DataPath = os.path.expanduser('~ee364/DataFolder/Lab13')

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

    def __init__(self, company, source, destination):
        mat = re.search(r', [A-Z]{2} ([0-9]{5})', source)
        szip = mat.group(1)
        mat = re.search(r', [A-Z]{2} ([0-9]{5})', destination)
        dzip = mat.group(1)

        self.company = company
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

    def __add__(self, other):
        if not (isinstance(other, Package) or isinstance(other, PackageGroup)):
            raise TypeError('Both operands must by of type Package')
        if not (self.company == other.company):
            raise ValueError('Packages must belong to the same company')

        if isinstance(other, Package):
            return PackageGroup(self.company, [self, other])
        else:
            return other + self

    def __lt__(self, other):
        if not isinstance(other, Package):
            raise TypeError("Must compare packages")
        else:
            return self.cost < other.cost

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

    def getStates(self):
        mat = re.search(r', ([A-Z]{2}) [0-9]{5}', self.source)
        sadd = mat.group(1)
        mat = re.search(r', ([A-Z]{2}) [0-9]{5}', self.destination)
        dadd = mat.group(1)

        return sadd, dadd

    def getCities(self):
        mat = re.search(r', ([A-Za-z].*), [A-Z]{2} [0-9]{5}', self.source)
        scit = mat.group(1)
        mat = re.search(r', ([A-Za-z].*), [A-Z]{2} [0-9]{5}', self.destination)
        dcit = mat.group(1)

        return scit, dcit


@total_ordering
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

    def __contains__(self, item):
        if not isinstance(item, Package):
            raise TypeError('Operand must be package')
        for p in self.packages:
            if ((p.source == item.source) and (p.destination == item.destination) and (p.company == item.company)):
                return True
        return False

    def __add__(self, other):
        if not isinstance(other, Package):
            raise TypeError('Can only add packages to package group')
        if not (other.company == self.company):
            raise ValueError('Must be the same company as the group to add')
        if other in self:
            return self

        self.packages.append(other)
        self.cost += other.cost
        self.packages.sort()

        return self


    def __radd__(self, other):
        return self + other

    #rich comp for sorting list of PGs
    def __lt__(self, other):
        if not isinstance(other, PackageGroup):
            raise TypeError("Must compare packagegroups")
        else:
            return self.company < other.company

    def __eq__(self, other):
        if not isinstance(other, PackageGroup):
            raise TypeError("Must compare packagegroups")
        else:
            return self.company == other.company

    def getByZip(self, zips):
        if zips == None or len(zips) == 0:
            raise ValueError('Set must be filled')

        matches = []

        for p in self.packages:
            pzips = p.getZips()
            if pzips[0] in zips or pzips[1] in zips:
                matches.append(p)

        matches.sort()
        return matches

    def getByState(self, states):
        if states == None or len(states) == 0:
            raise ValueError('Set must be filled')

        matches = []

        for p in self.packages:
            padds = p.getStates()
            if padds[0] in states or padds[1] in states:
                matches.append(p)

        matches.sort()
        return matches

    def getByCity(self, cities):
        if cities == None or len(cities) == 0:
            raise ValueError('Set must be filled')

        matches = []

        for p in self.packages:
            pcities = p.getCities()
            if pcities[0] in cities or pcities[1] in cities:
                matches.append(p)

        matches.sort()
        return matches


def loadPackages():
    p_file = open(os.path.join(DataPath, f'packages.dat'))
    data = p_file.read()
    data = data.split('\n')
    data = data[1:]

    #get all company names
    companies = set()

    for line in data:
        mat = re.search('"(.+)" , ".+", ".+"', line)
        companies.add(mat.group(1))

    pgList = []
    for c in companies:
        pgList.append(PackageGroup(c, []))

    for line in data:
        mat = re.search('"(.+)" , "(.+)", "(.+)"', line)
        p = Package(mat.group(1), mat.group(2), mat.group(3))
        for pg in pgList:
            if pg.company == p.company:
                pg + p

    p_file.close()
    pgList.sort()
    return pgList


if __name__ == "__main__":
    szip = '99337'
    dzip = '35115'
    print(getCost(szip, dzip))
    p = Package("APPLE", '782 W. Purple Finch Street, Crystal Lake, IL 60014', '9328 West Railroad St., Wilson, NC 27893')
    q = Package('APPLE','782 W. Purple Finch Street, Crystal Lake, IL 60014', '826 Winchester Ave., Grand Island, NE 68801')
    print(p)
    print(q < p)

    packs = [p, q]
    company = 'APPLE'
    pg = PackageGroup(company, packs)
    print(pg)
    print(pg.getByZip(set(['27893', '68801'])))
    print('NEW')
    print(p+q)
    print(q in pg)
    f = Package('APPLE','123 W. Purple Finch Street fdsafl Lake, IL 60014', '321 Winchester Ave., Grand Island, NE 68801')
    print(f in pg)


    print('getbyzip')
    print(pg.getByZip(set(['60014'])))
    print('getbystates')
    print(pg.getByState(set(['NC'])))
    print('getbycities')
    print(pg.getByCity(set(['Wilson'])))

    print(pg)
    print(pg)

    filePgs = loadPackages()
    print(filePgs)



