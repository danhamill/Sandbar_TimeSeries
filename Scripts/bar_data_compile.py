# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:44:03 2016

@author: dh396
"""

import pandas as pd
import fnmatch
import os

outFileName = r'C:\workspace\Sandbar_Process\csv_output\Sandbar_data.csv'

#Function to search all three of the csv_output folder
def find_files(fPattern, list_to_append):
    for root, dirnames, filenames in os.walk(r'c:\workspace\Sandbar_Process\csv_output\CSVs'):
        for filename in fnmatch.filter(filenames, fPattern):
            list_to_append.append(os.path.join(root, filename))
    for root, dirnames, filenames in os.walk(r'c:\workspace\Sandbar_Process\csv_output\No_Bath_CSVS'):
        for filename in fnmatch.filter(filenames, fPattern):
            list_to_append.append(os.path.join(root, filename))
    for root, dirnames, filenames in os.walk(r'c:\workspace\Sandbar_Process\csv_output\Two_Bar_CSVS'):
        for filename in fnmatch.filter(filenames, fPattern):
            list_to_append.append(os.path.join(root, filename))  
    return list_to_append
    
def append_whole_sites(list_to_append, channel_part):
    for item in list_to_append:
        if item == list_to_append[0]:
            data = pd.read_csv(item, sep=',', header=0)
            dataMod = data.assign(SitePart = channel_part)
            dataMod2 = dataMod.assign(Processed_File = item.split('\\')[-1])
            vstack = dataMod2
        else:
            data = pd.read_csv(item, sep=',', header=0)
            dataMod = data.assign(SitePart = channel_part)
            dataMod2 = dataMod.assign(Processed_File = item.split('\\')[-1])
            vstack = pd.concat([vstack, dataMod2], axis=0)  
    return vstack
############File Lists################################



#Create lists of files to process for each bin
chan = find_files('Channel_Low_Elevation.csv', [])
eddy_low = find_files('Eddy_Low_Elevation_Zone.csv',[])
eddy_fz = find_files('Eddy_Fluctuating_Zone.csv', [])
eddy_he = find_files('Eddy_High_Elevation_Zone.csv',[])
r_eddy_low = find_files('*_R_Low.csv', [])
s_eddy_low = find_files('*_S_Low.csv', [])
r_eddy_fz = find_files('*_R_Fluc.csv', [])
s_eddy_fz = find_files('*_S_Fluc.csv', [])
r_eddy_he = find_files('*_R_High.csv', [])
S_eddy_he = find_files('*_S_High.csv', [])


tmp_list = append_whole_sites(chan,'Channel')
tmp_list.to_csv(outFileName)

tmp_list = append_whole_sites(eddy_low,'Eddy')
tmp_list.to_csv(outFileName, mode='a', header=False)



#
#list_to_append = chan
#
#if item==list_to_append[1]:
#    print 'this works'
#for item in chan: 
#    item = chan[0]
#    if item == chan[0]:
#        data = pd.read_csv(item, sep=',', header=0)
#        addSitePart = 'Channel'
#        dataMod = data.assign(SitePart = addSitePart)
#        dataMod2 = data.assign(Processed_File = item.split('\\')[-1])
#        vstack = dataMod2
#    else:
#        data = pd.read_csv(item, sep=',', header=0)
#        addSitePart = 'Channel'
#        dataMod = data.assign(SitePart = addSitePart)
#        dataMod2 = data.assign(Processed_File = item.split('\\')[-1])
#        vstack = pd.concat([vstack, dataMod2], axis=0)
