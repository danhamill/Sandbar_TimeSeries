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
query1 = data[(data.Segment != '1_UMC') & (data.Segment != '2_LMC') & (data.Segment != '4_CGC') & (data.Segment != '5_WGC')  & (data.Segment != '0_Glen') & 
(data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.SiteRange=='short')& (data.Bar_type != 'Total')& (data.Time_Series == 'short')]
query1 = query1[query1['TripDate'] > '2004-01-01']

#Determine errors for norm volume
temp = query1
temp = pd.pivot_table(temp,values=['Volume','MaxVol'],index=['Site','SurveyDate','TripDate'], aggfunc= np.sum)
temp['NormVol'] = temp['Volume']/temp['MaxVol']
tmp_pvt = pd.pivot_table(temp.reset_index(), values=['NormVol'], index=['TripDate'], aggfunc=np.std)
tmp_pvt = tmp_pvt.rename(columns={'NormVol':'std_dev'})
tmp_count = pd.pivot_table(temp.reset_index(),values=['NormVol'], index=['TripDate'], aggfunc='count')
tmp_count = tmp_count.rename(columns={'NormVol':'count'})
tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
tmp_pvt = tmp_pvt[['std_error']]

#Determine what the earliest survey was for each site
table1 = pd.pivot_table(query1, values=['Volume', 'MaxVol'], index=['TripDate'], aggfunc=np.sum)
table1['NormVol']= table1['Volume']/table1['MaxVol']
table1 = table1[['NormVol']]
table1 = table1.merge(tmp_pvt, left_index=True, right_index=True, how='left')
del temp, tmp_pvt, tmp_count



#Central Grand Canyon
#query2 = data[(data.Segment != '1_UMC') & (data.Segment != '2_LMC') & (data.Segment != '3_EGC') & (data.Segment != '5_WGC')  & (data.Segment != '0_Glen') & 
#(data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.SiteRange=='short') & (data.Bar_type != 'Total') & (data.Time_Series == 'short')]
#query2 = query2[query2['TripDate'] > '2004-01-01']
#
#temp = query2
#temp['NormVol'] = temp['Volume']/temp['MaxVol']
#tmp_pvt = pd.pivot_table(temp, values=['NormVol'], index=['TripDate'], aggfunc=np.std)
#tmp_pvt = tmp_pvt.rename(columns={'NormVol':'std_dev'})
#tmp_count = pd.pivot_table(temp,values=['NormVol'], index=['TripDate'], aggfunc='count')
#tmp_count = tmp_count.rename(columns={'NormVol':'count'})
#tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
#tmp_pvt = tmp_pvt[['std_error']]
#
#table2 = pd.pivot_table(query2, values=['Volume', 'MaxVol'], index=['TripDate'], aggfunc=np.sum)
#table2['NormVol']= table2['Volume']/table2['MaxVol']
#table2 = table2[['NormVol']]
#table2 = table2.merge(tmp_pvt, left_index=True, right_index=True, how='left')
#del temp, tmp_pvt, tmp_count

#Western Grand Canyon
query3 = data[(data.Segment != '1_UMC') & (data.Segment != '2_LMC') & (data.Segment != '3_EGC') & (data.Segment != '4_CGC') & (data.Segment != '0_Glen')& 
(data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.SiteRange=='short')& (data.Bar_type != 'Total')& (data.Time_Series == 'short')]
query3 = query3[query3['TripDate'] > '2004-01-01']

temp = query3
temp = pd.pivot_table(temp,values=['Volume','MaxVol'],index=['Site','SurveyDate','TripDate'], aggfunc= np.sum)
temp['NormVol'] = temp['Volume']/temp['MaxVol']
tmp_pvt = pd.pivot_table(temp.reset_index(), values=['NormVol'], index=['TripDate'], aggfunc=np.std)
tmp_pvt = tmp_pvt.rename(columns={'NormVol':'std_dev'})
tmp_count = pd.pivot_table(temp.reset_index(),values=['NormVol'], index=['TripDate'], aggfunc='count')
tmp_count = tmp_count.rename(columns={'NormVol':'count'})
tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
tmp_pvt = tmp_pvt[['std_error']]

table3 = pd.pivot_table(query3, values=['Volume', 'MaxVol'], index=['TripDate'], aggfunc=np.sum)
table3['NormVol']= table3['Volume']/table3['MaxVol']
table3 = table3[['NormVol']]
table3 = table3.merge(tmp_pvt, left_index=True, right_index=True, how='left')
del temp, tmp_pvt, tmp_count

with PdfPages(r'C:\workspace\Time_Series\Output\2004-2015\GC_short_Term_Norm_Vol_eddyabv8k_w_err_bars.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(7,6),nrows=1)
    table1.plot(y = 'NormVol', yerr = 'std_error', ax = ax, label = 'Eastern Grand Canyon')
    #table2.plot(y = 'NormVol', yerr = 'std_error', ax = ax, label = 'Central Grand Canyon')
    table3.plot(y = 'NormVol', yerr = 'std_error', ax = ax, label = 'Western Grand Canyon')
    ax.set_ylabel('Normalized Volume [m$^3$/m$^3$] \n Normalized to Maximum Volume')
    ax.set_title('Short Term Monitoring Sites: Eddy above 8k')   
    pdf.savefig()
    plt.close()
del pdf

