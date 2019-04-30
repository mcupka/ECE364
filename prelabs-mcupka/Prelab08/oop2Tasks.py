#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        2/27/19
#######################################################
import os
import sys
from enum import Enum
from functools import total_ordering
from collections import UserList
from statistics import mean

@total_ordering
class Datum():
    def __init__(self, *args):
        valid_floats = []
        for arg in args:
            if type(arg) == float:
                valid_floats.append(arg)
            else: raise ValueError('All members of datum must be floats')
        self._storage = tuple(valid_floats)


    def __str__(self):
        string = '('
        for index, fl in enumerate(self._storage):
            string += '{:.02f}'.format(fl)
            if index != len(self._storage) - 1: string += ', '
        string += ')'
        return string

    def __repr__(self):
        string = '('
        for index, fl in enumerate(self._storage):
            string += '{:.02f}'.format(fl)
            if index != len(self._storage) - 1: string += ', '
        string += ')'
        return string

    def __hash__(self):
        return hash(self._storage)

    def distanceFrom(self, dat2):
        if (type(dat2) != Datum):
            raise TypeError('Argument must be type Datum')
        diffs = []
        if len(self._storage) > len(dat2._storage):
            for _ in self._storage: diffs.append(0)
        else:
            for _ in dat2._storage: diffs.append(0)

        for index, val in enumerate(self._storage):
            diffs[index] += (val)
        for index, val in enumerate(dat2._storage):
            diffs[index] -= val
        for index, _ in enumerate(diffs):
            diffs[index] = pow(diffs[index], 2)
        return pow(sum(diffs), .5)

    def clone(self):
        return Datum(*self._storage)

    def __contains__(self, item):
        if type(item) != float: raise TypeError('Operand must by type float')
        return item in self._storage
    def __len__(self):
        return len(self._storage)
    def __iter__(self):
        return iter(self._storage)
    def __neg__(self):
        return Datum(*tuple(-v for v in self._storage))
    def __getitem__(self, index):
        return self._storage[index]
    def __add__(self, other):
        if type(other) != Datum and type(other) != float: raise TypeError('operands must be type Datum or float')
        if isinstance(other, Datum):
            if len(other) > len(self): full_list = list(0 for _ in other)
            else: full_list = list(0.0 for _ in self)
            for index, a in enumerate(self): full_list[index] += a
            for index, b in enumerate(other): full_list[index] += b
            return Datum(*full_list)
        elif isinstance(other, float):
            return (Datum(*tuple((other + v) for v in self._storage)))

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if type(other) != Datum and type(other) != float: raise TypeError('operands must be type Datum or float')
        if isinstance(other, Datum):
            if len(other) > len(self): full_list = list(0 for _ in other)
            else: full_list = list(0.0 for _ in self)
            for index, a in enumerate(self): full_list[index] += a
            for index, b in enumerate(other): full_list[index] -= b
            return Datum(*full_list)
        elif isinstance(other, float):
            return Datum(*tuple((v - other) for v in self._storage))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if not isinstance(other, float): raise TypeError('operand must by type float')
        return Datum(*tuple((v * other) for v in self._storage))

    def __rmul__(self, other):
        return  self * other

    def __truediv__(self, other):
        return self * (1.0 / other)

    def __rtruediv__(self, other):
        if not isinstance(other, float): raise TypeError('operand must by type float')
        return Datum(*tuple((other / v) for v in self._storage))

    # rich comparison operators
    def __eq__(self, other):
        if not isinstance(other, Datum): raise TypeError('Operand must by type Datum')
        return self.distanceFrom(Datum(0.0)) == other.distanceFrom(Datum(0.0))
    def __lt__(self, other):
        if not isinstance(other, Datum): raise TypeError('Operand must by type Datum')
        return self.distanceFrom(Datum(0.0)) < other.distanceFrom(Datum(0.0))

    def extend_length(self, length):
        full = [0.0 for _ in range(length)]
        for index, el in enumerate(self._storage):
            full[index] = el
        return Datum(*full)

# Done with part 1

class Data(UserList):

    def __init__(self, datalist = None):
        if datalist == None: super().__init__([])
        elif type(datalist) != list: raise TypeError('Argument must be list of Datums')
        else:
            for el in datalist:
                if type(el) != Datum: raise TypeError('Argument must be list of Datums')
        super().__init__(datalist)

    def computeBounds(self):
        max_len = max(list(len(d) for d in self))
        extended_datums = [d.extend_length(max_len) for d in self]
        min_coords = [None for _ in range(max_len)]
        max_coords = [None for _ in range(max_len)]
        for index, axis_vals in enumerate(zip(*extended_datums)):
            min_coords[index] = min(axis_vals)
            max_coords[index] = max(axis_vals)
        return (Datum(*tuple(min_coords)), Datum(*tuple(max_coords)))

    def computeMean(self):
        max_len = max(list(len(d) for d in self))
        extended_datums = [d.extend_length(max_len) for d in self]
        avg_coords = [None for _ in range(max_len)]
        for index, axis_vals in enumerate(zip(*extended_datums)):
            avg_coords[index] = mean(axis_vals)
        return Datum(*avg_coords)

    def append(self, item):
        if not isinstance(item, Datum): raise TypeError('Can only append Datums to Data type')
        else: super().append(item)
    def count(self, item):
        if not isinstance(item, Datum): raise TypeError('Can only append Datums to Data type')
        else: super().count(item)
    def index(self, item):
        if not isinstance(item, Datum): raise TypeError('Can only append Datums to Data type')
        else: super().index(item)
    def insert(self, item):
        if not isinstance(item, Datum): raise TypeError('Can only append Datums to Data type')
        else: super().insert(item)
    def remove(self, item):
        if not isinstance(item, Datum): raise TypeError('Can only append Datums to Data type')
        else: super().remove(item)
    def __setitem__(self, item):
        if not isinstance(item, Datum): raise TypeError('Can only append Datums to Data type')
        else: super().__setitem__(item)

    def extend(self, item):
        if not isinstance(item, Data): raise TypeError('Argument must be type Data')
        else: super().extend(item)


class DataClass(Enum):
    Class1 = 1
    Class2 = 2

class DataClassifier:
    def __init__(self, group1 = None, group2 = None):
        if (group1 == None or group2 == None) or (not group1 or not group2): raise ValueError('Must have two non-empty arguments')
        elif not isinstance(group1, Data) or not isinstance(group2, Data): raise TypeError('Both arguments must be Data objects')
        else:
            self._class1 = group1
            self._class2 = group2

    def classify(self, datum):
        mean_dists = []
        mean_dists.append(datum.distanceFrom(self._class1.computeMean()))
        mean_dists.append(datum.distanceFrom(self._class2.computeMean()))
        if mean_dists.index(min(mean_dists)) == 0: return DataClass.Class1
        if mean_dists.index(min(mean_dists)) == 1: return DataClass.Class2





if __name__ == '__main__':
    dat = Datum(1.0, 1.0, 5.0, 8.0)
    dat2 = Datum(0.0, 5.0, 5.0)
    print(dat)
    print(hash(dat))
    print(dat.distanceFrom(dat2))
    print(dat2.clone())
    print(0.0 in dat2)
    print(len(dat2))
    for item in dat2: print(item)
    print(-dat)
    print(dat2[2])
    print(dat2 - dat)
    print('-------------')
    print(dat + 8.0)
    print(1.0 - dat)
    print(2.0 * dat)
    print('---DIV---')
    print(dat / 2.0)
    print(2.0 / dat)
    print('--------RICH COMP--------')
    dat = Datum(1.0, 5.0, 5.0, 0.0)
    dat2 = Datum(1.0, 6.0, 5.0)
    print(dat2 >= dat)
    data = Data([dat, dat2])
    print(data.computeBounds())
    print(data.computeMean())
    print('--------CLASSIFIER--------')
    dat = Datum(500.0, 500.0, 500.0, 500.0)
    dat2 = Datum(12.0, 16.0, 65.0)
    dat3 = Datum(19.0, 35.0, 45.0, 30.0)
    dat4 = Datum(51.0, 26.0, 25.0)
    data = Data([dat, dat2])
    data2 = Data([dat3, dat4])
    classifier = DataClassifier(data, data2)
    print(data.computeMean())
    print(data2.computeMean())
    print(classifier.classify(Datum(1000.0, 1000.0, 1000.0, 10000.0)))



