#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 16:14:21 2022

@author: deborahkhider
"""

import argparse
import lipd as lpd
import pandas as pd

# Get the argument in
parser = argparse.ArgumentParser(description='Extract each time series in a LiPD file as rows in a table')
parser.add_argument('-i1', '--lipdfile', type =str, help='Path to LiPD file')
parser.add_argument('-o1', '--outputfile', type =str, help = 'Name of output file')

#parse the arguments
args = parser.parse_args()

#print the arguments for help
print(args)
D=lpd.readLipd(args.lipdfile)
ts_list = lpd.extractTs(D)

time=[]
value=[]
time_name=[]
value_name=[]
time_unit=[]
value_unit=[]
archive=[]
lat=[]
lon=[]

for item in ts_list:
    if 'year' in item.keys():
        time_name.append('Year')
        time_unit.append(item['yearUnits'])
        time.append(item['year'])
        value.append(item['paleoData_values'])
        value_unit.append(item['paleoData_units'])
        value_name.append(item['paleoData_variableName'])
        archive.append(item['archiveType'])
        lat.append(item['geo_meanLat'])
        lon.append(item['geo_meanLon'])
        
    elif 'age' in item.keys():
        time_name.append('Age')
        time_unit.append(item['ageUnits'])
        time.append(item['age'])
        value.append(item['paleoData_values'])
        value_unit.append(item['paleoData_units'])
        value_name.append(item['paleoData_variableName'])
        archive.append(item['archiveType'])
        lat.append(item['geo_meanLat'])
        lon.append(item['geo_meanLon'])
        
    else:
        pass
    
    
data = pd.DataFrame({'time':time,
                     'value':value,
                     'time_name':time_name,
                     'value_name':value_name,
                     'time_unit':time_unit,
                     'value_unit':value_unit,
                     'archive':archive,
                    'lat':lat,
                    'lon':lon})   

data.to_csv(args.outputfile)