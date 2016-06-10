# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:18:58 2016

@author: dan
"""
import pandas as pd
import numpy as np
data = pd.read_csv(r'C:\workspace\sandbar_process\Merged_Sandbar_data.csv', sep =',')
query1 = data[(data['SurveyDate']>'2014-01-01') & (data['SurveyDate']<'2015-01-01')]
query2 = data[ (data['SurveyDate']>'2015-01-01')]
data = data.reset_index()

table1 = pd.pivot_table(query1,values=['Volume'],index=['Site','SurveyDate'], aggfunc=np.sum)
table2 = pd.pivot_table(query2,values=['Volume'],index=['Site','SurveyDate'], aggfunc=np.sum)

table1 = table1.reset_index(level=1)
table2 = table2.reset_index(level=1)



table2 = table2.merge(table1,left_index=True,right_index=True,how='left')

table2['VolChange']= table2.Volume_x-table2.Volume_y
table2.to_csv(r'C:\workspace\Time_Series\output\15T014Change.csv',sep=',')