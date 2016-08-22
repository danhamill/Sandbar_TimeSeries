# -*- coding: utf-8 -*-
"""
Created on Tue May 03 15:57:30 2016

@author: dan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


#Read Data from file
#data = pd.read_csv(r'C:\workspace\Time_Series\test.csv', sep ='',index_col =[1,10])
data = pd.read_csv(r'C:\workspace\sandbar_process\Merged_Sandbar_data.csv', sep =',')


#Set Trip dates to pandas datetime
data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')


#Marble Canyon percent Volume
query1 = data[(data.Segment != '2_LMC') &(data.Segment != '3_EGC') & (data.Segment != '4_CGC') & (data.Segment != '5_WGC') & 
(data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k') & (data.SiteRange=='long')]
query1 = query1[query1['TripDate'] > '2004-01-01']
#Determine what the earliest survey was for each site
umc_early_vol = pd.pivot_table(query1,values=['TripDate'], index=['Site'], aggfunc=np.min)
table1 = pd.pivot_table(query1, values=['Volume'], index=['Site','TripDate'], aggfunc=np.sum)
umc_early_vol = pd.merge(umc_early_vol.reset_index(),table1.reset_index(),on=['Site','TripDate'],how='left')
umc_early_vol = umc_early_vol.rename(columns = {'Volume':'Early_Vol'})
umc_early_vol = pd.pivot_table(umc_early_vol,values=['Early_Vol'], index=['TripDate'], aggfunc=np.sum)
del table1
#Associate Early_Vol with early dates
umc_vol = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.sum)
umc_std = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.std)
umc_std = umc_std.rename(columns={'Volume':'std_dev'})
umc_count = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc='count')
umc_count = umc_count.rename(columns={'Volume':'count'})
umc_vol['std_error']=umc_std.std_dev/np.sqrt(umc_count['count'])
umc_vol ['percent_vol'] = (umc_vol.Volume-umc_early_vol.Early_Vol[0])/umc_early_vol.Early_Vol[0]
umc_vol['percent_std_error'] = (umc_vol.std_error-umc_vol['std_error'][0])/umc_vol['std_error'][0]

del umc_std, umc_count, umc_early_vol


query2 = data[(data.Segment != '1_UMC') & (data.Segment != '3_EGC') & (data.Segment != '4_CGC') & (data.Segment != '5_WGC') & 
(data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k') & (data.SiteRange=='long')]
query2 = query2[query2['TripDate'] > '2004-01-01']
#Determine what the earliest survey was for each site
lmc_early_vol = pd.pivot_table(query2,values=['TripDate'], index=['Site'], aggfunc=np.min)
table2 = pd.pivot_table(query2, values=['Volume'], index=['Site','TripDate'], aggfunc=np.sum)
lmc_early_vol = pd.merge(lmc_early_vol.reset_index(),table2.reset_index(),on=['Site','TripDate'],how='left')
lmc_early_vol = lmc_early_vol.rename(columns = {'Volume':'Early_Vol'})
lmc_early_vol = pd.pivot_table(lmc_early_vol,values=['Early_Vol'], index=['TripDate'], aggfunc=np.sum)
del table2
#Associate Early_Vol with early dates
lmc_vol = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.sum)
lmc_std = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.std)
lmc_std = lmc_std.rename(columns={'Volume':'std_dev'})
lmc_count = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc='count')
lmc_count = lmc_count.rename(columns={'Volume':'count'})
lmc_vol['std_error']=lmc_std.std_dev/np.sqrt(lmc_count['count'])
lmc_vol ['percent_vol'] = (lmc_vol.Volume-lmc_early_vol.Early_Vol[0])/lmc_early_vol.Early_Vol[0]
lmc_vol['percent_std_error'] = (lmc_vol.std_error-lmc_vol['std_error'][0])/lmc_vol['std_error'][0]

del lmc_std, lmc_count, lmc_early_vol


with PdfPages(r'C:\workspace\Time_Series\Output\2004-2015\MC_Long_Term_percent_vol_2004.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(7,3),nrows=1)
    umc_vol.plot(y = 'percent_vol', yerr = umc_vol['percent_std_error'], ax = ax, label = 'Upper Marble Canyon')
    lmc_vol.plot(y = 'percent_vol', yerr = lmc_vol['percent_std_error'], ax = ax, label = 'Lower Marble Canyon')
    ax.set_ylabel('Percent Volume \n Normalized to 2004 volume')
    ax.set_title('Long Term Monitoring Sites')   
    pdf.savefig()
    plt.close()
del pdf

