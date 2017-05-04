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





####################################################################################################################
###########             Sediment Defecit Plots
####################################################################################################################

fz_subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='035l+r') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l')  & (data.Site !='202r_r')& (data.SitePart == 'Eddy') & (data.Plane_Height == 'eddy8kto25k') & (data.Bar_type != 'Total')]   
fz_subset = fz_subset[fz_subset['TripDate'] <='2003-09-20']

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'


fz_mc = fz_subset.query(mc_query)
fz_gc = fz_subset.query(gc_query)

fz_mc_norm_area, fz_mc_norm_area_tbl_deficit = area_norm_data(fz_mc)
fz_gc_norm_area, fz_gc_norm_area_tbl_deficit = area_norm_data(fz_gc)

fz_mc_norm_vol, fz_mc_norm_vol_tbl_deficit = vol_norm_data(fz_mc)
fz_gc_norm_vol, fz_gc_norm_vol_tbl_deficit = vol_norm_data(fz_gc)


he_subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='035l+r') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l')  & (data.Site !='202r_r')& (data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k') & (data.Bar_type != 'Total')]   
he_subset = he_subset[he_subset['TripDate'] <='2003-09-20']

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'


he_mc = he_subset.query(mc_query)
he_gc = he_subset.query(gc_query)

he_mc_norm_area, he_mc_norm_area_tbl_deficit = area_norm_data(he_mc)
he_gc_norm_area, he_gc_norm_area_tbl_deficit = area_norm_data(he_gc)

he_mc_norm_vol, he_mc_norm_vol_tbl_deficit = vol_norm_data(he_mc)
he_gc_norm_vol, he_gc_norm_vol_tbl_deficit = vol_norm_data(he_gc)

fig,(ax,ax1) = plt.subplots(nrows=2)
ax.scatter(x=he_mc_norm_vol['Norm_Vol'], y=fz_mc_norm_vol['Norm_Vol'], marker='x',label='Marble Canyon')
ax.scatter(x=he_gc_norm_vol['Norm_Vol'], y=fz_gc_norm_vol['Norm_Vol'], marker='>',label='Grand Canyon')
ax.set_xlabel('High Elevation \n Normalized Volume')
ax.set_ylabel('Fluctuating Zone \n Normalized Volume')

ax1.scatter(x=he_mc_norm_area['Norm_Area'], y=fz_mc_norm_area['Norm_Area'], marker='x',label='Marble Canyon')
ax1.scatter(x=he_gc_norm_area['Norm_Area'], y=fz_gc_norm_area['Norm_Area'], marker='>',label='Grand Canyon')
ax1.set_xlabel('High Elevation \n Normalized Area')
ax1.set_ylabel('Fluctuating Zone \n Normalized Area')

ax.set_xlim(0.1,0.7)
ax.set_ylim(0.2,0.7)
ax1.set_xlim(0.1,0.25)
ax1.set_ylim(0.15,0.40)

ax.legend(loc=9,ncol=2,fontsize=8)
ax1.legend(loc=9,ncol=2,fontsize=8)
plt.tight_layout()
plt.show()



####################################################################################################################
###########             Sediment Enrichment Plots
####################################################################################################################

subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='035l+r') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l')  & (data.Site !='202r_r')& (data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.Bar_type != 'Total')]   
subset = pd.pivot_table(subset,index=['Site','SurveyDate','SitePart','TripDate','SiteRange','Segment','Bar_type','Time_Series','Period'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()
subset = subset[subset['TripDate'] >='2003-09-20']

mc_query = 'Segment == ["1_UMC","2_LMC"]'
gc_query = 'Segment != ["1_UMC","2_LMC"]'


mc = subset.query(mc_query)
gc = subset.query(gc_query)

mc_norm_area, mc_norm_area_tbl_enrich = area_norm_data(mc)
gc_norm_area, gc_norm_area_tbl_enrich = area_norm_data(gc)


mc_norm_vol, mc_norm_vol_tbl_enrich = vol_norm_data(mc)
gc_norm_vol, gc_norm_vol_tbl_enrich = vol_norm_data(gc)

label_gc = 'Grand Canyon'
label_mc ='Marble Canyon'

fig, (ax,ax1) = plt.subplots(nrows=2,figsize=(7.5,7))

mc_norm_area.plot(y = 'Norm_Area',ax = ax, yerr = 'y_err',label = label_mc,linestyle='--',color='green',marker='x', sharex=ax1)
gc_norm_area.plot(y = 'Norm_Area', ax = ax, yerr = 'y_err',label = label_gc,linestyle='-',color='blue',marker='o' ,sharex=ax1)
ax.set_xlim(pd.Timestamp('2003-01-01'),  pd.Timestamp('2017-01-01'))
ax.set_ylabel('NORMALIZED SANDBAR AREA')
ax.set_xlabel('DATE')
ax.set_ylim(0.10,0.30)
ax.legend(loc=9,ncol=2,fontsize=10)



mc_norm_vol.plot(y = 'Norm_Vol',ax = ax1, yerr = 'y_err',label = label_mc,linestyle='--',color='green',marker='x')
gc_norm_vol.plot(y = 'Norm_Vol', ax = ax1, yerr = 'y_err',label = label_gc,linestyle='-',color='blue',marker='o' )

ax1.set_xlim(pd.Timestamp('2003-01-01'),  pd.Timestamp('2017-01-01'))
ax1.set_ylabel('NORMALIZED SANDBAR VOLUME')
ax1.set_xlabel('DATE')
ax1.set_ylim(0.2,0.7)
ax1.legend(loc=9,ncol=2,fontsize=10)
ax.set_autoscale_on(False)
ax1.set_autoscale_on(False)
plt.tight_layout()
plt.savefig(out_root + os.sep + "All_sites_sediment_enrichment_norm_volume_above_8k.png",dpi=600)

















writer = pd.ExcelWriter(out_root + os.sep + "all_sites_periods_norm_area_vol_data.xlsx",engine='xlsxwriter')
pd.concat([mc_norm_area_tbl_deficit,mc_norm_area_tbl_enrich]).to_excel(writer,sheet_name='MC_Normalized_Area')
pd.concat([gc_norm_vol_tbl_deficit,mc_norm_vol_tbl_enrich]).to_excel(writer,sheet_name='GC_Normalized_Area')


writer.save()

