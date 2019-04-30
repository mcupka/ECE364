#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        1/18/19
#######################################################
import os
import sys
from statistics import mean

# Module  level  Variables
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab02') #Data Poth


# Helper function to open the file and get the data for each day
def getDataEachDay(symbol: str) -> list:
    try:
        # open the symbol's file
        data_file = open(os.path.join(DataPath, f'{symbol}.dat'), 'r')
    except:
        return None

    # Get data for each date in a list
    data_each_day = data_file.read().split('\n')

    #remove non-data from the list
    del data_each_day[0:2] # header info
    del data_each_day[-1] # Blank line at the end

    return data_each_day

def getMaxDifference(symbol: str) -> str:

    # Get data for each date in a list
    data_each_day = getDataEachDay(symbol)

    if data_each_day is None:
        return None

    #list to hold diff values
    diff_values = []

    # iterate through each date in the list an calculate the difference
    for data_one_day in data_each_day:
        split_data = data_one_day.split(',')
        high = float(split_data[4])
        low = float(split_data[5])
        diff_values.append(abs(high - low))

    # return date of the first instance of the max difference
    return (data_each_day[diff_values.index(max(diff_values))].split(','))[0]

def getGainPercent(symbol: str) -> float:

    #get data from file
    data_each_day = getDataEachDay(symbol)

    if data_each_day is None:
        return None

    num_days = float(len(data_each_day))
    num_gain_days = float(0)

    for data_one_day in data_each_day:
        split_data = data_one_day.split(',')
        open = float(split_data[3])
        close = float(split_data[1])
        if open > close:
            num_gain_days += 1

    # return percentage of days that had gains
    return round(num_gain_days / num_days, 4)

def getVolumeSum(symbol: str, date1: str, date2: str) -> int:

    # get data
    data_each_day = getDataEachDay(symbol)

    if data_each_day is None:
        return None


    # get indecies of each date
    date1_index = None
    date2_index = None

    for day_index in range(len(data_each_day)):
        if date1 in data_each_day[day_index]:
            date1_index = day_index
        if date2 in data_each_day[day_index]:
            date2_index = day_index

    if date1_index is None or date2_index is None:
        print("Error finding date indiceis")

    # Make sure the date2 > date1
    if date1_index <= date2_index: #the index of date2 should be lower since the later dates are at the top of the file
        return None

    volume_in_range = 0

    for day_data in data_each_day[date2_index:(date1_index + 1)]:
        # sum each volume in the range
        split_data = day_data.split(',')
        volume_in_range += int(float(split_data[2]))

    return volume_in_range

def getBestGain(date: str) -> float:

    # get list of all symbols my scanning for .dat files in the data path
    all_files = os.listdir(DataPath)
    company_syms = []

    for file in all_files:
        if file.endswith('.dat'):
            company_syms.append(file[:-4])

    # get the gain percentages of each company for the given day

    gains_list = []
    for symbol in company_syms:
        # get data
        company_data = getDataEachDay(symbol)

        # find given date in data
        for day_index in range(len(company_data)):
            if date in company_data[day_index]:
                date_index = day_index

        # get the gain percentage for that given day
        split_data = company_data[day_index].split(',')

        open = float(split_data[3])
        close = float(split_data[1])
        gains = round(float((close - open) / open * 100.0), 4)

        gains_list.append(gains)

    # return the best gains percentage
    return max(gains_list)

def getAveragePrice(symbol: str, year: int) -> float:

    #get data from file
    data_each_day = getDataEachDay(symbol)

    if data_each_day is None:
        return None

    daily_averages_for_year = []

    # check each day to see if it matches the year. if so, calculate daily average
    for day_data in data_each_day:

        split_data = day_data.split(',')
        if int(split_data[0].split('/')[0]) == year:
            # if the data matches the year, add its daily average to the list
            open = float(split_data[3])
            close = float(split_data[1])
            daily_average = float((close + open) / 2.0)
            daily_averages_for_year.append(daily_average)

    # return average of all daily averages in the given year
    return round(mean(daily_averages_for_year), 4)

def getCountOver(symbol: str, price: float) -> int:

    # get data from file
    data_each_day = getDataEachDay(symbol)

    if data_each_day is None:
        return None

    count_over = 0

    for day in data_each_day:
        split_data = day.split(',')
        close = float(split_data[1])
        open = float(split_data[3])
        high = float(split_data[4])
        low = float(split_data[5])

        if (close >= price and open >= price and high >= price and low >= price):
            count_over += 1

    return count_over

if __name__ == '__main__':
    apple_max_diff_day = getMaxDifference('AAPL')
    print (f'Max Diff of AAPL occured on : {apple_max_diff_day}')

    gain_percent = getGainPercent('AAPL')
    print (f'Gain percentage of AAPL is: {gain_percent}')

    vol_sum = getVolumeSum('AAPL', '2019/01/07', '2019/01/11')
    print(f'Volume sum of AAPL in specified dates is: {vol_sum}')

    best_gain_percent = getBestGain('2019/01/07')
    print(f'Best Gain percentage for 2019/01/07 is: {best_gain_percent}')

    average_stock_price = getAveragePrice('AAPL', 2018)
    print(f'Average price of AAPL in 2018 was: {average_stock_price}')

    count_over = getCountOver('AAPL', 120.50)
    print(f'The count over 120.50 of AAPL is: {count_over}')