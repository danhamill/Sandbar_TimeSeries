#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 15:54:43 2017

@author: danielhamill
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform
import os


if platform.system() == 'Darwin':
    sandbar_root = '/Users/danielhamill/git_clones/sandbar_process'
    time_root = '/Users/danielhamill/git_clones/Time_Series'
    out_root = time_root + os.sep + 'Output/Joes_figs'
elif platform.system() == 'Windows':
    sandbar_root = r'C:\workspace\sandbar_process'
    time_root = r'C:\workspace\Time_Series'
    out_root = time_root + os.sep + r'Output\Joes_figs'
    
#Read Data from file
data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
data = pd.read_csv(data_file, sep =',')

data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')    



data = pd.pivot_table(data,index=['Site','SurveyDate','SitePart','TripDate','SiteRange','Segment','Bar_type','Time_Series','Period'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()

data = data[(data['TripDate']>'2010-01-01') & (data['TripDate']<'2013-01-01')]
            
data.loc[:,'NormVol'] = data['Volume']/data['MaxVol']
data = data[(data['Time_Series'] =='long') & (data['Bar_type'] != 'Total')]

pvt = pd.pivot_table(data,index=['TripDate','Site'],values = ['NormVol'],aggfunc=np.average).reset_index(level=1)#,columns=['Site']

grouped = pvt.groupby('Site')


df = pd.DataFrame(index='Site',columns=['Pct_Dif'])
for name, group in grouped:
    print name
    
    pct_dif = (group.iloc[1]['NormVol']-group.iloc[0]['NormVol'])/group.iloc[1]['NormVol']*100
    
    try: 
        len(df)
    except:
        df.iloc[0] = pd.DataFrame({'Site':name,'Pct_Dif':pct_dif})