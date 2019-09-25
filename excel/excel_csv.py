# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = None
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    
    # get stations
    TIME_COL = 0
    FIRST_STATION_COL = 1
    LAST_STATION_COL = sheet.ncols-1
    TOTAL_VALUE_COL = sheet.ncols
    stations = sheet.row_values(rowx=0, start_colx=FIRST_STATION_COL, end_colx=LAST_STATION_COL)
    
    # find the time and value of max load for each of the regions
    FIRST_VALUE_ROW = 1
    LAST_VALUE_ROW = sheet.nrows
    maxvalues = []
    maxtimes = []
    timeCol = sheet.col_values(colx=TIME_COL, start_rowx=FIRST_VALUE_ROW, end_rowx=LAST_VALUE_ROW)
    
    for i in range(FIRST_STATION_COL, LAST_STATION_COL):
        valCol = sheet.col_values(colx=i, start_rowx=FIRST_VALUE_ROW, end_rowx=LAST_VALUE_ROW)
        
        # get max load
        maxvalue = max(valCol)
        maxvalues.append(maxvalue) 
        
        # get the time
        maxtime = xlrd.xldate_as_tuple(timeCol[valCol.index(maxvalue)], workbook.datemode)
        maxtime = maxtime[0:-2] # strip minutes and seconds
        maxtimes.append(maxtime)
    
    data = {
        'stations'  : stations,
        'maxvalues' : maxvalues,
        'maxtimes'  : maxtimes
        }
    return data

def save_file(data, filename):
    # YOUR CODE HERE
    with open(filename, 'w+') as out:
        out.write('Station|Year|Month|Day|Hour|Max Load\n')
        for i in range(len(data['stations'])):
            out.write(data['stations'][i]+'|')
            out.write('|'.join(str(val) for val in data['maxtimes'][i]))
            out.write('|'+str(round(data['maxvalues'][i], 1))+'\n')
    
def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    test()
