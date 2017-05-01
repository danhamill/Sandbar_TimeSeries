# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:17:58 2017

@author: dan
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


#Read Data from file
#data = pd.read_csv(r'C:\workspace\Time_Series\test.csv', sep ='',index_col =[1,10])
data = pd.read_csv(r'C:\workspace\sandbar_process\Merged_Sandbar_data.csv', sep =',')
data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')
data = data[(data.Site !='m006r')& (data.Site !='033l') & (data.Site !='062r') & (data.Site !='068r') & (data.Site !='167l') & (data.Bar_type != 'Total')  & (data.SitePart =='Eddy')]
data = data[data['TripDate'] > '1997-01-01']
data = data[data.SiteRange == 'long']


################################################
#           Eddy above 8k
#############################################

subset = data[data.Plane_Height != 'eddyminto8k']
subset = pd.pivot_table(subset, index=['SurveyDate','Site','Bar_type'], values = ['Volume','MaxVol'], aggfunc =np.sum).reset_index()
subset = subset[subset['Volume'] >0]
##Reatt
reatt = subset[subset.Bar_type.str.startswith('Reatt')]
pvt = pd.pivot_table(reatt, index=['Site'],values=['Volume'],aggfunc = np.std).reset_index()
pvt2 = pd.pivot_table(reatt, index=['Site'],values=['Volume'],aggfunc = np.mean).reset_index()
pvt = pvt.rename(columns={'Volume':'Std'})
pvt['Std'] = pvt['Std'] /pvt2['Volume'] 
rt = pvt['River_Mile'] = pvt.Site.str[:3].astype('float')

fig,ax = plt.subplots()
pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='x',s=30,c='g',label='Reattachment')

##Sep
sep = subset[subset.Bar_type.str.startswith('Sep')]
pvt = pd.pivot_table(sep, index=['Site'],values=['Volume'],aggfunc = np.std).reset_index()
pvt2 = pd.pivot_table(sep, index=['Site'],values=['Volume'],aggfunc = np.mean).reset_index()
pvt = pvt.rename(columns={'Volume':'Std'})
pvt['Std'] = pvt['Std'] /pvt2['Volume'] 
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
sp = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='^',s=30,label='Separation')

#Undiff
undiff = subset[subset.Bar_type.str.startswith('Undif')]
pvt = pd.pivot_table(undiff, index=['Site'],values=['Volume'],aggfunc = np.std).reset_index()
pvt2 = pd.pivot_table(undiff, index=['Site'],values=['Volume'],aggfunc = np.mean).reset_index()
pvt = pvt.rename(columns={'Volume':'Std'})
pvt['Std'] = pvt['Std'] /pvt2['Volume'] 
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
ud = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker=',',s=30,c='r',label='Undifferentiated')

ax.set_xlim(0,225)
ax.set_ylim(0,0.8)
ax.set_xlabel('River Mile')
ax.set_ylabel('Standard Deviation')
major_xticks = np.arange(0, 260, 20)
ax.set_xticks(major_xticks)
ax.legend()
plt.tight_layout()
plt.savefig(r"C:\workspace\Time_Series\Output\STD_Plots" + os.sep + 'std_eddy_above8k.png',dpi=600)


################################################
#           Eddy 8k to 25k
#############################################

subset = data[data.Plane_Height == 'eddy8kto25k']
subset = subset[subset['Volume'] >0]
##Reatt
reatt = subset[data.Bar_type.str.startswith('Reatt')]
pvt = pd.pivot_table(reatt, index=['Site'],values=['Volume'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'Volume':'Std'})
rt = pvt['River_Mile'] = pvt.Site.str[:3].astype('float')

fig,ax = plt.subplots()
pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='x',s=30,c='g',label='Reattachment')

##Sep
sep = subset[data.Bar_type.str.startswith('Sep')]
pvt = pd.pivot_table(sep, index=['Site'],values=['Volume'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'Volume':'Std'})
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
sp = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='^',s=30,label='Separation')

#Undiff
undiff = subset[data.Bar_type.str.startswith('Undif')]
pvt = pd.pivot_table(undiff, index=['Site'],values=['Volume'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'Volume':'Std'})
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
ud = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker=',',s=30,c='r',label='Undifferentiated')

ax.set_xlim(0,225)
ax.set_ylim(0,5000)
ax.set_xlabel('River Mile')
ax.set_ylabel('Standard Deviation')
major_xticks = np.arange(0, 260, 20)
ax.set_xticks(major_xticks)
ax.legend()
plt.tight_layout()
plt.savefig(r"C:\workspace\Time_Series\Output\STD_Plots" + os.sep + 'std_eddy_8kto25k.png',dpi=600)

################################################
#           Eddy above25k
#############################################

subset = data[data.Plane_Height == 'eddyabove25k']
subset = subset[subset['Volume'] >0]
##Reatt
reatt = subset[data.Bar_type.str.startswith('Reatt')]
pvt = pd.pivot_table(reatt, index=['Site'],values=['Volume'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'Volume':'Std'})
rt = pvt['River_Mile'] = pvt.Site.str[:3].astype('float')

fig,ax = plt.subplots()
pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='x',s=30,c='g',label='Reattachment')

##Sep
sep = subset[data.Bar_type.str.startswith('Sep')]
pvt = pd.pivot_table(sep, index=['Site'],values=['Volume'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'Volume':'Std'})
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
sp = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='^',s=30,label='Separation')

#Undiff
undiff = subset[data.Bar_type.str.startswith('Undif')]
pvt = pd.pivot_table(undiff, index=['Site'],values=['Volume'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'Volume':'Std'})
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
ud = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker=',',s=30,c='r',label='Undifferentiated')

ax.set_xlim(0,225)
ax.set_ylim(0,2000)
ax.set_xlabel('River Mile')
ax.set_ylabel('Standard Deviation')
major_xticks = np.arange(0, 260, 20)
ax.set_xticks(major_xticks)
ax.legend()
plt.tight_layout()
plt.savefig(r"C:\workspace\Time_Series\Output\STD_Plots" + os.sep + 'std_eddy_above25k.png',dpi=600)

#######################################################################
##########                       Normalized Plots
#######################################################################
################################################
#           Eddy above 8k
#############################################

subset = data[data.Plane_Height != 'eddyminto8k']
subset = pd.pivot_table(subset, index=['SurveyDate','Site','Bar_type'], values = ['Volume','MaxVol'], aggfunc =np.sum).reset_index()
subset['NormVol'] = subset['Volume']/subset['MaxVol']
subset = subset[subset['Volume'] >0]
##Reatt
reatt = subset[subset.Bar_type.str.startswith('Reatt')]
pvt = pd.pivot_table(reatt, index=['Site'],values=['NormVol'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'NormVol':'Std'})
rt = pvt['River_Mile'] = pvt.Site.str[:3].astype('float')

fig,ax = plt.subplots()
pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='x',s=30,c='g',label='Reattachment')

##Sep
sep = subset[subset.Bar_type.str.startswith('Sep')]
pvt = pd.pivot_table(sep, index=['Site'],values=['NormVol'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'NormVol':'Std'})
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
sp = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='^',s=30,label='Separation')

#Undiff
undiff = subset[subset.Bar_type.str.startswith('Undif')]
pvt = pd.pivot_table(undiff, index=['Site'],values=['NormVol'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'NormVol':'Std'})
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
ud = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker=',',s=30,c='r',label='Undifferentiated')

ax.set_xlim(0,225)
#ax.set_ylim(0,0.5)
ax.set_xlabel('River Mile')
ax.set_ylabel('Normalized Volume Standard Deviation')
major_xticks = np.arange(0, 260, 20)
ax.set_xticks(major_xticks)
ax.legend()
plt.tight_layout()
plt.savefig(r"C:\workspace\Time_Series\Output\STD_Plots" + os.sep + 'norm_std_eddy_above8k.png',dpi=600)
print 'Eddyabove8k'
reatt[reatt['Site'] == '003l']['NormVol'].describe()

################################################
#           Eddy 8k to 25k
#############################################

subset = data[data.Plane_Height == 'eddy8kto25k']
subset['NormVol'] = subset['Volume']/subset['MaxVol']
subset = subset[subset['Volume'] >0]
##Reatt
reatt = subset[subset.Bar_type.str.startswith('Reatt')]
pvt = pd.pivot_table(reatt, index=['Site'],values=['NormVol'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'NormVol':'Std'})
rt = pvt['River_Mile'] = pvt.Site.str[:3].astype('float')

fig,ax = plt.subplots()
pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='x',s=30,c='g',label='Reattachment')

##Sep
sep = subset[subset.Bar_type.str.startswith('Sep')]
pvt = pd.pivot_table(sep, index=['Site'],values=['NormVol'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'NormVol':'Std'})
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
sp = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='^',s=30,label='Separation')

#Undiff
undiff = subset[subset.Bar_type.str.startswith('Undif')]
pvt = pd.pivot_table(undiff, index=['Site'],values=['NormVol'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'NormVol':'Std'})
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
ud = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker=',',s=30,c='r',label='Undifferentiated')

ax.set_xlim(0,225)
#ax.set_ylim(0,2000)
ax.set_xlabel('River Mile')
ax.set_ylabel('Normalized Volume Standard Deviation')
major_xticks = np.arange(0, 260, 20)
ax.set_xticks(major_xticks)
ax.legend()
plt.tight_layout()
plt.savefig(r"C:\workspace\Time_Series\Output\STD_Plots" + os.sep + 'norm_std_eddy_8kto25k.png',dpi=600)

print 'Fluctuating Zone'
reatt[reatt['Site'] == '003l']['NormVol'].describe()
################################################
#           Eddy above25k
#############################################

subset = data[data.Plane_Height == 'eddyabove25k']
subset['NormVol'] = subset['Volume']/subset['MaxVol']
subset = subset[subset['Volume'] >0]
##Reatt
reatt = subset[data.Bar_type.str.startswith('Reatt')]
pvt = pd.pivot_table(reatt, index=['Site'],values=['NormVol'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'NormVol':'Std'})
rt = pvt['River_Mile'] = pvt.Site.str[:3].astype('float')

fig,ax = plt.subplots()
pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='x',s=30,c='g',label='Reattachment')

##Sep
sep = subset[data.Bar_type.str.startswith('Sep')]
pvt = pd.pivot_table(sep, index=['Site'],values=['NormVol'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'NormVol':'Std'})
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
sp = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker='^',s=30,label='Separation')

#Undiff
undiff = subset[data.Bar_type.str.startswith('Undif')]
pvt = pd.pivot_table(undiff, index=['Site'],values=['NormVol'],aggfunc = np.std).reset_index()
pvt = pvt.rename(columns={'NormVol':'Std'})
pvt['River_Mile'] = pvt.Site.str[:3].astype('float')
ud = pvt.plot(ax=ax, kind='scatter', y='Std',x='River_Mile',marker=',',s=30,c='r',label='Undifferentiated')

ax.set_xlim(0,225)
#ax.set_ylim(0,0.5)
ax.set_xlabel('River Mile')
ax.set_ylabel('Normalized Volume Standard Deviation')
major_xticks = np.arange(0, 260, 20)
ax.set_xticks(major_xticks)
ax.legend()
plt.tight_layout()
plt.savefig(r"C:\workspace\Time_Series\Output\STD_Plots" + os.sep + 'norm_std_eddy_above25k.png',dpi=600)

print 'High Elevation'
reatt[reatt['Site'] == '003l']['NormVol'].describe()