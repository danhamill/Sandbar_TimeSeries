# -*- coding: utf-8 -*-
"""
Created on Wed May 17 14:17:05 2017

@author: dan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform
import os

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
    tmp_2 = pd.pivot_table(df, values=['Norm_Area'], index=['TripDate'],aggfunc=[len,np.mean,np.std,np.min,np.max])
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
    tmp_2 = pd.pivot_table(df, values=['Norm_Vol'], index=['TripDate'], aggfunc=[len,np.mean,np.std,np.min,np.max])
    
    tmp_pvt['y_err']=yerr
    return tmp_pvt, tmp_2


def area_norm_data_site(df,section=None):
    if section is not None:
        df=df.query(section)
    df['Norm_Area'] = df['Area_2D']/df['Max_Area']
    tmp_pvt = pd.pivot_table(df, values=['Norm_Area'], index=['TripDate','Site'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'Norm_Area':'std_dev'})
    tmp_count = pd.pivot_table(df,values=['Norm_Area'], index=['TripDate','Site'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'Norm_Area':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
    yerr = tmp_pvt[['std_error']]
    del tmp_count, tmp_pvt
    tmp_pvt = pd.pivot_table(df, values=['Norm_Area'], index=['TripDate','Site'], aggfunc=np.average)
    tmp_2 = pd.pivot_table(df, values=['Norm_Area'], index=['TripDate','Site'],aggfunc=[len,np.mean,np.std,np.min,np.max])
    tmp_pvt['y_err']=yerr
    return tmp_pvt, tmp_2
    
    
def vol_norm_data_site(df,section=None):
    if section is not None:
        df=df.query(section)
    df['Norm_Vol'] = df['Volume']/df['MaxVol']
    tmp_pvt = pd.pivot_table(df, values=['Norm_Vol'], index=['TripDate','Site'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'Norm_Vol':'std_dev'})
    tmp_count = pd.pivot_table(df,values=['Norm_Vol'], index=['TripDate','Site'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'Norm_Vol':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
    yerr = tmp_pvt[['std_error']]
    del tmp_count, tmp_pvt
    tmp_pvt = pd.pivot_table(df, values=['Norm_Vol'], index=['TripDate','Site'], aggfunc=np.average)
    tmp_2 = pd.pivot_table(df, values=['Norm_Vol'], index=['TripDate','Site'], aggfunc=[len,np.mean,np.std,np.min,np.max])
    
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


fz_subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='035l_r') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l')  & (data.Site !='202r_r') & (data.SitePart == 'Eddy') & (data.Plane_Height == 'eddy8kto25k') & (data.Bar_type != 'Total')]   
fz_subset = fz_subset[fz_subset['TripDate'] <='2003-09-20']

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'


fz_mc = fz_subset.query(mc_query)
fz_gc = fz_subset.query(gc_query)

fz_mc_norm_area, fz_mc_norm_area_tbl_deficit = area_norm_data(fz_mc)
fz_gc_norm_area, fz_gc_norm_area_tbl_deficit = area_norm_data(fz_gc)

fz_mc_norm_vol, fz_mc_norm_vol_tbl_deficit = vol_norm_data(fz_mc)
fz_gc_norm_vol, fz_gc_norm_vol_tbl_deficit = vol_norm_data(fz_gc)


he_subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='035l_r') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l')  & (data.Site !='202r_r')& (data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k') & (data.Bar_type != 'Total')]   
he_subset = he_subset[he_subset['TripDate'] <='2003-09-20']

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'


he_mc = he_subset.query(mc_query)
he_gc = he_subset.query(gc_query)

he_mc_norm_area, he_mc_norm_area_tbl_deficit = area_norm_data(he_mc)
he_gc_norm_area, he_gc_norm_area_tbl_deficit = area_norm_data(he_gc)

he_mc_norm_vol, he_mc_norm_vol_tbl_deficit = vol_norm_data(he_mc)
he_gc_norm_vol, he_gc_norm_vol_tbl_deficit = vol_norm_data(he_gc)

fig,((ax,ax1),(ax2,ax3)) = plt.subplots(figsize=(7.5,6.66), ncols=2,nrows=2)

#Area
he_mc_norm_area.plot(y = 'Norm_Area', yerr='y_err',ax = ax, label = 'Marble Canyon: High Elevation', color='blue',marker='o',sharex=ax2)
fz_mc_norm_area.plot(y = 'Norm_Area', yerr='y_err',ax = ax, label = 'Marble Canyon: Fluctuating Zone', color='green',linestyle='--',marker='x',sharex=ax2)

he_gc_norm_area.plot(y = 'Norm_Area', yerr='y_err',ax = ax1, label = 'Grand Canyon: High Elevation Zone', color='red',linestyle='-.',marker='^',sharex=ax3,sharey=ax)
fz_gc_norm_area.plot(y = 'Norm_Area', yerr='y_err',ax = ax1, label = 'Grand Canyon: Fluctuating Zone', color='black',linestyle=':',marker='>',sharex=ax3,sharey=ax)
ax.legend(loc=9,fontsize=8)#nrow=2,


#Volume
he_mc_norm_vol.plot(y = 'Norm_Vol', yerr='y_err',ax = ax2, label = 'Marble Canyon: High Elevation', color='blue',marker='o')
fz_mc_norm_vol.plot(y = 'Norm_Vol', yerr='y_err',ax = ax2, label = 'Marble Canyon: Fluctuating Zone', color='green',linestyle='--',marker='x')

he_gc_norm_vol.plot(y = 'Norm_Vol', yerr='y_err',ax = ax3, label = 'Grand Canyon: High Elevation Zone', color='red',linestyle='-.',marker='^',sharey=ax2)
fz_gc_norm_vol.plot(y = 'Norm_Vol', yerr='y_err',ax = ax3, label = 'Grand Canyon: Fluctuating Zone', color='black',linestyle=':',marker='>',sharey=ax2)

ax.set_ylim(0,0.5)    
ax1.set_ylim(0,0.5)
ax.set_ylabel('Normalized Sandbar Area')

ax2.set_ylim(0.1,0.8)    
ax3.set_ylim(0.1,0.8)    
ax2.set_ylabel('Normalized Sandbar Volume')

ax1.legend(loc=9,fontsize=8)
ax2.legend(loc=9,fontsize=8)
ax3.legend(loc=1,fontsize=8)


ax2.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2004-01-01'))
ax3.set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('2004-01-01'))
plt.tight_layout()
plt.savefig(out_root + os.sep + 'sediment_deficit_bin_time_series.png', dpi=600)



##########################################################
###########################################################
fz_subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='035l_r') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l')  & (data.Site !='202r_r') & (data.SitePart == 'Eddy') & (data.Plane_Height == 'eddy8kto25k') & (data.Bar_type != 'Total')]   
fz_subset = fz_subset[fz_subset['TripDate'] >='2003-09-20']

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'


fz_mc = fz_subset.query(mc_query)
fz_gc = fz_subset.query(gc_query)

fz_mc_norm_area, fz_mc_norm_area_tbl_enrich = area_norm_data(fz_mc)
fz_gc_norm_area, fz_gc_norm_area_tbl_enrich = area_norm_data(fz_gc)

fz_mc_norm_vol, fz_mc_norm_vol_tbl_enrich = vol_norm_data(fz_mc)
fz_gc_norm_vol, fz_gc_norm_vol_tbl_enrich = vol_norm_data(fz_gc)


he_subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='035l_r') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l')  & (data.Site !='202r_r')& (data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k') & (data.Bar_type != 'Total')]   
he_subset = he_subset[he_subset['TripDate'] >='2003-09-20']

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'


he_mc = he_subset.query(mc_query)
he_gc = he_subset.query(gc_query)

he_mc_norm_area, he_mc_norm_area_tbl_enrich = area_norm_data(he_mc)
he_gc_norm_area, he_gc_norm_area_tbl_enrich = area_norm_data(he_gc)

he_mc_norm_vol, he_mc_norm_vol_tbl_enrich = vol_norm_data(he_mc)
he_gc_norm_vol, he_gc_norm_vol_tbl_enrich = vol_norm_data(he_gc)

fig,((ax,ax1),(ax2,ax3)) = plt.subplots(figsize=(7.5,6.66), ncols=2,nrows=2)

#Area
he_mc_norm_area.plot(y = 'Norm_Area', yerr='y_err',ax = ax, label = 'Marble Canyon: High Elevation', color='blue',marker='o',sharex=ax2)
fz_mc_norm_area.plot(y = 'Norm_Area', yerr='y_err',ax = ax, label = 'Marble Canyon: Fluctuating Zone', color='green',linestyle='--',marker='x',sharex=ax2)

he_gc_norm_area.plot(y = 'Norm_Area', yerr='y_err',ax = ax1, label = 'Grand Canyon: High Elevation Zone', color='red',linestyle='-.',marker='^',sharex=ax3,sharey=ax)
fz_gc_norm_area.plot(y = 'Norm_Area', yerr='y_err',ax = ax1, label = 'Grand Canyon: Fluctuating Zone', color='black',linestyle=':',marker='>',sharex=ax3,sharey=ax)
ax.legend(loc=9,fontsize=8)#nrow=2,


#Volume
he_mc_norm_vol.plot(y = 'Norm_Vol', yerr='y_err',ax = ax2, label = 'Marble Canyon: High Elevation', color='blue',marker='o')
fz_mc_norm_vol.plot(y = 'Norm_Vol', yerr='y_err',ax = ax2, label = 'Marble Canyon: Fluctuating Zone', color='green',linestyle='--',marker='x')

he_gc_norm_vol.plot(y = 'Norm_Vol', yerr='y_err',ax = ax3, label = 'Grand Canyon: High Elevation Zone', color='red',linestyle='-.',marker='^',sharey=ax2)
fz_gc_norm_vol.plot(y = 'Norm_Vol', yerr='y_err',ax = ax3, label = 'Grand Canyon: Fluctuating Zone', color='black',linestyle=':',marker='>',sharey=ax2)

ax.set_ylim(0.1,0.4)    
ax1.set_ylim(0.0,0.4)
ax.set_ylabel('Normalized Sandbar Area')

ax2.set_ylim(0.1,1.0)    
ax3.set_ylim(0.1,1.0)    
ax2.set_ylabel('Normalized Sandbar Volume')

ax1.legend(loc=9,fontsize=8)
ax2.legend(loc=9,fontsize=8)
ax3.legend(loc=1,fontsize=8)


ax2.set_xlim(pd.Timestamp('2003-01-01'), pd.Timestamp('2018-01-01'))
ax3.set_xlim(pd.Timestamp('2003-01-01'), pd.Timestamp('2018-01-01'))
plt.tight_layout()
plt.savefig(out_root + os.sep + 'sediment_enrichment_bin_time_series.png', dpi=600)