# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 12:17:41 2016

@author: dan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def bin_me(row):
    if row['pct_change']<=-0.05:
        return 'Loss'
    if row['pct_change']>-0.05 and row['Volume']<0.05:
        return 'Same'
    if row['pct_change']>=0.05:
        return "Gain"
        
def sort_hack(row):
    if row['Volume']<=-500:
        return 1
    if row['Volume']>-500 and row['Volume']<500:
        return 2
    if row['Volume']>=500:
        return 3
        
def volume_data(df,section=None):
    if section is not None:
        df=df.query(section)
    tmp_pvt = pd.pivot_table(df, values=['Volume'], index=['TripDate'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'Volume':'std_dev'})
    tmp_count = pd.pivot_table(df,values=['Volume'], index=['TripDate'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'Volume':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']#/np.sqrt(tmp_count['count'])
    yerr = tmp_pvt[['std_error']]
    del tmp_count, tmp_pvt
    tmp_pvt = pd.pivot_table(df, values=['Volume'], index=['TripDate'], aggfunc=np.average)
    tmp_pvt['y_err']=yerr
    return tmp_pvt

def area_data(df,section=None):
    if section is not None:
        df=df.query(section)
    tmp_pvt = pd.pivot_table(df, values=['Area_2D'], index=['TripDate'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'Area_2D':'std_dev'})
    tmp_count = pd.pivot_table(df,values=['Area_2D'], index=['TripDate'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'Area_2D':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']#/np.sqrt(tmp_count['count'])
    yerr = tmp_pvt[['std_error']]
    tmp_pvt = pd.pivot_table(df, values=['Area_2D'], index=['TripDate'], aggfunc=np.average)
    tmp_pvt['y_err']=yerr
    return tmp_pvt
    
def merge_area_vol(df,section=None):
    vol = volume_data(df,section)
    area = area_data(df,section)
    merged = vol.merge(area, left_index=True, right_index=True, how='left')
    return merged


def pct_change(row):
    try:
        vol_15 = float(row['Volume'])
        vol_90 = float(row['Volume_90'])
        change = (vol_15-vol_90)/vol_90
        return change
    except:
        return 0
        
#Read Data from file
#data = pd.read_csv(r'C:\workspace\Time_Series\test.csv', sep ='',index_col =[1,10])
data = pd.read_csv(r'C:\workspace\sandbar_process\Merged_Sandbar_data.csv', sep =',')

query_90 = (data.Time_Series == 'long')& (data.Site !='m006r')& (data.Site !='033l')& (data.Site !='068r')

#Set Trip dates to pandas datetime
data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'

df_90 = data[(data.Time_Series == 'long')& (data.Site !='m006r')& (data.Site !='033l')& (data.Site !='068r')]
df_90 = df_90[df_90['TripDate'] == min(df_90['TripDate'].values)]




df_15 = data[(data.Time_Series == 'short') & (data.SiteRange =='long')& (data.Site !='068r')]
df_15 = df_15[df_15['TripDate'] == max(df_15['TripDate'].values)]

vol_change = df_15[['Site','Volume','Segment','Plane_Height']]
vol_change['Volume_90'] = df_90['Volume'].values

vol_change = pd.pivot_table(vol_change, values=['Volume_90','Volume'], index=['Site','Segment'], aggfunc=np.sum )
vol_change = vol_change.reset_index()

vol_change['pct_change'] = vol_change.apply(lambda row: pct_change(row), axis=1)
vol_change['long_trend'] = vol_change.apply(lambda row: bin_me(row), axis=1)
vol_change['sort_col'] = vol_change.apply(lambda row: sort_hack(row), axis=1)
vol_change = vol_change.sort_values(by='sort_col')


circ1 = Line2D([0], [0], linestyle="none", marker="s", markersize=6, markerfacecolor='red')
circ2 = Line2D([0], [0], linestyle="none", marker="s", markersize=6, markerfacecolor='blue')

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(2,3,1)
vol_change.groupby('long_trend').size().plot(ax=ax,kind='bar',rot=0,title='All Sites',ylim=(0,30))
ax.set_xlabel('')
ax.set_ylabel('Number of Sites')

ax = fig.add_subplot(2,3,2)
vol_change.query('Segment == ["1_UMC","2_LMC"]').groupby('long_trend').size().plot(ax=ax,kind='bar',rot=0,title='Marble Canyon',ylim=(0,30))
ax.set_xlabel('')
ax.set_ylabel('Number of Sites')

ax = fig.add_subplot(2,3,3)
vol_change.query('Segment != ["1_UMC","2_LMC"]').groupby('long_trend').size().plot(ax=ax,kind='bar',rot=0,title='Grand Canyon',ylim=(0,30))
ax.set_xlabel('')
ax.set_ylabel('Number of Sites')


#Get the data
merged_90 = merge_area_vol(df_90)
merged_15 = merge_area_vol(df_15)

ax1 = fig.add_subplot(2,3,4)
merged_90.Volume.plot(ax=ax1, color='red', kind='bar',position=2.5, use_index=False , width=0.1 , yerr=merged_90['y_err_x'],title='All Sites') 
merged_15.Volume.plot(ax=ax1, color='red', kind='bar',position=0, use_index=False, width=0.1, yerr=merged_15['y_err_x']) 
ax2 = ax1.twinx() 
merged_90.Area_2D.plot(ax=ax2,color='blue', kind='bar',position=3.5,use_index=False, width=0.1, yerr=merged_90['y_err_y']) 
merged_15.Area_2D.plot(ax=ax2,color='blue', kind='bar',position=1.0,use_index=False, width=0.1,  yerr=merged_15['y_err_y']) 
ax1.set_xlim([-.45, .2]) 
ax2.set_xlim([-.45, .2])
ax1.set_ylabel('Volume $m^3$') 
ax2.set_ylabel('Area $m^2$') 
ax1.set_xticks([-.23, 0]) 
ax2.set_ylim(-1000,6000)
ax1.set_ylim(-1000,6000)
ax1.set_xticklabels([1990, 2015], rotation=0)
ax1.legend((circ1, circ2),('Volume','Area'),numpoints=1, loc='9', ncol=2, columnspacing=1, fontsize=8)

#Get the data
merged_90 = merge_area_vol(df_90, mc_query)
merged_15 = merge_area_vol(df_15, mc_query)

ax1 = fig.add_subplot(2,3,5)
merged_90.Volume.plot(ax=ax1, color='red', kind='bar',position=2.5, use_index=False , width=0.1 , yerr=merged_90['y_err_x'],title='Marble Canyon') 
merged_15.Volume.plot(ax=ax1, color='red', kind='bar',position=0, use_index=False, width=0.1, yerr=merged_15['y_err_x']) 
ax2 = ax1.twinx() 
merged_90.Area_2D.plot(ax=ax2,color='blue', kind='bar',position=3.5,use_index=False, width=0.1, yerr=merged_90['y_err_y']) 
merged_15.Area_2D.plot(ax=ax2,color='blue', kind='bar',position=1.0,use_index=False, width=0.1,  yerr=merged_15['y_err_y']) 
ax1.set_xlim([-.45, .2]) 
ax2.set_xlim([-.45, .2])
ax1.set_ylabel('Volume $m^3$') 
ax2.set_ylabel('Area $m^2$') 
ax1.set_xticks([-.23, 0]) 
ax2.set_ylim(-1000,6000)
ax1.set_ylim(-1000,6000)
ax1.set_xticklabels([1990, 2015], rotation=0)
ax1.legend((circ1, circ2),('Volume','Area'),numpoints=1, loc='9', ncol=2, columnspacing=1, fontsize=8)

#Get the data
merged_90 = merge_area_vol(df_90, gc_query)
merged_15 = merge_area_vol(df_15, gc_query)
ax1 = fig.add_subplot(2,3,6)
merged_90.Volume.plot(ax=ax1, color='red', kind='bar',position=2.5, use_index=False , width=0.1 , yerr=merged_90['y_err_x'],title='Grand Canyon') 
merged_15.Volume.plot(ax=ax1, color='red', kind='bar',position=0, use_index=False, width=0.1, yerr=merged_15['y_err_x']) 
ax2 = ax1.twinx() 
merged_90.Area_2D.plot(ax=ax2,color='blue', kind='bar',position=3.5,use_index=False, width=0.1, yerr=merged_90['y_err_y']) 
merged_15.Area_2D.plot(ax=ax2,color='blue', kind='bar',position=1.0,use_index=False, width=0.1,  yerr=merged_15['y_err_y']) 
ax1.set_xlim([-.45, .2]) 
ax2.set_xlim([-.45, .2])
ax1.set_ylabel('Volume $m^3$') 
ax2.set_ylabel('Area $m^2$') 
ax1.set_xticks([-.23, 0]) 
ax2.set_ylim(-1000,6000)
ax1.set_ylim(-1000,6000)
ax1.set_xticklabels([1990, 2015], rotation=0)
ax1.legend((circ1, circ2),('Volume','Area'),numpoints=1, loc='9', ncol=2, columnspacing=1, fontsize=8)

plt.suptitle('Long Term Monitoring Sites',fontsize=14)
plt.tight_layout(pad=2.2)
plt.savefig(r"C:\workspace\Time_Series\output\Long_Term_Monitoring_Sites_Summary_std_dev_error_bars_average.png", dpi=600)
plt.show()



 
 
 
 
 