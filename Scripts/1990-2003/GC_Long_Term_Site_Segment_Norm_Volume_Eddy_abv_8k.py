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
(data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.SiteRange=='long')]
query1 = query1[query1['TripDate'] < '2004-01-01']

#Determine what the earliest survey was for each site
table1 = pd.pivot_table(query1, values=['Volume', 'MaxVol'], index=['TripDate'], aggfunc=np.sum)
table1['NormVol']= table1['Volume']/table1['MaxVol']
table1 = table1[['NormVol']]



#Central Grand Canyon
query2 = data[(data.Segment != '1_UMC') & (data.Segment != '2_LMC') & (data.Segment != '3_EGC') & (data.Segment != '5_WGC') & 
(data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.SiteRange=='long')]
query2 = query2[query2['TripDate'] < '2004-01-01']

table2 = pd.pivot_table(query2, values=['Volume', 'MaxVol'], index=['TripDate'], aggfunc=np.sum)
table2['NormVol']= table2['Volume']/table2['MaxVol']
table2 = table2[['NormVol']]

#Western Grand Canyon
query3 = data[(data.Segment != '1_UMC') & (data.Segment != '2_LMC') & (data.Segment != '3_EGC') & (data.Segment != '4_CGC') & 
(data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.SiteRange=='long')]
query3 = query3[query3['TripDate'] < '2004-01-01']

table3 = pd.pivot_table(query3, values=['Volume', 'MaxVol'], index=['TripDate'], aggfunc=np.sum)
table3['NormVol']= table3['Volume']/table3['MaxVol']
table3 = table3[['NormVol']]

with PdfPages(r'C:\workspace\Time_Series\Output\GC_long_Term_Norm_Vol_1990.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(7,6),nrows=1)
    table1.plot(y = 'NormVol', ax = ax, label = 'Eastern Grand Canyon')
    table2.plot(y = 'NormVol', ax = ax, label = 'Central Grand Canyon')
    table3.plot(y = 'NormVol', ax = ax, label = 'Western Grand Canyon')
    ax.set_ylabel('Normalized Volume [m$^3$/m$^3$] \n Normalized to Maximum Volume')
    ax.set_title('Long Term Monitoring Sites: Eddy above 8k')   
    pdf.savefig()
    plt.close()
del pdf

