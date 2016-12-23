#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:07:11 2016

@author: danielhamill
"""

import pandas as pd
import platform
import numpy as np
import matplotlib.pyplot as plt
def query_df(df):
    '''
    Functon to subset data dataframe to Marble Canyon Sediment Enricnment Period
    '''
    mc_query = 'Segment == ["1_UMC","2_LMC"]'
    df.query(mc_query,inplace=True)
    df.query('Period == ["Sediment_Enrichment"]',inplace = True)
    df.query('Time_Series ==["long"]')
    df['TripDate'] = pd.to_datetime(df['TripDate'], format='%Y-%m-%d')
    return df

    
def pivot_df(df):
    lt_pvt = pd.pivot_table(df, values=['Volume','MaxVol','Area_2D','Max_Area'],index=['TripDate'],aggfunc=np.sum)
    lt_pvt['Norm_Vol'] = lt_pvt['Volume']/lt_pvt['MaxVol']
    lt_pvt['Norm_Error'] = lt_pvt['Area_2D']/lt_pvt['Max_Area']
    lt_pvt = lt_pvt[['Norm_Vol','Norm_Error']]
    return lt_pvt
    
if platform.system() == 'Darwin':
    db_file = '/Users/danielhamill/git_clones/sandbar_process/Merged_Sandbar_data.csv'
    lt_sites ='/Users/danielhamill/git_clones/Time_Series/sites.xlsx'
elif platform.system() == 'Windows':
    dB_file = r'C:\workspace\sandbar_process\Merged_Sandbar_data.csv'
    lt_sties = r'C:\workspace\sandbar_process\sites.xlsx'


#Load Database    
data = pd.read_csv(db_file,sep=',')    

#Load long term monitoring sites
lu_sites = pd.read_excel(lt_sites)
lu_sites = lu_sites[['Sediment Deficit Sites']].dropna()


#Subset long term monitoring sites
long_term = data[data['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]
  

#Get data for plotting
long_term = query_df(long_term)
all_sites = query_df(data)

#Data to plot                 
long_term = pivot_df(long_term)
all_sites = pivot_df(all_sites)

fig,ax = plt.subplots()
long_term.plot(y = 'Norm_Vol', yerr='Norm_Error',ax = ax, label = 'Marble Canyon N=12',color='blue',marker='o')
all_sites.plot(y = 'Norm_Vol', yerr='Norm_Error',ax = ax, label = 'Marble Canyon N=30',color='green',linestyle='--',marker='x')
plt.tight_layout()
plt.savefig('/Users/danielhamill/git_clones/Time_Series/output/mc_variability.png',dpi=600)
plt.show()
