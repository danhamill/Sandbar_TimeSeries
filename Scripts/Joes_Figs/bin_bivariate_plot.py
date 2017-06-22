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

def find_zero_dates(df):
    tmp = df
    tmp = tmp[tmp['Plane_Height']=='eddyabove25k']
    tmp = tmp[tmp['Area_2D']==0]
    dates2drop = tmp[['Site','SurveyDate']].drop_duplicates()
    
    for i, thing in dates2drop.iterrows():
        df = df[(df['Site'] != thing['Site']) | (df['SurveyDate'] != thing['SurveyDate'])]
    return df
    
    
    


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
subset = find_zero_dates(subset)


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



r = r_he_a.merge(r_he_v, left_index=True,right_index=True,how='left')[['Norm_Area','Norm_Vol']]
r = r.rename(columns={'Norm_Area':'Norm_Area_High_Elevation','Norm_Vol':'Norm_Vol_High_Elevation'})

r = r.merge(r_fz_a[['Norm_Area']],left_index=True,right_index=True,how='left')
r = r.rename(columns={'Norm_Area':'Norm_Area_Fluctuating_Zone'})

r = r.merge(r_fz_v[['Norm_Vol']],left_index=True,right_index=True,how='left')
r = r.rename(columns={'Norm_Vol':'Norm_Vol_Fluctuating_Zone'})


u = u_he_a.merge(u_he_v, left_index=True,right_index=True,how='left')[['Norm_Area','Norm_Vol']]
u = u.rename(columns={'Norm_Area':'Norm_Area_High_Elevation','Norm_Vol':'Norm_Vol_High_Elevation'})

u = u.merge(u_fz_a[['Norm_Area']],left_index=True,right_index=True,how='left')
u = u.rename(columns={'Norm_Area':'Norm_Area_Fluctuating_Zone'})

u = u.merge(u_fz_v[['Norm_Vol']],left_index=True,right_index=True,how='left')
u = u.rename(columns={'Norm_Vol':'Norm_Vol_Fluctuating_Zone'})


s = s_he_a.merge(s_he_v, left_index=True,right_index=True,how='left')[['Norm_Area','Norm_Vol']]
s = s.rename(columns={'Norm_Area':'Norm_Area_High_Elevation','Norm_Vol':'Norm_Vol_High_Elevation'})

s = s.merge(s_fz_a[['Norm_Area']],left_index=True,right_index=True,how='left')
s = s.rename(columns={'Norm_Area':'Norm_Area_Fluctuating_Zone'})

s = s.merge(s_fz_v[['Norm_Vol']],left_index=True,right_index=True,how='left')
s = s.rename(columns={'Norm_Vol':'Norm_Vol_Fluctuating_Zone'})


writer = pd.ExcelWriter(out_root + os.sep + "bin_exchange_norm_area_vol_data.xlsx",engine='xlsxwriter')
r.to_excel(writer,sheet_name='Reattachment')
s.to_excel(writer,sheet_name='Separation')
u.to_excel(writer,sheet_name='Undifferentiated')
writer.save()
del writer, s,u,r

#################################################################################################################################
##                                      Area Plots
#################################################################################################################################

#All data (Reatt and Other)

#Linear regression
s,i,r,p,stderr = linregress(r_fz_a['Norm_Area'], r_he_a['Norm_Area'])


fig, ax = plt.subplots(figsize=(7.5,5))
#Deficit
a = ax.scatter(x=r_fz_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], y=r_he_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], 
               marker='D',facecolor='w',label='Reattachment: Deficit',s=100,hatch='...')
#Enrichment
b = ax.scatter(x=r_fz_a.loc['2003-09-20':,:]['Norm_Area'], y=r_he_a.loc['2003-09-20':,:]['Norm_Area'], 
               marker='D',facecolor='w',label='Reattachment: Enrichment ',s=100,hatch='|||||')
ax.plot(r_fz_a['Norm_Area'], i +s*r_fz_a['Norm_Area'],'k')

#Deficit
c = ax.scatter(x=s_fz_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], y=s_he_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], 
               marker='o',facecolor='w',label='Other: Deficit',s=100,hatch='...',alpha=0.4)
ax.scatter(x=u_fz_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], y=u_he_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], 
               marker='o',facecolor='w',s=100,hatch='...',alpha=0.4)
#Enrichment
d = ax.scatter(x=u_fz_a.loc['2003-09-20':,:]['Norm_Area'], y=u_he_a.loc['2003-09-20':,:]['Norm_Area'], 
               marker='o',facecolor='w',label='Other: Enrichment',s=100,hatch='|||||',alpha=0.4)
ax.scatter(x=s_fz_a.loc['2003-09-20':,:]['Norm_Area'], y=s_he_a.loc['2003-09-20':,:]['Norm_Area'], 
               marker='o',facecolor='w',s=100,hatch='|||||',alpha=0.4)

legend = ax.legend(handles=[a,b,c,d],loc=9,fontsize='small',ncol=2,title='Bar Type: Analysis Period',scatterpoints=1)
ax.set_ylabel('High Elevation Normalized Area')
ax.set_xlabel('Fluctuating Zone Normalized Area')
ax.text(0.16,0.3,'R$_{reatt}$$^2$=%1.4f' % r )
ax.set_ylim(0.1,0.4)
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\All_Norm_Area_bin_bivariate.png")


#######################################Undiff Data
#Linear regression
s,i,r,p,stderr = linregress(u_fz_a.loc['2003-09-20':,:]['Norm_Area'], u_he_a.loc['2003-09-20':,:]['Norm_Area'])
s1,i1,r1,p1,stderr1 = linregress(u_fz_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], u_he_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'])

fig, ax = plt.subplots(figsize=(7.5,5))
ax.scatter(x=u_fz_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], y=u_he_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], 
               marker='o',facecolor='w',s=100,hatch='...',alpha=0.4,label='Unidfferentiated: Deficit')
ax.scatter(x=u_fz_a.loc['2003-09-20':,:]['Norm_Area'], y=u_he_a.loc['2003-09-20':,:]['Norm_Area'], 
               marker='o',facecolor='w',label='Unidfferentiated: Enrichment',s=100,hatch='|||||',alpha=0.4)
ax.plot(u_fz_a['Norm_Area'], i +s*u_fz_a['Norm_Area'],'k',label='Linear Regression: Enrichment')
ax.plot(u_fz_a['Norm_Area'], i1 +s1*u_fz_a['Norm_Area'],'k',label='Linear Regression: Deficit',ls=':')
legend = ax.legend(loc=9,fontsize='small',ncol=2,title='Bar Type: Analysis Period',scatterpoints=1)
ax.set_ylabel('High Elevation Normalized Area')
ax.set_xlabel('Fluctuating Zone Normalized Area')
ax.text(0.16,0.3,'R$_{enrich}$$^2$=%1.4f' % r )
ax.text(0.16,0.28,'m$_{enrich}$$^2$=%1.4f' % s )
ax.text(0.34,0.3,'R$_{deficit}$$^2$=%1.4f' % r1 )
ax.text(0.34,0.28,'m$_{deficit}$$^2$=%1.4f' % s1 )

ax.set_ylim(0.1,0.4)
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\undiff_Norm_Area_bin_bivariate.png")

#######################################Reatt Data
#Linear regression
s,i,r,p,stderr = linregress(r_fz_a.loc['2003-09-20':,:]['Norm_Area'], r_he_a.loc['2003-09-20':,:]['Norm_Area'])
s1,i1,r1,p1,stderr1 = linregress(r_fz_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], r_he_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'])

fig, ax = plt.subplots(figsize=(7.5,5))
ax.scatter(x=r_fz_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], y=r_he_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], 
               marker='o',facecolor='w',s=100,hatch='...',alpha=0.4,label='Reattachment: Deficit')
ax.scatter(x=r_fz_a.loc['2003-09-20':,:]['Norm_Area'], y=r_he_a.loc['2003-09-20':,:]['Norm_Area'], 
               marker='o',facecolor='w',label='Reattachment: Enrichment',s=100,hatch='|||||',alpha=0.4)
ax.plot(r_fz_a['Norm_Area'], i +s*r_fz_a['Norm_Area'],'k',label='Linear Regression: Enrichment')
ax.plot(r_fz_a['Norm_Area'], i1 +s1*r_fz_a['Norm_Area'],'k',label='Linear Regression: Deficit',ls=':')
legend = ax.legend(loc=9,fontsize='small',ncol=2,title='Bar Type: Analysis Period',scatterpoints=1)
ax.set_ylabel('High Elevation Normalized Area')
ax.set_xlabel('Fluctuating Zone Normalized Area')
ax.text(0.16,0.28,'R$_{enrich}$$^2$=%1.4f' % r )
ax.text(0.16,0.26,'m$_{enrich}$$^2$=%1.4f' % s )
ax.text(0.34,0.28,'R$_{deficit}$$^2$=%1.4f' % r1 )
ax.text(0.34,0.26,'m$_{deficit}$$^2$=%1.4f' % s1 )
ax.set_ylim(0.05,0.35)
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\reatt_Norm_Area_bin_bivariate.png")

#######################################Sep Data
#Linear regression
s,i,r,p,stderr = linregress(s_fz_a.loc['2003-09-20':,:]['Norm_Area'], s_he_a.loc['2003-09-20':,:]['Norm_Area'])
s1,i1,r1,p1,stderr1 = linregress(s_fz_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], s_he_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'])

fig, ax = plt.subplots(figsize=(7.5,5))
ax.scatter(x=s_fz_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], y=s_he_a.loc['1990-06-10':'2003-09-20',:]['Norm_Area'], 
               marker='o',facecolor='w',s=100,hatch='...',alpha=0.4,label='Separation: Deficit')
ax.scatter(x=s_fz_a.loc['2003-09-20':,:]['Norm_Area'], y=s_he_a.loc['2003-09-20':,:]['Norm_Area'], 
               marker='o',facecolor='w',label='Separation: Enrichment',s=100,hatch='|||||',alpha=0.4)
ax.plot(s_fz_a['Norm_Area'], i +s*s_fz_a['Norm_Area'],'k',label='Linear Regression: Enrichment')
ax.plot(s_fz_a['Norm_Area'], i1 +s1*s_fz_a['Norm_Area'],'k',label='Linear Regression: Deficit',ls=':')
legend = ax.legend(loc=9,fontsize='small',ncol=2,title='Bar Type: Analysis Period',scatterpoints=1)
ax.set_ylabel('High Elevation Normalized Area')
ax.set_xlabel('Fluctuating Zone Normalized Area')
ax.text(0.20,0.23,'R$_{enrich}$$^2$=%1.4f' % r )
ax.text(0.20,0.22,'m$_{enrich}$$^2$=%1.4f' % s )
ax.text(0.28,0.23,'R$_{deficit}$$^2$=%1.4f' % r1 )
ax.text(0.28,0.22,'m$_{deficit}$$^2$=%1.4f' % s1 )
ax.set_ylim(0.12,0.27)
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\sep_Norm_Area_bin_bivariate.png")



#################################################################################################################################
##                                      Volume Plots
#################################################################################################################################

#All data (Reatt and Other)

#Linear regression
s,i,r,p,stderr = linregress(r_fz_v['Norm_Vol'], r_he_v['Norm_Vol'])


fig, ax = plt.subplots(figsize=(7.5,5))
#Deficit
a = ax.scatter(x=r_fz_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], y=r_he_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], 
               marker='D',facecolor='w',label='Reattachment: Deficit',s=100,hatch='...')
#Enrichment
b = ax.scatter(x=r_fz_v.loc['2003-09-20':,:]['Norm_Vol'], y=r_he_v.loc['2003-09-20':,:]['Norm_Vol'], 
               marker='D',facecolor='w',label='Reattachment: Enrichment ',s=100,hatch='|||||')
ax.plot(r_fz_v['Norm_Vol'], i +s*r_fz_v['Norm_Vol'],'k')

#Deficit
c = ax.scatter(x=s_fz_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], y=s_he_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], 
               marker='o',facecolor='w',label='Other: Deficit',s=100,hatch='...',alpha=0.4)
ax.scatter(x=u_fz_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], y=u_he_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], 
               marker='o',facecolor='w',s=100,hatch='...',alpha=0.4)
#Enrichment
d = ax.scatter(x=u_fz_v.loc['2003-09-20':,:]['Norm_Vol'], y=u_he_v.loc['2003-09-20':,:]['Norm_Vol'], 
               marker='o',facecolor='w',label='Other: Enrichment',s=100,hatch='|||||',alpha=0.4)
ax.scatter(x=s_fz_v.loc['2003-09-20':,:]['Norm_Vol'], y=s_he_v.loc['2003-09-20':,:]['Norm_Vol'], 
               marker='o',facecolor='w',s=100,hatch='|||||',alpha=0.4)

legend = ax.legend(handles=[a,b,c,d],loc=9,fontsize='small',ncol=2,title='Bar Type: Analysis Period',scatterpoints=1)
ax.set_ylabel('High Elevation Normalized Volume')
ax.set_xlabel('Fluctuating Zone Normalized Volume')
ax.text(0.25,0.6,'R$_{Reatt}$$^2$=%1.4f' % r )
#ax.set_ylim(0.1,0.4)
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\All_Norm_Vol_bin_bivariate.png")


#######################################Undiff Data
#Linear regression
s,i,r,p,stderr = linregress(u_fz_v.loc['2003-09-20':,:]['Norm_Vol'], u_he_v.loc['2003-09-20':,:]['Norm_Vol'])
s1,i1,r1,p1,stderr1 = linregress(u_fz_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], u_he_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'])

fig, ax = plt.subplots(figsize=(7.5,5))
ax.scatter(x=u_fz_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], y=u_he_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], 
               marker='o',facecolor='w',s=100,hatch='...',alpha=0.4,label='Unidfferentiated: Deficit')
ax.scatter(x=u_fz_v.loc['2003-09-20':,:]['Norm_Vol'], y=u_he_v.loc['2003-09-20':,:]['Norm_Vol'], 
               marker='o',facecolor='w',label='Unidfferentiated: Enrichment',s=100,hatch='|||||',alpha=0.4)
ax.plot(u_fz_v['Norm_Vol'], i +s*u_fz_v['Norm_Vol'],'k',label='Linear Regression: Enrichment')
ax.plot(u_fz_v['Norm_Vol'], i1 +s1*u_fz_v['Norm_Vol'],'k',label='Linear Regression: Deficit',ls=':')
legend = ax.legend(loc=9,fontsize='small',ncol=2,title='Bar Type: Analysis Period',scatterpoints=1)
ax.set_ylabel('High Elevation Normalized Volume')
ax.set_xlabel('Fluctuating Zone Normalized Volume')
ax.text(0.28,0.52,'R$_{enrich}$$^2$=%1.4f' % r )
ax.text(0.28,0.49,'m$_{enrich}$$^2$=%1.4f' % s )
ax.text(0.55,0.27,'R$_{deficit}$$^2$=%1.4f' % r1 )
ax.text(0.55,0.24,'m$_{deficit}$$^2$=%1.4f' % s1 )
#
#ax.set_ylim(0.1,0.4)
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\undiff_Norm_Vol_bin_bivariate.png")

#######################################Reatt Data
#Linear regression
s,i,r,p,stderr = linregress(r_fz_v.loc['2003-09-20':,:]['Norm_Vol'], r_he_v.loc['2003-09-20':,:]['Norm_Vol'])
s1,i1,r1,p1,stderr1 = linregress(r_fz_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], r_he_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'])

fig, ax = plt.subplots(figsize=(7.5,5))
ax.scatter(x=r_fz_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], y=r_he_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], 
               marker='o',facecolor='w',s=100,hatch='...',alpha=0.4,label='Reattachment: Deficit')
ax.scatter(x=r_fz_v.loc['2003-09-20':,:]['Norm_Vol'], y=r_he_v.loc['2003-09-20':,:]['Norm_Vol'], 
               marker='o',facecolor='w',label='Reattachment: Enrichment',s=100,hatch='|||||',alpha=0.4)
ax.plot(r_fz_v['Norm_Vol'], i +s*r_fz_v['Norm_Vol'],'k',label='Linear Regression: Enrichment')
ax.plot(r_fz_v['Norm_Vol'], i1 +s1*r_fz_v['Norm_Vol'],'k',label='Linear Regression: Deficit',ls=':')
legend = ax.legend(loc=9,fontsize='small',ncol=2,title='Bar Type: Analysis Period',scatterpoints=1)
ax.set_ylabel('High Elevation Normalized Volume')
ax.set_xlabel('Fluctuating Zone Normalized Volume')
ax.text(0.28,0.52,'R$_{enrich}$$^2$=%1.4f' % r )
ax.text(0.28,0.49,'m$_{enrich}$$^2$=%1.4f' % s )
ax.text(0.51,0.33,'R$_{deficit}$$^2$=%1.4f' % r1 )
ax.text(0.51,0.30,'m$_{deficit}$$^2$=%1.4f' % s1 )
#ax.set_ylim(0.05,0.35)
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\reatt_Norm_Vol_bin_bivariate.png")

#######################################Sep Data
#Linear regression
s,i,r,p,stderr = linregress(s_fz_v.loc['2003-09-20':,:]['Norm_Vol'], s_he_v.loc['2003-09-20':,:]['Norm_Vol'])
s1,i1,r1,p1,stderr1 = linregress(s_fz_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], s_he_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'])

fig, ax = plt.subplots(figsize=(7.5,5))
ax.scatter(x=s_fz_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], y=s_he_v.loc['1990-06-10':'2003-09-20',:]['Norm_Vol'], 
               marker='o',facecolor='w',s=100,hatch='...',alpha=0.4,label='Separation: Deficit')
ax.scatter(x=s_fz_v.loc['2003-09-20':,:]['Norm_Vol'], y=s_he_v.loc['2003-09-20':,:]['Norm_Vol'], 
               marker='o',facecolor='w',label='Separation: Enrichment',s=100,hatch='|||||',alpha=0.4)
ax.plot(s_fz_v['Norm_Vol'], i +s*s_fz_v['Norm_Vol'],'k',label='Linear Regression: Enrichment')
ax.plot(s_fz_v['Norm_Vol'], i1 +s1*s_fz_v['Norm_Vol'],'k',label='Linear Regression: Deficit',ls=':')
legend = ax.legend(loc=9,fontsize='small',ncol=2,title='Bar Type: Analysis Period',scatterpoints=1)
ax.set_ylabel('High Elevation Normalized Volume')
ax.set_xlabel('Fluctuating Zone Normalized Volume')
ax.text(0.16,0.45,'R$_{enrich}$$^2$=%1.4f' % r )
ax.text(0.16,0.43,'m$_{enrich}$$^2$=%1.4f' % s )
ax.text(0.56,0.32,'R$_{deficit}$$^2$=%1.4f' % r1 )
ax.text(0.56,0.30,'m$_{deficit}$$^2$=%1.4f' % s1 )
ax.set_ylim(0.2,0.60)
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\sep_Norm_Volume_bin_bivariate.png")


####################################################################################################################################

#Linear regression
s,i,r,p,stderr = linregress(r_fz_v['Norm_Vol'], r_he_v['Norm_Vol'])


#Volume Plot
fig, ax = plt.subplots(figsize=(7.5,5))
a = ax.scatter(x=r_fz_v['Norm_Vol'], y=r_he_v['Norm_Vol'], marker='x',c='k',label='Reattachment',s=30)
ax.plot(r_fz_v['Norm_Vol'], i +s*r_fz_v['Norm_Vol'],'k')
b = ax.scatter(x=s_fz_v['Norm_Vol'], y=s_he_v['Norm_Vol'], marker='o',c='grey',alpha=0.4,label='Other')
ax.scatter(x=u_fz_v['Norm_Vol'], y=u_he_v['Norm_Vol'], marker='o',c='grey',alpha=0.4)
legend = ax.legend(handles=[a,b],loc=9,fontsize='small',ncol=2,title='Bar Type')
ax.set_ylabel('High Elevation Normalized Volume')
ax.set_xlabel('Fluctuating Zone Normalized Volume')
ax.text(0.25,0.5,'R$^2$=%1.4f' % r )
#ax.set_ylim(0.1,0.8)
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\Norm_Vol_bin_bivariate.png",dpi=600)

#s,i,r,p,stderr = linregress(pd.concat([r_fz_v['Norm_Vol'],s_fz_v['Norm_Vol'],u_fz_v['Norm_Vol']]), pd.concat([r_he_v['Norm_Vol'],s_he_v['Norm_Vol'],u_he_v['Norm_Vol']]))



#Area Data
r_fz_a,r_fz_a_tbl= area_norm_data_site(r_fz)
s_fz_a,s_fz_a_tbl= area_norm_data_site(s_fz)
u_fz_a,u_fz_a_tbl= area_norm_data_site(u_fz)

r_he_a,r_he_a_tbl= area_norm_data_site(r_he)
s_he_a,s_he_a_tbl= area_norm_data_site(s_he)
u_he_a,u_he_a_tbl= area_norm_data_site(u_he)

#Vol Data
r_fz_v,r_fz_v_tbl= vol_norm_data_site(r_fz)
s_fz_v,s_fz_v_tbl= vol_norm_data_site(s_fz)
u_fz_v,u_fz_v_tbl= vol_norm_data_site(u_fz)

r_he_v,r_he_v_tbl= vol_norm_data_site(r_he)
s_he_v,s_he_v_tbl= vol_norm_data_site(s_he)
u_he_v,u_he_v_tbl= vol_norm_data_site(u_he)


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
ax.text(0.18,0.12,'R$^2$=%1.4f' % r )
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\Norm_Area_bin_bivariate.png",dpi=600)


#Linear regression
s,i,r,p,stderr = linregress(r_fz_v['Norm_Vol'], r_he_v['Norm_Vol'])


#Volume Plot
fig, ax = plt.subplots(figsize=(7.5,5))
a = ax.scatter(x=r_fz_v['Norm_Vol'], y=r_he_v['Norm_Vol'], marker='x',c='k',label='Reattachment',s=30)
ax.plot(r_fz_v['Norm_Vol'], i +s*r_fz_v['Norm_Vol'],'k')
b = ax.scatter(x=s_fz_v['Norm_Vol'], y=s_he_v['Norm_Vol'], marker='o',c='grey',alpha=0.4,label='Other')
ax.scatter(x=u_fz_v['Norm_Vol'], y=u_he_v['Norm_Vol'], marker='o',c='grey',alpha=0.4)
legend = ax.legend(handles=[a,b],loc=9,fontsize='small',ncol=2,title='Bar Type')
ax.set_ylabel('High Elevation Normalized Volume')
ax.set_xlabel('Fluctuating Zone Normalized Volume')
ax.text(0.25,0.5,'R$^2$=%1.4f' % r )
#ax.set_ylim(0.1,0.8)
plt.setp(legend.get_title(),fontsize='small')
plt.tight_layout()
plt.savefig(r"c:\workspace\Time_Series\Output\Joes_Figs\Norm_Vol_bin_bivariate.png",dpi=600)