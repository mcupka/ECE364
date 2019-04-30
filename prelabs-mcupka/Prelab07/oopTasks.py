#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        2/15/19
#######################################################
import os
import sys
from enum import Enum

# Enumeration for class levels
class Level(Enum):
    Freshman = 0
    Sophomore = 1
    Junior = 2
    Senior = 3

class ComponentType(Enum):
    Resistor = 0
    Capacitor = 1
    Inductor = 2
    Transistor = 3


class Student:
    def __init__(self, ID, firstName, lastName, level):
        if (type(level) is not Level):
            raise TypeError('Level passed is not an enum of type \'Level\'')
        self.firstName = firstName
        self.lastName = lastName
        self.ID = ID
        self.level = level

    def __str__(self):
        return self.ID + ', ' + self.firstName + ' ' + self.lastName + ', ' + self.level.name

class Component:
    def __init__(self, ID, ctype, price):
        if (type(ctype) is not ComponentType):
            raise TypeError('Type passed is not an enum of type \'ComponentType\'')
        self.ID = ID
        self.ctype = ctype
        self.price = price

    def __str__(self):
        rounded_price = round(self.price, 2)
        return f'{self.ctype.name}, {self.ID}, ${rounded_price}'

    def __hash__(self):
        return hash(self.ID)


class Circuit:
    def __init__(self, ID, components):
        self.ID = ID
        self.cost = 0.0
        self.components = set()
        for c in components:
           if type(c) != Component:
               raise TypeError('Components set passed is not a set of \'Component\' objects')
           else:
               self.components.add(c)
               self.cost += c.price


    def __str__(self):
        rCount = 0
        cCount = 0
        iCount = 0
        tCount = 0
        r_cost = round(self.cost, 2)

        for c in self.components:
            if c.ctype == ComponentType.Resistor:
                rCount += 1
            elif c.ctype == ComponentType.Inductor:
                iCount += 1
            elif c.ctype == ComponentType.Capacitor:
                cCount += 1
            elif c.ctype == ComponentType.Transistor:
                tCount += 1

        return '{}: (R = {:02d}, C = {:02d}, I = {:02d}, T = {:02d}), Cost = ${:.2f}'.format(self.ID, rCount, cCount, iCount, tCount, r_cost)

    def getByType(self, cType):
        if type(cType) != ComponentType:
            raise ValueError('The type is not an instance of type \'ComponentType\'')
        typeSet = set()
        for c in self.components:
            if c.ctype == cType:
                typeSet.add(c)
        return typeSet

    def __contains__(self, comp):
        ids = []
        if type(comp) != Component:
            raise TypeError('Given component is not an object of type \'Component\'')
        for c in self.components:
            ids.append(c.ID)
        return (comp.ID in ids)

    def __add__(self, comp):
        if type(comp) != Component:
            raise TypeError('Component not an object of the \'Component\' class')
        if (comp not in  self):
            self.components.add(comp)
            self.cost += comp.price
        return self

    def __sub__(self, comp):
        if type(comp) != Component:
            raise TypeError('Component not an object of the \'Component\' class')
        if (comp in self):
            for c in self.components:
                if c.ID == comp.ID:
                    cRemove = c
            self.components.remove(cRemove)
            self.cost -= comp.price
        return self


    def __eq__(self, circ2):
        if type(circ2) != Circuit:
            raise TypeError('Operand not a Circuit object')
        return (self.cost == circ2.cost)

    def __gt__(self, circ2):
        if type(circ2) != Circuit:
            raise TypeError('Operand not a Circuit object')
        return (self.cost > circ2.cost)

    def __lt__(self, circ2):
        if type(circ2) != Circuit:
            raise TypeError('Operand not a Circuit object')
        return (self.cost < circ2.cost)

class Project:

    def __init__(self, ID, participants, circuits):
        self.ID = ID
        self.participants = []
        self.circuits = []
        self.cost = 0.0

        for p in participants:
            if type(p) != Student:
                raise ValueError('Participant list is not a list of Student objects')
            else:
                self.participants.append(p)

        for c in circuits:
            if type(c) != Circuit:
                raise ValueError('Circuit list is not a list of Circuit objects')
            else:
                self.circuits.append(c)
                self.cost += c.cost

    def __str__(self):
        return '{}: ({:02d} Circuits {:02d} Participants), Cost = ${:.2f}'.format(self.ID, len(self.circuits), len(self.participants), self.cost)

    def __contains__(self, other):
        contains = False
        if type(other) == Component:
            for cir in self.circuits:
                if other in cir:
                    contains = True
        elif type(other) == Student:
            for s in self.participants:
                if s.ID == other.ID:
                    contains = True
        elif type(other) == Circuit:
            for circ in self.circuits:
                if circ.ID == other.ID:
                    contains = True
        else:
            raise TypeError('Invalid operand for \'in\' operator')
        return contains

    def __add__(self, cir):
        if type(cir) != Circuit:
            raise TypeError('Circuit not an object of the \'Circuit\' class')
        if cir not in self:
            # add the circuit
            self.circuits.append(cir)
            self.cost += cir.cost
        return self


    def __sub__(self, cir):
        if type(cir) != Circuit:
            raise TypeError('Circuit not an object of the \'Circuit\' class')
        if cir in self:
            # remove the circuit
            for c in self.circuits:
                if cir.ID == c.ID:
                    removeCirc = c
            self.circuits.remove(removeCirc)
            self.cost -= cir.cost
        return self

    def __getitem__(self, ID):
        for c in self.circuits:
            if c.ID == ID:
                return c
        raise KeyError('Circuit ID not present in the project')

class Capstone(Project):

    def __init__(self, *args):
        if type(args[0]) == Project:
            self.ID = args[0].ID
            self.circuits = args[0].circuits
            self.cost = args[0].cost
            for p in args[0].participants:
                if p.level != Level.Senior:
                    raise ValueError('All students in capstone must be seniors')
            self.participants = args[0].participants
        else:
            for p in args[1]:
                if p.level != Level.Senior:
                    raise ValueError('All students in capstone must be seniors')
            super().__init__(args[0], args[1], args[2])




if __name__ == '__main__':
    stu = Student('0026907496', 'Michael', 'Cupka', Level.Junior)
    print(stu.firstName, stu.lastName, stu.level, stu.ID)
    print(str(stu))
    comp = Component('123', ComponentType.Resistor, 23.72432432)
    print(str(comp))
    print(hash(comp))
    comp2 = Component('T-69', ComponentType.Resistor, 18.99932)
    cir = Circuit('TEST-123', set([comp, comp2]))
    comp3 = Component('T-69', ComponentType.Transistor, 18.99932)
    print(str(cir), '----', comp3 in cir)
    print(cir.getByType(ComponentType.Resistor))
    print(comp2 in cir)
    cir2 = Circuit('TEST-321', set([comp, comp2]))
    cir2 = cir2 - comp + comp2 + comp + comp
    print(cir == cir2)
    for c in cir2.components:
        print(c)
    proj = Project('PROJECT X', list([stu]), list([cir, cir2]))
    for c in proj.circuits:
        print(c)
    print(str(proj))
    cir3 = Circuit('POO', set([comp, comp2]))
    stu2 = Student('123456', 'Mark', 'Beepis', Level.Freshman)
    print(cir3 in proj, stu2 in proj)
    print(proj)
    print(proj['TEST-321'])
    stu = Student('IDMAN', 'Old', 'Man', Level.Senior)
    proj = Project('PROJECT X', list([stu]), list([cir, cir2]))
    capstone = Capstone('PROJECT X', list([stu]), list([cir, cir2]))
    capstone = Capstone(proj)
    print('::::', capstone)