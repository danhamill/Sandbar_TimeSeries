# -*- coding: utf-8 -*-
"""
Created on Mon May 01 13:18:56 2017

@author: pb389
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
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
    tmp_2 = pd.pivot_table(df, values=['Area_2D'], index=['TripDate'], aggfunc=[np.mean,np.std,np.min,np.max])
    #tmp_pvt = tmp_pvt.rename(columns={'Area_2D':'Average'})
    tmp_pvt['y_err']=yerr
    return tmp_pvt, tmp_2
    
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
    tmp_2 = pd.pivot_table(df, values=['Norm_Area'], index=['TripDate'], aggfunc=[np.mean,np.std,np.min,np.max])
    tmp_pvt['y_err']=yerr
    return tmp_pvt, tmp_2
    
    
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
    tmp_2 = pd.pivot_table(df, values=['Volume'], index=['TripDate'], aggfunc=[np.mean,np.std,np.min,np.max])
    #tmp_pvt = tmp_pvt.rename(columns={'Area_2D':'Average'})
    tmp_pvt['y_err']=yerr
    return tmp_pvt, tmp_2
    
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
    tmp_2 = pd.pivot_table(df, values=['Norm_Vol'], index=['TripDate'], aggfunc=[np.mean,np.std,np.min,np.max])
    tmp_pvt['y_err']=yerr
    return tmp_pvt, tmp_2
    
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
subset = pd.pivot_table(subset,index=['Site','SurveyDate','SitePart','TripDate','SiteRange','Segment','Bar_type','Time_Series','Period'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()
mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'


mc = subset.query(mc_query)
gc = subset.query(gc_query)


mc = mc[mc['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]
gc = gc[gc['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]


mc_total = pd.pivot_table(mc, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)
gc_total = pd.pivot_table(gc, index=['TripDate'], values=['Area_2D'],aggfunc=np.sum)

mc_average, mc_avg_area_tbl = area_average_data(mc)
gc_average, gc_avg_area_tbl = area_average_data(gc)

mc_norm_area, mc_norm_area_tbl = area_norm_data(mc)
gc_norm_area, gc_norm_area_tbl = area_norm_data(gc)

#Entire Time Series
label_gc = 'Grand Canyon: N=' + str(len(gc['Site'].unique()))
label_mc ='Marble Canyon: N=' + str(len(mc['Site'].unique()))

fig, (ax,ax1,ax2) = plt.subplots(nrows=3,figsize=(7.5,10))

mc_norm_area.plot(y = 'Norm_Area',ax = ax2, yerr = 'y_err',label = label_mc,linestyle='--',color='green',marker='x')
gc_norm_area.plot(y = 'Norm_Area', ax = ax2, yerr = 'y_err',label = label_gc,linestyle='-',color='blue',marker='o' )

ax2.set_xlim(pd.Timestamp('1990-01-01'),  pd.Timestamp('2018-01-01'))
ax2.set_ylabel('NORMALIZED SANDBAR AREA')
ax2.set_xlabel('DATE')
ax2.set_ylim(0.1,0.30)
ax2.legend(loc=9,ncol=2,fontsize=10)

mc_total.plot(y = 'Area_2D', ax = ax, label = label_mc, linestyle='--',color='green',marker='x',sharex=ax2)
gc_total.plot(y = 'Area_2D', ax = ax, label = label_gc, linestyle='-',color='blue',marker='o' ,sharex=ax2)

ax.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2018-01-01'))
ax.set_ylabel('TOTAL SANDBAR AREA, \n IN METERS SQUARED')
ax.set_xlabel('DATE')
ax.set_ylim(35000,65000)

ax.legend(loc=9,ncol=2,fontsize=10)


mc_average.plot(y = 'Area_2D', ax = ax1, yerr = 'y_err',label = label_mc,linestyle='--',color='green',marker='x',sharex=ax2)
gc_average.plot(y = 'Area_2D', ax = ax1, yerr = 'y_err', label = label_gc,linestyle='-',color='blue',marker='o' ,sharex=ax2)

ax1.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2018-01-01'))
ax1.set_ylabel('AVERAGE SANDBAR AREA, \n IN METERS SQUARED')
ax1.set_xlabel('DATE')
ax1.set_ylim(1000,6000)
ax1.legend(loc=9,ncol=2,fontsize=10)




ax.set_autoscale_on(False)
ax1.set_autoscale_on(False)
ax2.set_autoscale_on(False)

ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))
ax1.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))
#ax2.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.tight_layout()
plt.savefig(out_root + os.sep + "Time_Series_area_above_8k.png",dpi=600)


##################################################################################################################
##################################################################################################################

mc = subset.query(mc_query)
gc = subset.query(gc_query)


mc = mc[mc['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]
gc = gc[gc['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]


mc_total_vol = pd.pivot_table(mc, index=['TripDate'], values=['Volume','Errors'],aggfunc=np.sum)
gc_total_vol = pd.pivot_table(gc, index=['TripDate'], values=['Volume','Errors'],aggfunc=np.sum)
mc_total_vol_tbl = pd.pivot_table(mc, index=['TripDate'], values=['Volume'],aggfunc=[np.mean,np.std,np.min,np.max])
gc_total_vol_tbl = pd.pivot_table(gc, index=['TripDate'], values=['Volume'],aggfunc=[np.mean,np.std,np.min,np.max])
 
mc_average_vol , mc_avg_vol_tbl= vol_average_data(mc)
gc_average_vol, gc_avg_vol_tbl = vol_average_data(gc)

mc_norm_vol, mc_norm_vol_tbl = vol_norm_data(mc)
gc_norm_vol, gc_norm_vol_tbl = vol_norm_data(gc)

fig, (ax,ax1,ax2) = plt.subplots(nrows=3,figsize=(7.5,10))
mc_total_vol.plot(y = 'Volume', ax = ax, yerr='Errors',label = label_mc, linestyle='--',color='green',marker='x',sharex=ax2)
gc_total_vol.plot(y = 'Volume', ax = ax, yerr='Errors',label = label_gc, linestyle='-',color='blue',marker='o',sharex=ax2 )

ax.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2018-01-01'))
ax.set_ylabel('TOTAL SANDBAR VOLUME, \n IN CUBIC METERS')
ax.set_xlabel('DATE')
ax.set_ylim(20000,80000)
ax.legend(loc=9,ncol=2,fontsize=10)


mc_average_vol.plot(y = 'Volume', ax = ax1, yerr = 'y_err',label = label_mc,linestyle='--',color='green',marker='x',sharex=ax2)
gc_average_vol.plot(y = 'Volume', ax = ax1, yerr = 'y_err', label = label_gc,linestyle='-',color='blue',marker='o',sharex=ax2 )

ax1.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2018-01-01'))
ax1.set_ylabel('AVERAGE SANDBAR VOLUME, \n IN CUBIC METERS')
ax1.set_xlabel('DATE')
ax1.set_ylim(0,6000)
ax1.legend(loc=9,ncol=2,fontsize=10)


fig,ax2 = plt.subplots(figsize=(7.5,3.33))
mc_norm_vol.plot(y = 'Norm_Vol',ax = ax2, yerr = 'y_err',label = label_mc,linestyle='--',color='green',marker='x')
gc_norm_vol.plot(y = 'Norm_Vol', ax = ax2, yerr = 'y_err',label = label_gc,linestyle='-',color='blue',marker='o' )

ax2.set_xlim(pd.Timestamp('1990-01-01'),  pd.Timestamp('2018-01-01'))
ax2.set_ylabel('NORMALIZED SANDBAR VOLUME')
ax2.set_xlabel('DATE')
ax2.set_ylim(0.1,0.8)
ax2.legend(loc=9,ncol=2,fontsize=10)

#
#ax.set_autoscale_on(False)
#ax1.set_autoscale_on(False)
ax2.set_autoscale_on(False)


#ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))
#ax1.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))
#ax2.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.tight_layout()


plt.savefig(out_root + os.sep + "Time_Series_Norm_vol_above_8k.png",dpi=600)


writer = pd.ExcelWriter(out_root + os.sep + "Time_series_area_vol_data.xlsx",engine='xlsxwriter')
mc_total_vol_tbl.to_excel(writer,sheet_name='MC_Total_Area')
mc_avg_area_tbl.to_excel(writer,sheet_name='MC_Average_Area')
mc_norm_area_tbl.to_excel(writer,sheet_name='MC_Normalized_Area')
gc_total_vol_tbl.to_excel(writer,sheet_name='GC_Total_Area')
gc_avg_area_tbl.to_excel(writer,sheet_name='GC_Average_Area')
gc_norm_area_tbl.to_excel(writer,sheet_name='GC_Normalized_Area')
writer.save()

