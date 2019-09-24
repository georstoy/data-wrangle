#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format

"""

import xlrd
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0) # get first sheet

# find and return the min, max and average values for the COAST region
    # get data from the COAST col
    COAST_COL = 1
    coast_data = [sheet.cell_value(r, COAST_COL) 
                    for r in range(1, sheet.nrows)]

    minvalue = min(coast_data)
    maxvalue = max(coast_data)

# find and return the time value for the min and max entries
    # get data from the Hour_End col
    TIME_COL = 0
    time_data = [sheet.cell_value(r, TIME_COL)
                    for r in range(1, sheet.nrows)]

    data = {
            'maxtime': xlrd.xldate_as_tuple(time_data[coast_data.index(maxvalue)], workbook.datemode),
            'maxvalue': round(maxvalue,10),
            'mintime': xlrd.xldate_as_tuple(time_data[coast_data.index(minvalue)], workbook.datemode),
            'minvalue': round(minvalue,10),
            'avgcoast': round(sum(coast_data)/len(coast_data),10)
    }
    return data


def test():
    open_zip(datafile.lower().rstrip('.xls').replace('_','-'))
    data = parse_file(datafile)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)

test()