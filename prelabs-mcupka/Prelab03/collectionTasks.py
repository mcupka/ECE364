#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        1/24/19
#######################################################

import os
import sys
from collections import namedtuple


# Module level vars
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab03') #Data Poth

# helper function to return a dict where each projectID cooresponds to a list of components
def getProjectDict() -> dict:
    # open file
    project_file = open(os.path.join(DataPath, 'maps/projects.dat'))
    project_data = project_file.read()
    project_file.close()

    project_data = project_data.split('\n')
    del project_data[0:2]

    project_set = set()

    #get set of all project ids
    for line in project_data:
        parsed_line = ' '.join(line.split()).split(' ')
        project_set.add(parsed_line[1])

    #create dictianary using projectIDs as keys and empty lists as elements
    project_dict = {}
    for pID in project_set:
        project_dict[pID] = []

    #fill dict lists with component values
    for line in project_data:
        parsed_line = ' '.join(line.split()).split(' ')
        project_dict[parsed_line[1]].append(parsed_line[0])

    #return final dictionary
    return project_dict

# return a dict where key is component type and elements are named tuples of those components and their prices
def getComponentsDict() -> dict:
    # open files
    res_data = (open(os.path.join(DataPath, 'maps/resistors.dat')).read(), 'R')
    ind_data = (open(os.path.join(DataPath, 'maps/inductors.dat')).read(), 'I')
    cap_data = (open(os.path.join(DataPath, 'maps/capacitors.dat')).read(), 'C')
    tran_data = (open(os.path.join(DataPath, 'maps/transistors.dat')).read() , 'T')

    types = [res_data, ind_data, cap_data, tran_data]

    components_dict = {'R':[], 'I':[], 'C':[], 'T':[]}

    # define component tuple
    Component = namedtuple('Component', ['ID', 'Price'])

    # parse data for each comp type, add components to the list cooresponding to each component type key
    for type in types:
        parse_data = type[0].split('\n')
        del parse_data[0:3]
        for line in parse_data:
            parsed_line = ' '.join(line.split()).split(' ')
            parsed_line[1] = parsed_line[1].strip('$')
            components_dict[type[1]].append(Component(ID=parsed_line[0], Price=float(parsed_line[1])))

    return components_dict

def getCircuitInfo(circuitID: str) -> namedtuple:

    #open circuit file and read data
    cir_data = open(os.path.join(DataPath, f'circuits/circuit_{circuitID}.dat')).read().split('\n')
    del cir_data[0:2]

    Circuit = namedtuple("Circuit", ["Participants", "Components"])
    participants = []
    components = []

    # get participants
    entry = None
    while entry != '':
        entry = cir_data.pop(0)
        if entry != '': participants.append(entry.strip(' '))

    # get components
    del cir_data[0:2]
    components.extend(cir_data)
    for comp in range(len(components)):
        components[comp] = components[comp].strip(' ')

    return Circuit(Participants=participants, Components=components)


# gets info for all circuits and stores in a dict
def getCircuitDict() -> dict:
    all_circs = os.listdir(os.path.join(DataPath,'circuits'))

    circ_ids = []

    for file in all_circs:
        if file.endswith('.dat'):
            circ_ids.append(file[8:-4])

    circuit_dict = {}
    for id in circ_ids:
        circuit_dict[id] = getCircuitInfo(id)

    return circuit_dict

def getComponentCountByProject(projectID: str, componentSymbol: str) -> int:

    # get project dictionary
    project_dict = getProjectDict()

    # See if the given ID is found
    if projectID not in project_dict.keys():
        raise ValueError('Project ID not found in file')

    # get list of circuits used in the project
    circuit_list = project_dict[projectID]

    # get components dictionary
    components_dict = getComponentsDict()

    matching_comps = components_dict[componentSymbol]
    matching_ids = []
    # get ids from Component tuples
    for match in matching_comps:
        matching_ids.append(match.ID)

    circuit_dict = getCircuitDict()
    final_set = set()

    for circuit in circuit_list:
        cir_comps = circuit_dict[circuit].Components
        for comp in cir_comps:
            if comp in matching_ids: final_set.add(comp)

    return len(final_set)

# function to get dictionary of student names as keys and ids as elements
def getStudentDict() -> dict:
    student_data = open(os.path.join(DataPath, 'maps/students.dat')).read().split('\n')
    del student_data[0:2]

    student_dict = {}
    for line in student_data:
        parsed_line = line.split('|')
        if line != '':
            student_dict[parsed_line[0].strip()] = parsed_line[1].strip()


    return student_dict

def getComponentCountByStudent(studentName: str, componentSymbol: str) -> int:

    student_dict = getStudentDict()
    circuit_dict = getCircuitDict()
    comp_dict = getComponentsDict()

    if studentName not in student_dict.keys():
        raise ValueError('Student does not exist')

    student_id = student_dict[studentName]

    student_components = set()

    mathcing_comps = comp_dict[componentSymbol]
    matching_comp_IDs = []
    for comp in mathcing_comps:
        matching_comp_IDs.append(comp.ID)

    # check all circuits for matching student ids
    for circuit in circuit_dict.values():
        if student_id in circuit.Participants:
            for comp in circuit.Components:
                if comp in matching_comp_IDs:
                    student_components.add(comp)

    return len(student_components)


def getParticipationByStudent(studentName: str) -> set:
    project_dict = getProjectDict()
    student_dict = getStudentDict()
    student_id = student_dict[studentName] # get student id
    circuit_dict = getCircuitDict()

    if studentName not in student_dict.keys():
        raise ValueError('Student does not exist')

    project_set = set()

    # search through all project ids, checking each circuit for an ID match
    for key in project_dict.keys():
        circuits = project_dict[key]
        for circ in circuits:
            if student_id in circuit_dict[circ].Participants:
                project_set.add(key)

    return project_set

def getParticipationByProject(projectID: str) -> set:

    student_names = set()

    project_dict = getProjectDict()
    student_dict = getStudentDict()
    circuit_dict = getCircuitDict()

    if projectID not in project_dict.keys():
        raise ValueError('Project not found')

    for name in student_dict.keys():

        stud_projects = set()

        for key in project_dict.keys():
            circuits = project_dict[key]
            for circ in circuits:
                if student_dict[name] in circuit_dict[circ].Participants:
                    stud_projects.add(key)

        if projectID in stud_projects: student_names.add(name)

    return student_names

def getCostOfProjects() -> dict:
    project_dict = getProjectDict()
    circuit_dict = getCircuitDict()
    components_dict = getComponentsDict()
    proj_cost_dict = {} #empty dict



    comp_prices = {}
    #create dict of comps and prices
    for type in components_dict.values():
        for comp_tup in type:
            comp_prices[comp_tup.ID] = comp_tup.Price

    #for each project, create an entry in the dict where key= project id and value= cost
    for proj in project_dict:
        cost = 0.0
        for cir in project_dict[proj]:
            #get cost of circuit
            for comp_id in circuit_dict[cir].Components:
                #find component and add price to sum
                cost += comp_prices[comp_id]
        proj_cost_dict[proj] = round(cost, 2)

    return proj_cost_dict

def getProjectByComponent(componentIDs: set) -> set:
    proj_dict = getProjectDict()
    cir_dict = getCircuitDict()

    #create empty set
    project_set = set()

    #for each proj, check if any circuit has matching comps, if so, add proj to set
    for proj in proj_dict.keys():
        for cir in proj_dict[proj]:
            if any(cid in cir_dict[cir].Components for cid in componentIDs):
                project_set.add(proj)

    return project_set

def getCommonByProject(projectID1: str, projectID2: str) -> list:

    # create two sets of components, then create set of common ones, convert to list

    p1Comps = set()
    p2Comps = set()
    common_comps = set()

    proj_dict = getProjectDict()
    cir_dict = getCircuitDict()

    if projectID1 not in proj_dict.keys():
        raise ValueError('Project 1 not found')
    if projectID2 not in proj_dict.keys():
        raise ValueError('Project 2 not found')

    for cir in  proj_dict[projectID1]:
        for comp in cir_dict[cir].Components:
            p1Comps.add(comp)

    for cir in  proj_dict[projectID2]:
        for comp in cir_dict[cir].Components:
            p2Comps.add(comp)

    # get common
    for comp in p1Comps:
        if comp in p2Comps: common_comps.add(comp)

    common_comps = (p1Comps.intersection(p2Comps))
    sorted_list = list(common_comps)
    sorted_list.sort()

    return sorted_list

def getComponentReport(componentIDs: set) -> dict:

    proj_dict = getProjectDict()
    cir_dict = getCircuitDict()

    comp_report = {}

    for compIDgiven in componentIDs:
        comp_used_count = 0
        for proj in proj_dict.keys():
            for cir in proj_dict[proj]:
                for comp in cir_dict[cir].Components:
                    if compIDgiven == comp: comp_used_count += 1
        comp_report[compIDgiven] = comp_used_count

    return comp_report

def getCircuitByStudent(studentNames: set) -> set:
    stud_dict = getStudentDict()
    proj_dict = getProjectDict()
    all_circs = set()

    # for each student, add all matching circuits
    for givenStudent in studentNames:
        proj_part_in = getParticipationByStudent(givenStudent)
        for proj in proj_part_in:
            for cir in proj_dict[proj]:
                all_circs.add(cir)

    return all_circs

def getCircuitByComponent(componentIDs: set) -> set:
    cir_dict = getCircuitDict()
    all_circs = set()

    # for each comp id, add all matching circuits
    for compIDgiven in componentIDs:
        for cir in cir_dict.keys():
            for comp in cir_dict[cir].Components:
                if compIDgiven == comp: all_circs.add(cir)
    return all_circs


if __name__ == "__main__":
    print(getComponentCountByProject('DE06228A-0544-4543-9055-A39D19DEDFA4', 'I'))
    print(getComponentCountByStudent('Allen, Amanda', 'R'))
    print(getParticipationByStudent('Allen, Amanda'))
    print(getParticipationByProject('DE06228A-0544-4543-9055-A39D19DEDFA4'))
    print(getCostOfProjects())
    print(getProjectByComponent(set((['RNW-027', 'RFU-406', 'QPR-163']))))
    print(getCommonByProject('DE06228A-0544-4543-9055-A39D19DEDFA4', '96CC6F98-B44B-4FEB-A06B-390432C1F6EA'))
    print(getComponentReport(set(['RNW-027', 'RFU-406', 'QPR-163'])))
    print(getCircuitByStudent(set(['Cox, Shirley', 'Allen, Amanda'])))
    print(getCircuitByComponent(set(['AGC-216', 'BKT-189', 'PLR-243'])))
