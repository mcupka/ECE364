#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        2/15/19
#######################################################
import os
import sys
import re
from uuid import UUID

DataPath = os.path.expanduser('~ee364/DataFolder/Prelab06') #Data Poth

def getUrlParts(url: str) -> tuple:
    pattern = r'http://(?P<BaseAddress>[\w.-]+)/(?P<Controller>[\w.-]+)/(?P<Action>[\w.-]+)\?'
    search = re.search(pattern, url)
    return (search['BaseAddress'], search['Controller'], search['Action'])


def getQueryParameters(url: str) -> list:
    pattern = r'http://[\w.-]+/[\w.-]+/[\w.-]+\?((([\w.-]+)=([\w.-]+)&?)+)'
    search = re.search(pattern, url)
    params = search.group(1)
    return re.findall(r'([\w.-]+)=([\w.-]+)', params)

def getSpecial(sentence: str, letter: str) -> list:
    pattern1 = r'\b[^\W' + letter + r']\w*' + letter + r'\b'
    pattern2 = r'\b' + letter + r'\w+[^\W' + letter + r']\b'
    search = re.findall(pattern1 + r'|' + pattern2, sentence, re.IGNORECASE)
    return search

def getRealMAC(sentence: str) -> str:
    pattern1 = r'(([0-9a-fA-F]{2}:){5})([0-9a-fA-F]{2})'
    pattern2 = r'(([0-9a-fA-F]{2}-){5})([0-9a-fA-F]{2})'
    pattern = pattern1 + '|' + pattern2
    mac_address = re.search(pattern, sentence)
    if (mac_address):
        return mac_address.group(0)

# return list of rejected employee names
def getRejectedEntries() -> list:
    infile = open(os.path.join(DataPath, 'Employees.txt'))
    data = infile.read()
    name_pattern1 = r'[\w]+ [\w]+'
    name_pattern2 = r'[\w]+, [\w]+'
    names_pattern = '(' + name_pattern1 + r'|' + name_pattern2 + ')'
    pattern = names_pattern + '[,; ]+?\n'
    names = re.findall(pattern, data)
    formatted_names = []
    for n in names:
        if re.search(r',', n):
            last, first = re.findall(r'([\w]*), ([\w]*)', n)[0]
            formatted_names.append(first + ' ' + last)
        else: formatted_names.append(n)
    formatted_names.sort()
    return formatted_names


def formatName(name: str) -> str:
    if re.search(r',', name):
        last, first = re.findall(r'([\w]+), ([\w]+)', name)[0]
        formatted = first + ' ' + last
    else: formatted = name
    return formatted


def getEmployeesWithIDs() -> dict:
    infile = open(os.path.join(DataPath, 'Employees.txt'))
    data = infile.read()
    id_pattern = r'(\{?[\w]{8}-?[\w]{4}-?[\w]{4}-?[\w]{4}-?[\w]{12}\}?).*'
    name_pattern1 = r'[\w]+ [\w]+'
    name_pattern2 = r'[\w]+, [\w]+'
    names_pattern = '(' + name_pattern1 + r'|' + name_pattern2 + ')'


    pattern = names_pattern + r'[,; ]+' + id_pattern
    search = re.findall(pattern, data)


    emp_id_dict = {}
    for name, id in search:
        emp_id_dict[formatName(name)] = str(UUID(id))

    return emp_id_dict

def getEmployeesWithoutIDs() -> list:
    infile = open(os.path.join(DataPath, 'Employees.txt'))
    data = infile.read()

    #pattern is name + phone + ... | name + state + ...
    name_pattern1 = r'[\w]+ [\w]+'
    name_pattern2 = r'[\w]+, [\w]+'
    names_pattern = '(' + name_pattern1 + r'|' + name_pattern2 + ')'
    phone_pattern = r'(\d{3}-\d{3}-\d{4}|\(\d{3}\) \d{3}-\d{4}|\d{10})'
    state_pattern = r'(\w+ ?\w*)'

    pattern1 = names_pattern + '[,; ]+' + phone_pattern + '.*\n'
    pattern2 = names_pattern + '[,; ]+' + state_pattern + ',*\n'

    name_phone = re.findall(pattern1, data)
    name_state = re.findall(pattern2, data)

    name_list = []

    for name, _ in name_phone:
        name_list.append(formatName(name))
    for name, _ in name_state:
        name_list.append(formatName(name))

    name_list.sort()
    return name_list

def getEmployeesWithPhones() -> dict:
    infile = open(os.path.join(DataPath, 'Employees.txt'))
    data = infile.read()

    # pattern is name.....phone...
    name_pattern1 = r'[\w]+ [\w]+'
    name_pattern2 = r'[\w]+, [\w]+'
    names_pattern = '(' + name_pattern1 + r'|' + name_pattern2 + ')'
    phone_pattern = r'(\d{3}-\d{3}-\d{4}|\(\d{3}\) \d{3}-\d{4}|\d{10})'

    pattern = names_pattern + r'.+' + phone_pattern

    search = re.findall(pattern, data)

    name_phone_dict = {}
    for name, phone in search:
        name_phone_dict[formatName(name)] = formatPhone(phone)

    return name_phone_dict


def formatPhone(phone: str) -> str:
    pattern = '(\d{3})-(\d{3})-(\d{4})|\((\d{3})\) (\d{3})-(\d{4})|(\d{3})(\d{3})(\d{4})'
    search = re.findall(pattern, phone)
    area_code = search[0][0] + search[0][3] + search[0][6]
    phone_1 = search[0][1] + search[0][4] + search[0][7]
    phone_2 = search[0][2] + search[0][5] + search[0][8]
    return '(' + area_code + ') ' + phone_1 + '-' + phone_2


def getEmployeesWithStates() -> dict:
    infile = open(os.path.join(DataPath, 'Employees.txt'))
    data = infile.read()

    # pattern is name.....state\n
    name_pattern1 = r'[\w]+ [\w]+'
    name_pattern2 = r'[\w]+, [\w]+'
    names_pattern = '(' + name_pattern1 + r'|' + name_pattern2 + ')'
    state_pattern1 = r'[,; ](\w+ \w+)\n'
    state_pattern2 = r'[,; ](\w+)\n'


    name_state_dict = {}
    search1 = re.findall(names_pattern + r'.*' + state_pattern1, data)
    search2 = re.findall(names_pattern + r'.*' + state_pattern2, data)


    #fill dict with pattern for one work states, then override for states with two names
    for name, state in search2:
        name_state_dict[formatName(name)] = state
    for name, state in search1:
        name_state_dict[formatName(name)] = state

    return name_state_dict

def getCompleteEntries() -> dict:
    infile = open(os.path.join(DataPath, 'Employees.txt'))
    data = infile.read()
    name_pattern1 = r'[\w]+ [\w]+'
    name_pattern2 = r'[\w]+, [\w]+'
    names_pattern = '(' + name_pattern1 + r'|' + name_pattern2 + ')'
    phone_pattern = r'(\d{3}-\d{3}-\d{4}|\(\d{3}\) \d{3}-\d{4}|\d{10})'

    pattern = names_pattern + r'[,; ]+([0-9a-fA-f{}:-]+)[,; ]+' + phone_pattern + '[,; ]+([\w ]+)\n'
    search = re.findall(pattern, data)

    complete_dict = {}

    for name, id, phone, state in search:
        complete_dict[formatName(name)] = (str(UUID(id)), formatPhone(phone), state)

    return complete_dict


if __name__ == '__main__':
    url = "http://www.purdue.edu/Home/Calendar?Year=2016&Month=September&Semester=Fall"
    url_parts = getUrlParts(url)
    print(url_parts, type(url_parts))
    url = "http://www.google.com/Math/Const?Pi=3.14&Max_Int=65536&What_Else=Not-Here"
    q_params = getQueryParameters(url)
    print(q_params, type(q_params), type(q_params[0]))
    s = "The TART program runs on Tuesdays and Thursdays, but it does not start until next week."
    spec = getSpecial(s, 't')
    print(spec, type(spec), type(spec[0]))
    mac_addr = getRealMAC('This is a MAC Address: da-23-54-FE-CE-DA. That Was a Mac Address')
    print(mac_addr)
    print(getRejectedEntries())
    print(getEmployeesWithIDs())
    print(getEmployeesWithoutIDs())
    print(getEmployeesWithPhones())
    print(getEmployeesWithStates())
    print(getCompleteEntries())