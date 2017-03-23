# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 12:17:41 2016

@author: dan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform
import os


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
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
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
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
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

def return_plot_series_med(df):
    temp = df
    temp['NormVol'] = temp['Volume']/temp['MaxVol']
    tmp_pvt = pd.pivot_table(temp, values=['NormVol'], index=['TripDate'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'NormVol':'std_dev'})
    tmp_count = pd.pivot_table(temp,values=['NormVol'], index=['TripDate'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'NormVol':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
    tmp_pvt = tmp_pvt[['std_error']]  
    table1 = df
    table1['NormVol']= table1['Volume']/table1['MaxVol']
    table1 = pd.pivot_table(table1, values=['NormVol'], index=['TripDate'], aggfunc=np.median)
    table1 = table1[['NormVol']]
    table1 = table1.merge(tmp_pvt, left_index=True, right_index=True, how='left')
    return table1

def get_std_error(df):
    temp = df
    tmp_pvt = pd.pivot_table(temp, values=['Volume'], index=['TripDate'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'Volume':'std_dev'})
    tmp_count = pd.pivot_table(temp,values=['Volume'], index=['TripDate'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'Volume':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
    tmp_pvt = tmp_pvt[['std_error']]
    table1 = df
    table1 = pd.pivot_table(table1, values=['Volume'], index=['TripDate'], aggfunc=np.mean)
    table1 = table1[['Volume']]
    table1 = table1.merge(tmp_pvt, left_index=True, right_index=True, how='left')
    return table1

def return_plot_series_mean(df):
    temp = df
    temp['NormVol'] = temp['Volume']/temp['MaxVol']
    tmp_pvt = pd.pivot_table(temp, values=['NormVol'], index=['TripDate'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'NormVol':'std_dev'})
    tmp_count = pd.pivot_table(temp,values=['NormVol'], index=['TripDate'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'NormVol':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
    tmp_pvt = tmp_pvt[['std_error']]    
    table1 = df
    table1['NormVol']= table1['Volume']/table1['MaxVol']
    table1 = pd.pivot_table(table1, values=['NormVol'], index=['TripDate'], aggfunc=np.mean)
    table1 = table1[['NormVol']]
    table1 = table1.merge(tmp_pvt, left_index=True, right_index=True, how='left')
    return table1

def return_area_norm(df):
    temp = df
    temp['NormVol'] = temp['Area_2D']/temp['Max_Area']
    tmp_pvt = pd.pivot_table(temp, values=['NormVol'], index=['TripDate'], aggfunc=np.mean)
    tmp_pvt = tmp_pvt[['NormVol']]
    return tmp_pvt
    
if platform.system() == 'Darwin':
    sandbar_root = '/Users/danielhamill/git_clones/sandbar_process'
    time_root = '/Users/danielhamill/git_clones/Time_Series'
    out_root = time_root + os.sep + 'Output/Joes_figs'
elif platform.system() == 'Windows':
    sandbar_root = r'C:\workspace\sandbar_process'
    time_root = r'C:\workspace\Time_Series'
    out_root = time_root + os.sep + r'Output\Joes_figs'



#################################################################################################################################
#                    Volume eddy above 8k               
##################################################################################################################################    
lt_sites = time_root + os.sep + 'sites.xlsx'
lu_sites = pd.read_excel(lt_sites)
lu_sites = lu_sites[['Sediment Deficit Sites']].dropna()    

#Read Data from file
data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
data = pd.read_csv(data_file, sep =',')

query_90 = (data.Time_Series == 'long')& (data.Site !='m006r')& (data.Site !='033l')& (data.Site !='068r')

#Set Trip dates to pandas datetime
data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'

subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='033l') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l') & (data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.Bar_type != 'Total')]   

                
early = subset[subset['Period'] == 'Sediment_Deficit']
mc_early = early.query(mc_query)
gc_early = early.query(gc_query)
mc_early = mc_early[mc_early['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]
gc_early = gc_early[gc_early['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]

subset1 = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='033l') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l') & (data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k')& (data.Bar_type != 'Total')]   


late = subset1[subset1['Period'] == 'Sediment_Enrichment']
mc_late = late.query(mc_query)
gc_late = late.query(gc_query)


gc_early_plot_mean = return_area_norm(gc_early)
mc_early_plot_mean = return_area_norm(mc_early)

mc_late_plot_mean = return_area_norm(mc_late)
gc_late_plot_mean = return_area_norm(gc_late)

mc_early_average = pd.pivot_table(mc_early,index=['TripDate'], values = ['Area_2D'],aggfunc = np.average)
gc_early_average =pd.pivot_table(gc_early, index=['TripDate'], values=['Area_2D'],aggfunc=np.average)

mc_late_average = pd.pivot_table(mc_late,index=['TripDate'], values = ['Area_2D'],aggfunc = np.average)
gc_late_average = pd.pivot_table(gc_late, index=['TripDate'], values=['Area_2D'],aggfunc=np.average)


mc_early_total = pd.pivot_table(mc_early, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)
gc_early_total = pd.pivot_table(gc_early, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)

mc_late_total = pd.pivot_table(mc_late, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)
gc_late_total = pd.pivot_table(gc_late, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)



#Sediment Deficit
label_gc = 'Grand Canyon: N=' + str(len(gc_early['Site'].unique()))
label_mc ='Marble Canyon: N=' + str(len(mc_early['Site'].unique()))

fig, (ax,ax1,ax2) = plt.subplots(nrows=3,figsize=(7.5,10))
gc_early_total.plot(y = 'Area_2D', ax = ax, label = label_gc, linestyle='-',color='blue',marker='o' )
mc_early_total.plot(y = 'Area_2D', ax = ax, label = label_mc, linestyle='--',color='green',marker='x')
ax.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2003-11-01'))
ax.set_ylabel('TOTAL SANDBAR AREA, \n IN METERS SQUARED')
ax.set_xlabel('DATE')
ax.set_ylim(30000,70000)



gc_early_average.plot(y = 'Area_2D', ax = ax1, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_early_average.plot(y = 'Area_2D', ax = ax1, label = label_mc,linestyle='--',color='green',marker='x')
ax1.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2003-11-01'))
ax1.set_ylabel('AVERAGE SANDBAR AREA, \n IN METERS SQUARED')
ax1.set_xlabel('DATE')
ax1.set_ylim(1000,2500)

gc_early_plot_mean.plot(y = 'NormVol', ax = ax2, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_early_plot_mean.plot(y = 'NormVol',ax = ax2, label = label_mc,linestyle='--',color='green',marker='x')
ax2.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2003-11-01'))
ax2.set_ylabel('NORMALIZED SANDBAR AREA')
ax2.set_xlabel('DATE')
ax2.set_ylim(0.1,0.4)


ax.set_autoscale_on(False)
ax1.set_autoscale_on(False)
ax2.set_autoscale_on(False)
plt.tight_layout()
plt.savefig(out_root + os.sep + "sediment_deficit_area_above_8k.png",dpi=600)


#Sediment Enrichment
label_gc = 'Grand Canyon: N=' + str(len(gc_late['Site'].unique()))
label_mc = 'Marble Canyon: N=' + str(len(mc_late['Site'].unique()))

fig, (ax,ax1,ax2) = plt.subplots(nrows=3,figsize=(7.5,10))
gc_late_total.plot(y = 'Area_2D', ax = ax, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_late_total.plot(y = 'Area_2D',ax = ax, label = label_mc,linestyle='--',color='green',marker='x')
ax.set_xlim(pd.Timestamp('2003-11-01'), pd.Timestamp('2017-01-01'))
ax.set_ylim(40000,130000)
ax.set_ylabel('TOTAL SANDBAR AREA, \n IN METERS SQUARED')
ax.set_xlabel('DATE')

gc_late_average.plot(y = 'Area_2D', ax = ax1, label = label_gc, linestyle='-', color='blue', marker='o' )
mc_late_average.plot(y = 'Area_2D', ax = ax1, label = label_mc,linestyle='--',color='green',marker='x')
ax1.set_xlim(pd.Timestamp('2003-11-01'), pd.Timestamp('2017-01-01'))
ax1.set_ylabel('AVERAGE SANDBAR AREA, \n IN METERS SQUARED')
ax1.set_xlabel('DATE')
ax1.set_ylim(1000,2500)


gc_late_plot_mean.plot(y = 'NormVol', ax = ax2, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_late_plot_mean.plot(y = 'NormVol',ax = ax2, label = label_mc,linestyle='--',color='green',marker='x')
ax2.set_xlim(pd.Timestamp('2003-11-01'), pd.Timestamp('2017-01-01'))
ax2.set_ylabel('NORMALIZED SANDBAR AREA')
ax2.set_xlabel('DATE')
ax2.set_ylim(0.15,0.35)


ax.set_autoscale_on(False)
ax1.set_autoscale_on(False)
ax2.set_autoscale_on(False)
plt.tight_layout()
plt.savefig(out_root + os.sep + "sediment_enrichment_area_above_8k.png",dpi=600)




#################################################################################################################################
#                    Volume eddy above 25k               
##################################################################################################################################    
lt_sites = time_root + os.sep + 'sites.xlsx'
lu_sites = pd.read_excel(lt_sites)
lu_sites = lu_sites[['Sediment Deficit Sites']].dropna()    

#Read Data from file
data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
data = pd.read_csv(data_file, sep =',')

query_90 = (data.Time_Series == 'long')& (data.Site !='m006r')& (data.Site !='033l')& (data.Site !='068r')

#Set Trip dates to pandas datetime
data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'

subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='033l') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l') & (data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k')& (data.Bar_type != 'Total')]   

                
early = subset[subset['Period'] == 'Sediment_Deficit']
mc_early = early.query(mc_query)
gc_early = early.query(gc_query)
mc_early = mc_early[mc_early['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]
gc_early = gc_early[gc_early['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]

subset1 = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='033l') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l') & (data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k')& (data.Bar_type != 'Total')]   


late = subset1[subset1['Period'] == 'Sediment_Enrichment']
mc_late = late.query(mc_query)
gc_late = late.query(gc_query)


gc_early_plot_mean = return_area_norm(gc_early)
mc_early_plot_mean = return_area_norm(mc_early)

mc_late_plot_mean = return_area_norm(mc_late)
gc_late_plot_mean = return_area_norm(gc_late)

mc_early_average = pd.pivot_table(mc_early,index=['TripDate'], values = ['Area_2D'],aggfunc = np.average)
gc_early_average =pd.pivot_table(gc_early, index=['TripDate'], values=['Area_2D'],aggfunc=np.average)

mc_late_average = pd.pivot_table(mc_late,index=['TripDate'], values = ['Area_2D'],aggfunc = np.average)
gc_late_average = pd.pivot_table(gc_late, index=['TripDate'], values=['Area_2D'],aggfunc=np.average)


mc_early_total = pd.pivot_table(mc_early, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)
gc_early_total = pd.pivot_table(gc_early, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)

mc_late_total = pd.pivot_table(mc_late, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)
gc_late_total = pd.pivot_table(gc_late, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)


#Sediment Deficit
label_gc = 'Grand Canyon: N=' + str(len(gc_early['Site'].unique()))
label_mc ='Marble Canyon: N=' + str(len(mc_early['Site'].unique()))
fig, (ax,ax1,ax2) = plt.subplots(nrows=3,figsize=(7.5,10))
gc_early_total.plot(y = 'Area_2D', ax = ax, label = label_gc, linestyle='-',color='blue',marker='o' )
mc_early_total.plot(y = 'Area_2D', ax = ax, label = label_mc, linestyle='--',color='green',marker='x')
ax.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2003-11-01'))
ax.set_ylabel('TOTAL SANDBAR AREA, \n IN METERS SQUARED')
ax.set_xlabel('DATE')
ax.set_ylim(5000,35000)


gc_early_average.plot(y = 'Area_2D', ax = ax1, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_early_average.plot(y = 'Area_2D', ax = ax1, label = label_mc,linestyle='--',color='green',marker='x')
ax1.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2003-11-01'))
ax1.set_ylabel('AVERAGE SANDBAR AREA, \n IN METERS SQUARED')
ax1.set_xlabel('DATE')
ax1.set_ylim(0,2400)


gc_early_plot_mean.plot(y = 'NormVol', ax = ax2, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_early_plot_mean.plot(y = 'NormVol', ax = ax2, label = label_mc,linestyle='--',color='green',marker='x')
ax2.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2003-11-01'))
ax2.set_ylabel('NORMALIZED SANDBAR AREA')
ax2.set_xlabel('DATE')
ax2.set_ylim(0.1,0.3)

ax.set_autoscale_on(False)
ax1.set_autoscale_on(False)
ax2.set_autoscale_on(False)
plt.tight_layout()
plt.savefig(out_root + os.sep + "sediment_deficit_area_above_25k.png",dpi=600)


#Sediment Enrichment
label_gc = 'Grand Canyon: N=' + str(len(gc_late['Site'].unique()))
label_mc = 'Marble Canyon: N=' + str(len(mc_late['Site'].unique()))

fig, (ax,ax1,ax2) = plt.subplots(nrows=3,figsize=(7.5,10))
gc_late_total.plot(y = 'Area_2D', ax = ax, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_late_total.plot(y = 'Area_2D', ax = ax, label = label_mc,linestyle='--',color='green',marker='x')
ax.set_xlim(pd.Timestamp('2003-11-01'), pd.Timestamp('2017-01-01'))
ax.set_ylim(20000,60000)
ax.set_ylabel('TOTAL SANDBAR AREA, \n IN METERS SQUARED')
ax.set_xlabel('DATE')

gc_late_average.plot(y = 'Area_2D', ax = ax1, label = label_gc, linestyle='-', color='blue', marker='o' )
mc_late_average.plot(y = 'Area_2D', ax = ax1, label = label_mc,linestyle='--',color='green',marker='x')
ax1.set_xlim(pd.Timestamp('2003-11-01'), pd.Timestamp('2017-01-01'))
ax1.set_ylabel('AVERAGE SANDBAR AREA, \n IN METERS SQUARED')
ax1.set_xlabel('DATE')
ax1.set_ylim(500,3000)



gc_late_plot_mean.plot(y = 'NormVol', ax = ax2, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_late_plot_mean.plot(y = 'NormVol',ax = ax2, label = label_mc,linestyle='--',color='green',marker='x')
ax2.set_xlim(pd.Timestamp('2003-11-01'), pd.Timestamp('2017-01-01'))
ax2.set_ylabel('NORMALIZED SANDBAR AREA')
ax2.set_xlabel('DATE')
ax2.set_ylim(0.1,0.4)
plt.tight_layout()
ax.set_autoscale_on(False)
ax1.set_autoscale_on(False)
ax2.set_autoscale_on(False)
plt.savefig(out_root + os.sep + "sediment_enrichment_area_above_25k.png",dpi=600)


#################################################################################################################################
#                    Volume eddy 8k to 25k    
##################################################################################################################################    
lt_sites = time_root + os.sep + 'sites.xlsx'
lu_sites = pd.read_excel(lt_sites)
lu_sites = lu_sites[['Sediment Deficit Sites']].dropna()    

#Read Data from file
data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
data = pd.read_csv(data_file, sep =',')

query_90 = (data.Time_Series == 'long')& (data.Site !='m006r')& (data.Site !='033l')& (data.Site !='068r')

#Set Trip dates to pandas datetime
data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'

subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='033l') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l') & (data.SitePart == 'Eddy') & (data.Plane_Height == 'eddy8kto25k')& (data.Bar_type != 'Total')]   
                
early = subset[subset['Period'] == 'Sediment_Deficit']
mc_early = early.query(mc_query)
gc_early = early.query(gc_query)
mc_early = mc_early[mc_early['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]
gc_early = gc_early[gc_early['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]

subset1 = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='033l') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l') & (data.SitePart == 'Eddy') & (data.Plane_Height == 'eddy8kto25k')& (data.Bar_type != 'Total')]   


late = subset1[subset1['Period'] == 'Sediment_Enrichment']
mc_late = late.query(mc_query)
gc_late = late.query(gc_query)


gc_early_plot_mean = return_area_norm(gc_early)
mc_early_plot_mean = return_area_norm(mc_early)

mc_late_plot_mean = return_area_norm(mc_late)
gc_late_plot_mean = return_area_norm(gc_late)

mc_early_average = pd.pivot_table(mc_early,index=['TripDate'], values = ['Area_2D'],aggfunc = np.average)
gc_early_average =pd.pivot_table(gc_early, index=['TripDate'], values=['Area_2D'],aggfunc=np.average)

mc_late_average = pd.pivot_table(mc_late,index=['TripDate'], values = ['Area_2D'],aggfunc = np.average)
gc_late_average = pd.pivot_table(gc_late, index=['TripDate'], values=['Area_2D'],aggfunc=np.average)


mc_early_total = pd.pivot_table(mc_early, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)
gc_early_total = pd.pivot_table(gc_early, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)

mc_late_total = pd.pivot_table(mc_late, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)
gc_late_total = pd.pivot_table(gc_late, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)


#Sediment Deficit
label_gc = 'Grand Canyon: N=' + str(len(gc_early['Site'].unique()))
label_mc ='Marble Canyon: N=' + str(len(mc_early['Site'].unique()))
fig, (ax,ax1,ax2) = plt.subplots(nrows=3,figsize=(7.5,10))
gc_early_total.plot(y = 'Area_2D', ax = ax, label = label_gc, linestyle='-',color='blue',marker='o' )
mc_early_total.plot(y = 'Area_2D', ax = ax, label = label_mc, linestyle='--',color='green',marker='x')
ax.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2003-11-01'))
ax.set_ylabel('TOTAL SANDBAR AREA, \n IN METERS SQUARED')
ax.set_xlabel('DATE')
ax.set_ylim(20000,50000)


gc_early_average.plot(y = 'Area_2D', ax = ax1, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_early_average.plot(y = 'Area_2D',ax = ax1, label = label_mc,linestyle='--',color='green',marker='x')
ax1.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2003-11-01'))
ax1.set_ylabel('AVERAGE SANDBAR AREA, \n IN METERS SQUARED')
ax1.set_xlabel('DATE')
ax1.set_ylim(1200,4000)


gc_early_plot_mean.plot(y = 'NormVol', ax = ax2, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_early_plot_mean.plot(y = 'NormVol', ax = ax2, label = label_mc,linestyle='--',color='green',marker='x')
ax2.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2003-11-01'))
ax2.set_ylabel('NORMALIZED SANDBAR AREA')
ax2.set_xlabel('DATE')
ax2.set_ylim(0.1,0.5)

ax.set_autoscale_on(False)
ax1.set_autoscale_on(False)
ax2.set_autoscale_on(False)
plt.tight_layout()
plt.savefig(out_root + os.sep + "sediment_deficit_area_8kto25k.png",dpi=600)


#Sediment Enrichment
label_gc = 'Grand Canyon: N=' + str(len(gc_late['Site'].unique()))
label_mc = 'Marble Canyon: N=' + str(len(mc_late['Site'].unique()))

fig, (ax,ax1,ax2) = plt.subplots(nrows=3,figsize=(7.5,10))
gc_late_total.plot(y = 'Area_2D', ax = ax, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_late_total.plot(y = 'Area_2D',ax = ax, label = label_mc,linestyle='--',color='green',marker='x')
ax.set_xlim(pd.Timestamp('2003-11-01'), pd.Timestamp('2017-01-01'))
ax.set_ylim(20000,80000)
ax.set_ylabel('TOTAL SANDBAR AREA, \n IN METERS SQUARED')
ax.set_xlabel('DATE')

gc_late_average.plot(y = 'Area_2D', ax = ax1, label = label_gc, linestyle='-', color='blue', marker='o' )
mc_late_average.plot(y = 'Area_2D', ax = ax1, label = label_mc,linestyle='--',color='green',marker='x')
ax1.set_xlim(pd.Timestamp('2003-11-01'), pd.Timestamp('2017-01-01'))
ax1.set_ylabel('AVERAGE SANDBAR AREA, \n IN METERS SQUARED')
ax1.set_xlabel('DATE')
ax1.set_ylim(500,4000)



gc_late_plot_mean.plot(y = 'NormVol', ax = ax2, label = label_gc,linestyle='-',color='blue',marker='o' )
mc_late_plot_mean.plot(y = 'NormVol',ax = ax2, label = label_mc,linestyle='--',color='green',marker='x')
ax2.set_xlim(pd.Timestamp('2003-11-01'), pd.Timestamp('2017-01-01'))
ax2.set_ylabel('NORMALIZED SANDBAR AREA')
ax2.set_xlabel('DATE')
ax2.set_ylim(0.15,0.35)

ax.set_autoscale_on(False)
ax1.set_autoscale_on(False)
ax2.set_autoscale_on(False)

plt.tight_layout()
plt.savefig(out_root + os.sep + "sediment_enrichment_area_8kto25k.png",dpi=600)



 
 
 
 
 