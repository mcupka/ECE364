#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        3/6/19
#######################################################
import sys
import os
from functools import total_ordering

@total_ordering
class TimeSpan:
    def __init__(self, weeks, days, hours):
        if (weeks < 0) | (weeks < 0) | (hours < 0):
            raise ValueError('Input arguments must be greater than or equal to 0.')
        self.hours = (hours % 24)
        self.days = ((days % 7) + (hours // 24)) % 7
        self.weeks = weeks + (days // 7) + ((days % 7) + (hours // 24)) // 7



    def __str__(self):
        return '{:02d}W {:01d}D {:02d}H'.format(self.weeks, self.days, self.hours)

    def getTotalHours(self):
        return self.weeks * (7 * 24) + self.days * 24 + self.hours

    def __add__(self, other):
        if not isinstance(other, TimeSpan): raise TypeError('Expected operand of type \'TimeSpan\'')
        return TimeSpan(self.weeks + other.weeks, self.days + other.days, self.hours + other.hours)

    def __mul__(self, other):
        if not isinstance(other, int) and not isinstance(other, float): raise TypeError('Operand for multiplication must be type float or int')
        if isinstance(other, int):
            if other <= 0: raise ValueError('Operand for multiplication must be greater than 0')
            return TimeSpan(self.weeks * other, self.days * other, self.hours * other)
        if isinstance(other, float):
            if other <= 0.0: raise ValueError('Operand for multiplication must be greater than 0')
            return TimeSpan(0, 0, int(round(self.getTotalHours() * other)))

    def __rmul__(self, other):
        return self * other

    # rich comparison stuff
    def __eq__(self, other):
        if not isinstance(other, TimeSpan): raise TypeError('Operand must by type \'TimeSpan\'')
        return self.getTotalHours() == other.getTotalHours()
    def __lt__(self, other):
        if not isinstance(other, TimeSpan): raise TypeError('Operand must by type \'TimeSpan\'')
        return self.getTotalHours() < other.getTotalHours()

if __name__ == '__main__':
    t1 = TimeSpan(1, 1, 2)
    print(t1)
    print(t1.getTotalHours())
    t2 = TimeSpan(2, 60, 2)
    print(t1 + t2)
    print(5 * t1)
    print((5.5 * t1).getTotalHours())
    print(t2 > t1)
