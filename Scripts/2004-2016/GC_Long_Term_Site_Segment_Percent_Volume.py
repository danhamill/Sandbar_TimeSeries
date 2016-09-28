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


#Eastern Grand Canyon
query1 = data[(data.Segment != '1_UMC') & (data.Segment != '2_LMC') & (data.Segment != '4_CGC') & (data.Segment != '5_WGC') & 
(data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k') & (data.SiteRange=='long')]
query1 = query1[query1['TripDate'] > '2004-01-01']
#Determine what the earliest survey was for each site
egc_early_vol = pd.pivot_table(query1,values=['TripDate'], index=['Site'], aggfunc=np.min)
table1 = pd.pivot_table(query1, values=['Volume'], index=['Site','TripDate'], aggfunc=np.sum)
egc_early_vol = pd.merge(egc_early_vol.reset_index(),table1.reset_index(),on=['Site','TripDate'],how='left')
egc_early_vol = egc_early_vol.rename(columns = {'Volume':'Early_Vol'})
egc_early_vol = pd.pivot_table(egc_early_vol,values=['Early_Vol'], index=['TripDate'], aggfunc=np.sum)
del table1
#Associate Early_Vol with early dates
egc_vol = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.sum)
egc_std = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.std)
egc_std = egc_std.rename(columns={'Volume':'std_dev'})
egc_count = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc='count')
egc_count = egc_count.rename(columns={'Volume':'count'})
egc_vol['std_error']=egc_std.std_dev/np.sqrt(egc_count['count'])
egc_vol ['percent_vol'] = (egc_vol.Volume-egc_early_vol.Early_Vol[0])/egc_early_vol.Early_Vol[0]
egc_vol['percent_std_error'] = (egc_vol.std_error-egc_vol['std_error'][0])/egc_vol['std_error'][0]

del egc_std, egc_count, egc_early_vol

#Central Grand Canyon
query2 = data[(data.Segment != '1_UMC') & (data.Segment != '2_LMC') & (data.Segment != '3_EGC') & (data.Segment != '5_WGC') & 
(data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k') & (data.SiteRange=='long')]
query2 = query2[query2['TripDate'] > '2004-01-01']
#Determine what the earliest survey was for each site
cgc_early_vol = pd.pivot_table(query2,values=['TripDate'], index=['Site'], aggfunc=np.min)
table2 = pd.pivot_table(query2, values=['Volume'], index=['Site','TripDate'], aggfunc=np.sum)
cgc_early_vol = pd.merge(cgc_early_vol.reset_index(),table2.reset_index(),on=['Site','TripDate'],how='left')
cgc_early_vol = cgc_early_vol.rename(columns = {'Volume':'Early_Vol'})
cgc_early_vol = pd.pivot_table(cgc_early_vol,values=['Early_Vol'], index=['TripDate'], aggfunc=np.sum)
del table2
#Associate Early_Vol with early dates
cgc_vol = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.sum)
cgc_std = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.std)
cgc_std = cgc_std.rename(columns={'Volume':'std_dev'})
cgc_count = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc='count')
cgc_count = cgc_count.rename(columns={'Volume':'count'})
cgc_vol['std_error']=cgc_std.std_dev/np.sqrt(cgc_count['count'])
cgc_vol ['percent_vol'] = (cgc_vol.Volume-cgc_early_vol.Early_Vol[0])/cgc_early_vol.Early_Vol[0]
cgc_vol['percent_std_error'] = (cgc_vol.std_error-cgc_vol['std_error'][0])/cgc_vol['std_error'][0]

del cgc_std, cgc_count, cgc_early_vol

#Western Grand Canyon
query3 = data[(data.Segment != '1_UMC') & (data.Segment != '2_LMC') & (data.Segment != '3_EGC') & (data.Segment != '4_CGC') & 
(data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k') & (data.SiteRange=='long')]
query3 = query3[query3['TripDate'] > '2004-01-01']
#Determine what the earliest survey was for each site
wgc_early_vol = pd.pivot_table(query3,values=['TripDate'], index=['Site'], aggfunc=np.min)
table3 = pd.pivot_table(query3, values=['Volume'], index=['Site','TripDate'], aggfunc=np.sum)
wgc_early_vol = pd.merge(wgc_early_vol.reset_index(),table3.reset_index(),on=['Site','TripDate'],how='left')
wgc_early_vol = wgc_early_vol.rename(columns = {'Volume':'Early_Vol'})
wgc_early_vol = pd.pivot_table(wgc_early_vol,values=['Early_Vol'], index=['TripDate'], aggfunc=np.sum)
del table3
#Associate Early_Vol with early dates
wgc_vol = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.sum)
wgc_std = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.std)
wgc_std = wgc_std.rename(columns={'Volume':'std_dev'})
wgc_count = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc='count')
wgc_count = wgc_count.rename(columns={'Volume':'count'})
wgc_vol['std_error']=wgc_std.std_dev/np.sqrt(wgc_count['count'])
wgc_vol ['percent_vol'] = (wgc_vol.Volume-wgc_early_vol.Early_Vol[0])/wgc_early_vol.Early_Vol[0]
wgc_vol['percent_std_error'] = (wgc_vol.std_error-wgc_vol['std_error'][0])/wgc_vol['std_error'][0]

del wgc_std, wgc_count, wgc_early_vol

with PdfPages(r'C:\workspace\Time_Series\Output\2004-2015\GC_long_Term_percent_vol_2004.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(7,6),nrows=1)
    egc_vol.plot(y = 'percent_vol', yerr = egc_vol['percent_std_error'], ax = ax, label = 'Eastern Grand Canyon')
    cgc_vol.plot(y = 'percent_vol', yerr = cgc_vol['percent_std_error'], ax = ax, label = 'Central Grand Canyon')
    wgc_vol.plot(y = 'percent_vol', yerr = wgc_vol['percent_std_error'], ax = ax, label = 'Western Grand Canyon')
    ax.set_ylabel('Percent Volume \n Normalized to 2004 volume')
    ax.set_title('Long Term Monitoring Sites')   
    pdf.savefig()
    plt.close()
del pdf

