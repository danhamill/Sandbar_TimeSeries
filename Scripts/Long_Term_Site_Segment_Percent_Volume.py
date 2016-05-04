# -*- coding: utf-8 -*-
"""
Created on Tue May 03 15:57:30 2016

@author: dan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages


#Read Data from file
#data = pd.read_csv(r'C:\workspace\Time_Series\test.csv', sep ='',index_col =[1,10])
data = pd.read_csv(r'C:\workspace\sandbar_process\Merged_Sandbar_data.csv', sep =',')


#Set Trip dates to pandas datetime
data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')


#Marble Canyon percent Volume
query1 = data[(data.Segment != '3_EGC') & (data.Segment != '4_CGC') & (data.Segment != '5_WGC') & 
(data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k') & (data.SiteRange=='long')]

#Determine what the earliest survey was for each site
mc_early_vol = pd.pivot_table(query1,values=['TripDate'], index=['Site'], aggfunc=np.min)
table1 = pd.pivot_table(query1, values=['Volume'], index=['Site','TripDate'], aggfunc=np.sum)
mc_early_vol = pd.merge(mc_early_vol.reset_index(),table1.reset_index(),on=['Site','TripDate'],how='left')
mc_early_vol = mc_early_vol.rename(columns = {'Volume':'Early_Vol'})
mc_early_vol = pd.pivot_table(mc_early_vol,values=['Early_Vol'], index=['TripDate'], aggfunc=np.sum)
del table1
#Associate Early_Vol with early dates
mc_vol = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.sum)
mc_std = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc=np.std)
mc_std = mc_std.rename(columns={'Volume':'std_dev'})
mc_count = pd.pivot_table(query1, values=['Volume'], index=['TripDate'], aggfunc='count')
mc_count = mc_count.rename(columns={'Volume':'count'})
mc_vol['std_error']=mc_std.std_dev/np.sqrt(mc_count['count'])
mc_vol ['percent_vol'] = (mc_vol.Volume-mc_early_vol.Early_Vol[0])/mc_early_vol.Early_Vol[0]
mc_vol['percent_std_error'] = (mc_vol.std_error-mc_vol['std_error'][0])/mc_vol['std_error'][0]

del mc_std, mc_count, mc_early_vol
#Grand Canyon percent Volume
query2 = data[(data.Segment != '1_UMC') & (data.Segment != '2_LMC') &
(data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k') & (data.SiteRange=='long')]

#Determine what the earliest survey was for each site
gc_early_vol = pd.pivot_table(query2,values=['TripDate'], index=['Site'], aggfunc=np.min)
table1 = pd.pivot_table(query2, values=['Volume'], index=['Site','TripDate'], aggfunc=np.sum)
gc_early_vol = pd.merge(gc_early_vol.reset_index(),table1.reset_index(),on=['Site','TripDate'],how='left')
gc_early_vol = gc_early_vol.rename(columns = {'Volume':'Early_Vol'})
gc_early_vol = pd.pivot_table(gc_early_vol,values=['Early_Vol'], index=['TripDate'], aggfunc=np.sum)
del table1
gc_vol = pd.pivot_table(query2, values=['Volume'], index=['TripDate'], aggfunc=np.sum)
gc_std = pd.pivot_table(query2, values=['Volume'], index=['TripDate'], aggfunc=np.std)
gc_std = gc_std.rename(columns={'Volume':'std_dev'})
gc_count = pd.pivot_table(query2, values=['Volume'], index=['TripDate'], aggfunc='count')
gc_count = gc_count.rename(columns={'Volume':'count'})
gc_vol['std_error']=gc_std.std_dev/np.sqrt(gc_count['count'])
gc_vol ['percent_vol'] = (gc_vol.Volume-gc_early_vol.Early_Vol[0])/gc_early_vol.Early_Vol[0]
gc_vol['percent_std_error'] = (gc_vol.std_error-gc_vol['std_error'][0])/gc_vol['std_error'][0]
del gc_std, gc_count, gc_early_vol

with PdfPages(r'C:\workspace\Time_Series\Output\Short_Term_percent_vol.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(7,3),nrows=1)
    mc_vol.plot(y = 'percent_vol', yerr = mc_vol['percent_std_error'], ax = ax, label = 'Marble Canyon')
    gc_vol.plot(y = 'percent_vol', yerr = gc_vol['percent_std_error'], ax = ax, label = 'Grand Canyon')
    ax.set_ylabel('Percent Volume \n Normalized to 1990 volume')
    ax.set_title('Long Term Monitoring Sites')   
    pdf.savefig()
    plt.close()
del pdf

