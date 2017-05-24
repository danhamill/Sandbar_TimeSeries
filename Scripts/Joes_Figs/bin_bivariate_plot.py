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
from scipy.stats import linregress

    
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


###############################################################################################################
# All sites, All Dates, Bar Type Plots
###############################################################################################################

subset = data[(data.Time_Series == 'long') & (data.Site !='m006r')& (data.Site !='035l_r') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l')  & (data.Site !='202r_r')& (data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.Bar_type != 'Total')]   



#Bar Types
reatt = subset[subset.Bar_type.str.startswith('Re')]
sepp = subset[subset.Bar_type.str.startswith('Se')]
undif = subset[subset.Bar_type.str.startswith('Un')]

#FZ
r_fz = reatt[reatt['Plane_Height'] == 'eddy8kto25k']
s_fz = sepp[sepp['Plane_Height'] == 'eddy8kto25k' ]
u_fz = undif[undif['Plane_Height'] =='eddy8kto25k']

#HE
r_he = reatt[reatt['Plane_Height'] == 'eddyabove25k']
s_he = sepp[sepp['Plane_Height'] == 'eddyabove25k' ]
u_he = undif[undif['Plane_Height'] =='eddyabove25k']


#Area Data
r_fz_a,r_fz_a_tbl= area_norm_data(r_fz)
s_fz_a,s_fz_a_tbl= area_norm_data(s_fz)
u_fz_a,u_fz_a_tbl= area_norm_data(u_fz)

r_he_a,r_he_a_tbl= area_norm_data(r_he)
s_he_a,s_he_a_tbl= area_norm_data(s_he)
u_he_a,u_he_a_tbl= area_norm_data(u_he)

#Vol Data
r_fz_v,r_fz_v_tbl= vol_norm_data(r_fz)
s_fz_v,s_fz_v_tbl= vol_norm_data(s_fz)
u_fz_v,u_fz_v_tbl= vol_norm_data(u_fz)

r_he_v,r_he_v_tbl= vol_norm_data(r_he)
s_he_v,s_he_v_tbl= vol_norm_data(s_he)
u_he_v,u_he_v_tbl= vol_norm_data(u_he)


#Linear regression
s,i,r,p,stderr = linregress(r_fz_a['Norm_Area'], r_he_a['Norm_Area'])


#Area Plot
fig, ax = plt.subplots(figsize=(7.5,5))
a = ax.scatter(x=r_fz_a['Norm_Area'], y=r_he_a['Norm_Area'], marker='x',c='k',label='Reattachment',s=30)
ax.plot(r_fz_a['Norm_Area'], i +s*r_fz_a['Norm_Area'],'k')
b = ax.scatter(x=s_fz_a['Norm_Area'], y=s_he_a['Norm_Area'], marker='o',c='grey',alpha=0.4,label='Other')
ax.scatter(x=u_fz_a['Norm_Area'], y=u_he_a['Norm_Area'], marker='o',c='grey',alpha=0.4)
legend = ax.legend(handles=[a,b],loc=9,fontsize='small',ncol=2,title='Bar Type')
ax.set_ylabel('High Elevation Normalized Area')
ax.set_xlabel('Fluctuating Zone Normalized Area')
ax.text(0.29,0.08,'R$^2$=%1.4f' % r )
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\Norm_Area_bin_bivariate.png",dpi=600)


#Linear regression
s,i,r,p,stderr = linregress(r_fz_v['Norm_Vol'], r_he_v['Norm_Vol'])


#Area Plot
fig, ax = plt.subplots(figsize=(7.5,5))
a = ax.scatter(x=r_fz_v['Norm_Vol'], y=r_he_v['Norm_Vol'], marker='x',c='k',label='Reattachment',s=30)
ax.plot(r_fz_v['Norm_Vol'], i +s*r_fz_v['Norm_Vol'],'k')
b = ax.scatter(x=s_fz_v['Norm_Vol'], y=s_he_v['Norm_Vol'], marker='o',c='grey',alpha=0.4,label='Other')
ax.scatter(x=u_fz_v['Norm_Vol'], y=u_he_v['Norm_Vol'], marker='o',c='grey',alpha=0.4)
legend = ax.legend(handles=[a,b],loc=9,fontsize='small',ncol=2,title='Bar Type')
ax.set_ylabel('High Elevation Normalized Volume')
ax.set_xlabel('Fluctuating Zone Normalized Volume')
ax.text(0.15,0.5,'R$^2$=%1.4f' % r )
ax.set_ylim(0.1,0.8)
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\Norm_Vol_bin_bivariate.png",dpi=600)