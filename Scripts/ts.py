# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Read Data from file
#data = pd.read_csv(r'C:\workspace\Time_Series\test.csv', sep =',',index_col =[1,10])
data = pd.read_csv(r'C:\workspace\Time_Series\test.csv', sep =',')

#Drop ID column from csv
data = data.drop(data.columns[[0]],axis=1)

#Set Trip dates to pandas datetime
data['TripDate'] = pd.to_datetime(data['TripDate'], format='%m/%d/%Y')

#Query to select 'long' time series and 'long trips\
query1 = data[data.SiteGroup=='long']
query1 = query1[query1.TripGroup=='long']
query1 = query1[query1.SitePart=='Eddy']

#Query to obtain the earliest volume
query2 = query1[query1.TripDate=='1990-06-10']


#Create two picot tables
table1 = pd.pivot_table(query1, values=['Volume'], index=['Site','TripDate'], aggfunc=np.sum)
table2 = pd.pivot_table(query1, values=['Max_Volume'], index=['Site','TripDate'], aggfunc=np.sum)
table3 = pd.pivot_table(query2,values=['Volume'], index=['Site','TripDate'], aggfunc=np.sum)
table3 = table3.rename(columns = {'Volume':'Early_Vol'})

#Merge the two pivot tables
merge1 = table1.merge(table2,left_index=True,right_index=True,how='left')

merge2 = pd.merge(merge1.reset_index(),table3.reset_index(),on=['Site'],how='left')

#Reformat tables to look nice
merge2 = merge2.drop(merge2.columns[[-2]], axis=1)
merge2 = merge2.rename(columns = {'TripDate_x':'TripDate'})


#Normalize the Volumes
merge2['Norm_vol'] = merge2.Volume/merge2.Max_Volume

#Calculate percent Volume
merge2['Percent_Vol']=(merge2.Volume-merge2.Early_Vol)/merge2.Early_Vol
merge2 = merge2.set_index(['Site','TripDate'])

#plot % volume vs. time
t=merge2.unstack(level=0)
fig,axes = plt.subplots(figsize=(10,10),nrows=3)
t[[12]].dropna(axis=0).plot(ax=axes[0],rot=45,x_compat=True, marker='o')
t[[13]].dropna(axis=0).plot(ax=axes[1],rot=45,x_compat=True, marker='o')
t[[14]].dropna(axis=0).plot(ax=axes[2],rot=45,x_compat=True, marker='o')