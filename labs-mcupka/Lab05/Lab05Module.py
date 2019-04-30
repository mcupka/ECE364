#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        2/13/19
#######################################################
import os
import sys

# Module  level  Variables.
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Lab05')

def getPeopleData() -> dict:
    p_file = open(os.path.join(DataPath, 'people.dat'))
    people_raw = p_file.read().split('\n')
    del people_raw[0:2]
    del people_raw[-1]

    people_dict = {}

    for line in people_raw:
        sp_line = line.split('|')
        people_dict[sp_line[0].strip()] = sp_line[1].strip()

    return people_dict

def getPinData() -> dict:
    pin_file = open(os.path.join(DataPath, 'pins.dat'))
    pins_raw = pin_file.read().split('\n')

    pin_dict = {}

    del pins_raw[0:1]
    dates = pins_raw[0].split(' ')
    dates_true = []
    for el in dates:
        if (el.find('/')) != -1:
            dates_true.append(el)

    for el in dates_true:
        pin_dict[el] = {}

    del pins_raw[0:2]
    for line in pins_raw:
        p_line = line.split(' ')
        line_true = []
        for el in p_line:
            if el != '':
                line_true.append(el)
        per_id = line_true[0]
        for index, pin in enumerate(line_true[1:]):
            date = dates_true[index]
            (pin_dict[date])[per_id] = pin

    return pin_dict


def getPinFor(name, date) -> str:
    people_dict = getPeopleData()
    pin_dict = getPinData()
    if name not in people_dict.keys():
        raise ValueError('Name not in list')
    if date not in pin_dict.keys():
        raise ValueError('Date not in list')

    id = people_dict[name]
    return str(pin_dict[date][id])

def getUserOf(pin, date):
    people_dict = getPeopleData()
    pin_dict = getPinData()
    pin_set = set()
    for date_dict in pin_dict.values():
        for p in date_dict.values():
            pin_set.add(p)

    if pin not in pin_set:
        raise ValueError('Pin not in list')
    if date not in pin_dict.keys():
        raise ValueError('Date not in list')

    date_dict = pin_dict[date]
    id = -1
    for k, val in date_dict.items():

        if (val == pin):
            id = k

    if id== -1:
        raise ValueError("id not in date")

    for k, val in people_dict.items():
        if (val == id):
            return k

def getUsersOn(date):
    people_dict = getPeopleData()
    pin_dict = getPinData()
    log_ent = getLogData()

    if date not in pin_dict.keys():
        raise ValueError("date not in file")

    pin_set = set()


    for (ldate, res, pin) in log_ent:
        if ldate == date:
            pin_set.add(pin)


    id_set = set()

    date_dict = pin_dict[date]

    for id, pnum in date_dict.items():
        if pnum in pin_set:
            id_set.add(id)

    name_set = set()

    for k, val in people_dict.items():
        if val in id_set:
            name_set.add(k)

    return name_set

def getResourcesOn(date):
    people_dict = getPeopleData()
    pin_dict = getPinData()
    log_ent = getLogData()

    if date not in pin_dict.keys():
        raise ValueError("date not in file")

    res_set = set()


    for (ldate, res, pin) in log_ent:
        if ldate == date:
            res_set.add(res)
    return res_set




def getLogData() -> set:
    pin_dict = getPinData()
    log_file = open(os.path.join(DataPath, 'log.dat'))
    log_raw = log_file.read().split('\n')

    del log_raw[0:3]

    log_entries = []

    for line in log_raw:
        p_line = line.split(' ')
        line_true = []
        for el in p_line:
            if el != '': line_true.append(el)
        date = line_true[0]
        res = line_true[2]
        pin_num = line_true[3]
        log_entries.append((date, res, pin_num))
    return log_entries


if __name__ == "__main__":
    print(getPinFor('Roberts, Teresa', '01/17'))
    print(getUserOf('710', '03/18'))
    print(getUsersOn('04/15'))
    print(getResourcesOn('03/03'))