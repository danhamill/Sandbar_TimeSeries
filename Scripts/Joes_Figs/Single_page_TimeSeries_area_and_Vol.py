# -*- coding: utf-8 -*-
"""
Created on Mon May 01 13:18:56 2017

@author: pb389
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform
import os


def area_average_data(df,section=None):
    if section is not None:
        df=df.query(section)
    tmp_pvt = pd.pivot_table(df, values=['Area_2D'], index=['TripDate'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'Area_2D':'std_dev'})
    tmp_count = pd.pivot_table(df,values=['Area_2D'], index=['TripDate'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'Area_2D':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
    yerr = tmp_pvt[['std_error']]
    del tmp_count, tmp_pvt
    tmp_pvt = pd.pivot_table(df, values=['Area_2D'], index=['TripDate'], aggfunc=np.average)
    #tmp_pvt = tmp_pvt.rename(columns={'Area_2D':'Average'})
    tmp_pvt['y_err']=yerr
    return tmp_pvt
    
def area_norm_data(df,section=None):
    if section is not None:
        df=df.query(section)
    df['Norm_Area'] = df['Area_2D']/df['Max_Area']
    tmp_pvt = pd.pivot_table(df, values=['Norm_Area'], index=['TripDate'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'Norm_Area':'std_dev'})
    tmp_count = pd.pivot_table(df,values=['Norm_Area'], index=['TripDate'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'Norm_Area':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
    yerr = tmp_pvt[['std_error']]
    del tmp_count, tmp_pvt
    tmp_pvt = pd.pivot_table(df, values=['Norm_Area'], index=['TripDate'], aggfunc=np.average)
    tmp_pvt['y_err']=yerr
    return tmp_pvt
    
    
def vol_average_data(df,section=None):
    if section is not None:
        df=df.query(section)
    tmp_pvt = pd.pivot_table(df, values=['Volume'], index=['TripDate'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'Volume':'std_dev'})
    tmp_count = pd.pivot_table(df,values=['Volume'], index=['TripDate'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'Volume':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
    yerr = tmp_pvt[['std_error']]
    del tmp_count, tmp_pvt
    tmp_pvt = pd.pivot_table(df, values=['Volume'], index=['TripDate'], aggfunc=np.average)
    #tmp_pvt = tmp_pvt.rename(columns={'Area_2D':'Average'})
    tmp_pvt['y_err']=yerr
    return tmp_pvt
    
def vol_norm_data(df,section=None):
    if section is not None:
        df=df.query(section)
    df['Norm_Vol'] = df['Volume']/df['MaxVol']
    tmp_pvt = pd.pivot_table(df, values=['Norm_Vol'], index=['TripDate'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'Norm_Vol':'std_dev'})
    tmp_count = pd.pivot_table(df,values=['Norm_Vol'], index=['TripDate'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'Norm_Vol':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
    yerr = tmp_pvt[['std_error']]
    del tmp_count, tmp_pvt
    tmp_pvt = pd.pivot_table(df, values=['Norm_Vol'], index=['TripDate'], aggfunc=np.average)
    tmp_pvt['y_err']=yerr
    return tmp_pvt
    
if platform.system() == 'Darwin':
    sandbar_root = '/Users/danielhamill/git_clones/sandbar_process'
    time_root = '/Users/danielhamill/git_clones/Time_Series'
    out_root = time_root + os.sep + 'Output/Joes_figs'
elif platform.system() == 'Windows':
    sandbar_root = r'C:\workspace\sandbar_process'
    time_root = r'C:\workspace\Time_Series'
    out_root = time_root + os.sep + r'Output\Joes_figs'
    


lt_sites = time_root + os.sep + 'sites.xlsx'
lu_sites = pd.read_excel(lt_sites)
lu_sites = lu_sites[['Sediment Deficit Sites']].dropna()    


#Read Data from file
data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
data = pd.read_csv(data_file, sep =',')

data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')


subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='033l') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l') & (data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.Bar_type != 'Total')]   

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'


mc = subset.query(mc_query)
gc = subset.query(gc_query)


mc = mc[mc['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]
gc = gc[gc['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]


mc_total = pd.pivot_table(mc, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)
gc_total = pd.pivot_table(gc, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)

mc_average = area_average_data(mc)
gc_average = area_average_data(gc)

mc_norm_area = area_norm_data(mc)
gc_norm_area = area_norm_data(gc)

#Entire Time Series
label_gc = 'Grand Canyon: N=' + str(len(gc['Site'].unique()))
label_mc ='Marble Canyon: N=' + str(len(mc['Site'].unique()))

fig, (ax,ax1,ax2) = plt.subplots(nrows=3,figsize=(7.5,10))
gc_total.plot(y = 'Area_2D', ax = ax, label = label_gc, linestyle='-',color='blue',marker='o' )
mc_total.plot(y = 'Area_2D', ax = ax, label = label_mc, linestyle='--',color='green',marker='x')
ax.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2018-01-01'))
ax.set_ylabel('TOTAL SANDBAR AREA, \n IN METERS SQUARED')
ax.set_xlabel('DATE')
ax.set_ylim(30000,70000)
ax.legend(loc=9,ncol=2)



gc_average.plot(y = 'Area_2D', ax = ax1, yerr = 'y_err', label = label_gc,linestyle='-',color='blue',marker='o' )
mc_average.plot(y = 'Area_2D', ax = ax1, yerr = 'y_err',label = label_mc,linestyle='--',color='green',marker='x')
ax1.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2018-01-01'))
ax1.set_ylabel('AVERAGE SANDBAR AREA, \n IN METERS SQUARED')
ax1.set_xlabel('DATE')
ax1.set_ylim(500,3000)
ax1.legend(loc=9,ncol=2)

gc_norm_area.plot(y = 'Norm_Area', ax = ax2, yerr = 'y_err',label = label_gc,linestyle='-',color='blue',marker='o' )
mc_norm_area.plot(y = 'Norm_Area',ax = ax2, yerr = 'y_err',label = label_mc,linestyle='--',color='green',marker='x')
ax2.set_xlim(pd.Timestamp('1990-01-01'),  pd.Timestamp('2018-01-01'))
ax2.set_ylabel('NORMALIZED SANDBAR AREA')
ax2.set_xlabel('DATE')
ax2.set_ylim(0.1,0.35)
ax2.legend(loc=9,ncol=2)


ax.set_autoscale_on(False)
ax1.set_autoscale_on(False)
ax2.set_autoscale_on(False)
plt.tight_layout()
plt.savefig(out_root + os.sep + "Time_Series_area_above_8k.png",dpi=600)

mc = subset.query(mc_query)
gc = subset.query(gc_query)


mc = mc[mc['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]
gc = gc[gc['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]


mc_total_vol = pd.pivot_table(mc, index=['TripDate'], values=['Volume','Errors'],aggfunc=np.sum)
gc_total_vol = pd.pivot_table(gc, index=['TripDate'], values=['Volume','Errors'],aggfunc=np.sum)

mc_average = vol_average_data(mc)
gc_average = vol_average_data(gc)

mc_norm_vol = vol_norm_data(mc)
gc_norm_vol = vol_norm_data(gc)

fig, (ax,ax1,ax2) = plt.subplots(nrows=3,figsize=(7.5,10))
gc_total_vol.plot(y = 'Volume', ax = ax, yerr='Errors',label = label_gc, linestyle='-',color='blue',marker='o' )
mc_total_vol.plot(y = 'Volume', ax = ax, yerr='Errors',label = label_mc, linestyle='--',color='green',marker='x')
ax.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2018-01-01'))
ax.set_ylabel('TOTAL SANDBAR VOLUME, \n IN CUBIC METERS')
ax.set_xlabel('DATE')
ax.set_ylim(20000,90000)
ax.legend(loc=9,ncol=2)



gc_average.plot(y = 'Volume', ax = ax1, yerr = 'y_err', label = label_gc,linestyle='-',color='blue',marker='o' )
mc_average.plot(y = 'Volume', ax = ax1, yerr = 'y_err',label = label_mc,linestyle='--',color='green',marker='x')
ax1.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2018-01-01'))
ax1.set_ylabel('AVERAGE SANDBAR VOLUME, \n IN CUBIC METERS PER SECOND')
ax1.set_xlabel('DATE')
ax1.set_ylim(0,3000)
ax1.legend(loc=9,ncol=2)

gc_norm_vol.plot(y = 'Norm_Vol', ax = ax2, yerr = 'y_err',label = label_gc,linestyle='-',color='blue',marker='o' )
mc_norm_vol.plot(y = 'Norm_Vol',ax = ax2, yerr = 'y_err',label = label_mc,linestyle='--',color='green',marker='x')
ax2.set_xlim(pd.Timestamp('1990-01-01'),  pd.Timestamp('2018-01-01'))
ax2.set_ylabel('NORMALIZED SANDBAR VOLUME')
ax2.set_xlabel('DATE')
ax2.set_ylim(0.1,0.8)
ax2.legend(loc=9,ncol=2)


ax.set_autoscale_on(False)
ax1.set_autoscale_on(False)
ax2.set_autoscale_on(False)
plt.tight_layout()
plt.savefig(out_root + os.sep + "Time_Series_volume_above_8k.png",dpi=600)