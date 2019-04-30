#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        2/3/19
#######################################################

import os
import sys
from collections import namedtuple


# Module level vars
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab04') #Data Poth


#helper function to return data in technicians file
def getTechData() -> dict:
    tech_file = open(os.path.join(DataPath, 'maps/technicians.dat'))
    file_content = tech_file.read().split('\n')
    del file_content[0:2]
    del file_content[-1]
    tech_dict = {}
    for line in file_content:
        parsed_line = line.split()
        name = ' '.join(parsed_line[0:2])
        id = parsed_line[-1]
        tech_dict[name] = id
    return tech_dict


# helper function to return data in viruses.dat file format of dict: {Name:(ID, Cost)}
def getVirusData() -> dict:
    virus_file = open(os.path.join(DataPath, 'maps/viruses.dat'))
    file_content = virus_file.read().split('\n')
    del file_content[0:2]
    virus_dict = {}
    VirusInfo = namedtuple('VirusInfo', 'ID Price')
    for line in file_content:
        parsed_line = line.split('|')
        name = parsed_line[0].strip()
        id = parsed_line[1].strip()
        price = float(parsed_line[2].strip().strip('$'))
        id_cost_tuple = VirusInfo(id, price)
        virus_dict[name] = id_cost_tuple

    return virus_dict


# helper function to get data from all reports if format: {ID:[list of tuples (userID, virusID, units)]}
def getReportData() -> dict:
    all_reports = os.listdir(os.path.join(DataPath,'reports'))

    report_ids = []

    ReportInfo = namedtuple('ReportInfo', 'UserID VirusID Units')

    for file in all_reports:
        if file.endswith('.dat'):
            report_ids.append(file[7:-4])

    report_dict = {}

    for rep_id in report_ids:
        report_file = open(os.path.join(DataPath, f'reports/report_{rep_id}.dat'))
        file_data = report_file.read().split('\n')
        report_file.close()

        #get user id
        userID = file_data[0]
        userID = userID.split()
        userID = userID[-1]

        trial_list = []

        #parse report data
        del file_data[0:4]
        for line in file_data:
            parsed_line  = line.split()
            virID = parsed_line[1]
            units = int(parsed_line[2])
            trial_list.append(ReportInfo(userID, virID, units))

        report_dict[rep_id] = trial_list
    return report_dict

#problem 1
def getTechWork(techName: str) -> dict:
    techDict = getTechData() #get the ids of all techs
    virDict = getVirusData() #get the virus info for all viruses
    repDict = getReportData() #get data for all reports

    #get id of tech given
    techID = techDict[techName]

    # dict that the function will return
    tech_work_dict = {}

    #create lookup dict for virus name {ID:Name}
    virIDLookup = {}
    for virus in virDict.keys():
        vID = virDict[virus].ID
        virIDLookup[vID] = virus

    #check each report, if the id matches, analyze the trials
    for trialList in repDict.values():
        for trial in trialList:
            if trial.UserID == techID:
                if trial.VirusID not in tech_work_dict.keys():
                    tech_work_dict[trial.VirusID] = trial.Units
                else: tech_work_dict[trial.VirusID] += trial.Units

    return tech_work_dict


# problem 2
def getStrainConsumption(virusName) -> dict:
    techDict = getTechData() #get the ids of all techs
    virDict = getVirusData() #get the virus info for all viruses
    repDict = getReportData() #get data for all reports

    strain_consumption_dict = {}

    # get virus ID
    virusID = virDict[virusName].ID

    #create name lookup by reversing the techDict
    techNameLookup = {}
    for name in techDict.keys():
        techNameLookup[techDict[name]] = name

    #check each trial in each report for a matching virus id
    for trialList in repDict.values():
        for trial in trialList:
            if trial.VirusID == virusID:
                if techNameLookup[trial.UserID] not in strain_consumption_dict:
                    strain_consumption_dict[techNameLookup[trial.UserID]] = trial.Units
                else: strain_consumption_dict[techNameLookup[trial.UserID]] += trial.Units

    return strain_consumption_dict

# problem 3
def getTechSpending() -> dict:
    techDict = getTechData() #get the ids of all techs
    virDict = getVirusData() #get the virus info for all viruses
    repDict = getReportData() #get data for all reports

    tech_spending_dict = {}

    # get a set of all techs who have performed experiments
    used_techs = set()
    for repID in repDict.keys():
        used_techs.add(repDict[repID][0].UserID)

    #create name lookup by reversing the techDict
    techNameLookup = {}
    for name in techDict.keys():
        techNameLookup[techDict[name]] = name

    # create price lookup based on virus ID
    virPriceLookup = {}
    for virus in virDict.keys():
        vID = virDict[virus].ID
        virPriceLookup[vID] = virDict[virus].Price

    for techID in used_techs:
        techName = techNameLookup[techID]
        tech_spending_dict[techName] = 0.0

    for trialList in repDict.values():
        for trial in trialList:
            tech_spending_dict[techNameLookup[trial.UserID]] += float(trial.Units * virPriceLookup[trial.VirusID])
            tech_spending_dict[techNameLookup[trial.UserID]] = round(tech_spending_dict[techNameLookup[trial.UserID]], 2)

    return tech_spending_dict

def getStrainCost() -> dict:
    techDict = getTechData() #get the ids of all techs
    virDict = getVirusData() #get the virus info for all viruses
    repDict = getReportData() #get data for all reports

    strain_cost_dict = {}

    #get set of strains that are used
    strains_used = set()
    for trailList in repDict.values():
        for trial in trailList:
            strains_used.add(trial.VirusID)

    #Create lookup for virus name based on ID
    virNameLookup = {}
    for name in virDict.keys():
        id = virDict[name].ID
        virNameLookup[id] = name


    for strain in strains_used:
        strain_cost_dict[virNameLookup[strain]] = 0.0

    for trialList in repDict.values():
        for trial in trialList:
            virPrice = virDict[virNameLookup[trial.VirusID]].Price
            strain_cost_dict[virNameLookup[trial.VirusID]] += virPrice * trial.Units
            strain_cost_dict[virNameLookup[trial.VirusID]] = round(strain_cost_dict[virNameLookup[trial.VirusID]], 2)

    return strain_cost_dict


def getAbsentTechs() -> set:

    techDict = getTechData() #get the ids of all techs
    repDict = getReportData() #get data for all reports


    #create name lookup by reversing the techDict
    techNameLookup = {}
    for name in techDict.keys():
        techNameLookup[techDict[name]] = name

    #get set of techs who have worked
    active_techs = set()

    for trialList in repDict.values():
        for trial in trialList:
            active_techs.add(techNameLookup[trial.UserID])

    all_techs = set(techDict.keys())

    return (all_techs - active_techs)

def getUnusedStrains() -> set:
    virDict = getVirusData() #get the virus info for all viruses
    repDict = getReportData() #get data for all reports


    #Create lookup for virus name based on ID
    virNameLookup = {}
    for name in virDict.keys():
        id = virDict[name].ID
        virNameLookup[id] = name

    #get set of used strains
    used_strains = set()
    for trialList in repDict.values():
        for trial in trialList:
            used_strains.add(virNameLookup[trial.VirusID])

    #get set of all strains
    all_strains = set(virDict.keys())

    return (all_strains - used_strains)





if __name__ == '__main__':
    techDict = getTechData()
    #print(techDict)
    virDict = getVirusData()
    #print(virDict)
    repDict = getReportData()
    #print(repDict['0BBA0A3D-1CD3-49A5-88D7-6D59A57669F6'])
    techWork = getTechWork('Barnes, Sean')
    print(techWork)
    strCons = getStrainConsumption('Ebolavirus')
    print(strCons)
    print(getTechSpending())
    print(getStrainCost())
    print(getAbsentTechs())
    print(getUnusedStrains())
