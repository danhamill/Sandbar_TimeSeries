#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:07:11 2016

@author: danielhamill
"""

import pandas as pd
import platform

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