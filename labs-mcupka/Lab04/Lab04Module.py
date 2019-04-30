#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        2/6/19
#######################################################
import os
import sys

# Module  level  Variables.
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Lab04')


def getProviderList() -> list:
    all_providers = os.listdir(os.path.join(DataPath, 'providers'))
    return all_providers

def getProviderInfo(provider: str) -> dict:
    p_file = open(os.path.join(DataPath, f'providers/{provider}.dat'))
    raw_data  = p_file.read().split('\n')
    del raw_data[0:3]

    p_data = {}
    for line in raw_data:
        parsed_line = line.split(',')
        price = float(parsed_line[1].strip(' $'))
        item = parsed_line[0].strip()
        p_data[item] = price
    return p_data

def getDifference(provider1: str, provider2: str) -> set:

    pfile_list = getProviderList()
    p1fn = provider1 + '.dat'
    p2fn = provider2 + '.dat'
    if p1fn not in pfile_list or p2fn not in pfile_list:
        raise ValueError('Provider not in list')


    p1_info = getProviderInfo(provider1)
    p2_info = getProviderInfo(provider2)

    p1_sbcs = set(p1_info.keys())
    p2_sbcs = set(p2_info.keys())

    return p1_sbcs - p2_sbcs

def getPriceOf(sbc: str, provider: str) -> float:

    pfile_list = getProviderList()
    pfn = provider + '.dat'
    if pfn not in pfile_list:
        raise ValueError('Provider not in list')

    p_info = getProviderInfo(provider)
    return p_info[sbc]


#returns list of all provider info dicts
def getAllProviderInfo() -> dict:
    all_files = getProviderList()
    all_pnames = []
    for file in all_files:
        file = list(file)
        del file[-4:]
        file = ''.join(file)
        all_pnames.append(file)

    all_info = {}
    for name in all_pnames:
        all_info[name] = (getProviderInfo(name))
    return all_info



def checkAllPrices(sbcSet) -> dict:

    all_prices_dict = {}
    all_pinfo = getAllProviderInfo()


    for name in sbcSet:
        prices = {}
        for p_name in all_pinfo.keys():
            if name in all_pinfo[p_name].keys():
                prices[all_pinfo[p_name][name]] = p_name
        all_prices_dict[name] = (min(prices.keys()), prices[min(prices.keys())])
    return  all_prices_dict

if __name__ == "__main__":
    a = getDifference('provider2', 'provider4')
    print(a)
    b = getPriceOf('Rasp. Pi-4702MQ', 'provider2')
    print(b)
    c = checkAllPrices(set(['Rasp. Pi-4702MQ', 'Rasp. Pi-5950HQ']))
    print(c)