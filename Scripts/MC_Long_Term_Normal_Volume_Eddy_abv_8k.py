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
(data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.SiteRange=='long')]

table1 = pd.pivot_table(query1, values=['Volume', 'MaxVol'], index=['TripDate'], aggfunc=np.sum)
table1['NormVol']= table1['Volume']/table1['MaxVol']
table1 = table1[['NormVol']]
#Lower Marble Canyon
query2 = data[(data.Segment != '1_UMC') & (data.Segment != '3_EGC') & (data.Segment != '4_CGC') & (data.Segment != '5_WGC') & 
(data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k') & (data.SiteRange=='long')]

table2 = pd.pivot_table(query2, values=['Volume','MaxVol'], index=['TripDate'], aggfunc=np.sum)
table2['NormVol']= table2['Volume']/table2['MaxVol']
table2 = table2[['NormVol']]

with PdfPages(r'C:\workspace\Time_Series\Output\MC_Long_Term_Norm_Vol_eddyabv8k.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(7,3),nrows=1)
    table1.plot(y = 'NormVol', ax = ax, label = 'Upper Marble Canyon')
    table2.plot(y = 'NormVol', ax = ax, label = 'Lower Marble Canyon')
    ax.set_ylabel('Normalized Volume [m$^3$/m$^3$] \n Normalized to Maximum Volume')
    ax.set_title('Long Term Monitoring Sites: Eddy Above 8k')   
    pdf.savefig()
    plt.close()
del pdf

