# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:23:27 2017

@author: dan
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

import pytablewriter


df= pd.read_excel(r"C:\Users\dan\Downloads\rob_comparison.xlsx",sheetname='8-25k')

df = df[["Site","Volume_wb",'Area_2D','Volume','SurveyDate']]


fig , ax =plt.subplots(11,5,sharex=True,sharey=True,figsize=(15,150))


df2 = pd.DataFrame(columns=['Slope','r_squared'],index=df.Site.unique())
df2.Site = df.Site.unique()
n=0
labels=[]
for name, group in df.groupby('Site'):
    s,i,r,p,std_error = linregress(group['Volume'],group['Volume_wb'])
    
    s = '%1.4f' %s
    r = '%1.4f' %r**2
    df2.loc[name] = pd.Series({'Slope':s,'r_squared':r})
    label = name + ' slope: ' + s + ', R$^2$: '+ r
    labels.append(label)
    group.plot(kind='scatter',x='Volume',y='Volume_wb',label=name,ax=fig.axes[n])
    fig.axes[n].plot(group['Volume'],i+group['Volume']*linregress(group['Volume'],group['Volume_wb'])[0],'k')

    n+=1

del s,i,r,p,std_error,n
[i.legend_.remove() for i in fig.axes[0:-1]]
[i.set_ylabel('WB_Vol',fontsize='x-small') for i in fig.axes[0:-1]]
[i.set_xlabel('TinVol',fontsize='x-small') for i in fig.axes[0:-1]]
handles = []
    
[handles.append(i.get_legend_handles_labels()[0][0]) for i in fig.axes[0:-1]]


fig.legend(handles = handles, labels=labels, loc = 'lower center', bbox_to_anchor = (0,0.005,1,1),
        bbox_transform = fig.transFigure,ncol=5)
fig.tight_layout()
df2=df2.reset_index()
writer = pytablewriter.MarkdownTableWriter()
writer.table_name = "Site-by-Site Method Volume Regression Analysis"
writer.header_list = list(df2.columns.values)
writer.value_matrix = df2.values.tolist()
writer.write_table()   