# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

max_vol = r'C:\workspace\Sandbar_Process\LU_Max_Vol.xlsx'
bar_compile = r'C:\workspace\Sandbar_Process\csv_output\Sandbar_data.csv'
bar_trip = r'C:\workspace\Sandbar_Process\LU_Site_location_time_Series.csv' 
outFileName = r'C:\workspace\Sandbar_Process\Merged_Sandbar_data.csv'

#Load in bar compile
data = pd.read_csv(bar_compile, sep=',', index_col=[1])
data = data.drop(data.columns[[0]],axis=1)

#Merge bar_compile with bar_trip
lu_1 = pd.read_csv(bar_trip, sep=',',index_col=[0])
data = data.merge(lu_1,left_index=True,right_index=True,how='left')

#Load max_vol
lu_2 = pd.read_excel(max_vol, index_col=[0])

#Format max_vol for merging
chan_MaxVol = lu_2[['MaxVol_ChMinTo8k']].dropna(axis=0)
chan_MaxVol=chan_MaxVol.rename(columns={'MaxVol_ChMinTo8k':'MaxVol'})
eddy_low_MaxVol = lu_2[['MaxVol_EdMinTo8k']].dropna(axis=0)
eddy_low_MaxVol = eddy_low_MaxVol.rename(columns = {'MaxVol_EdMinTo8k':'MaxVol'})
eddy_fz_MaxVol = lu_2[['MaxVol_Ed8kto25k']].dropna(axis=0)
eddy_fz_MaxVol = eddy_fz_MaxVol.rename(columns = {'MaxVol_Ed8kto25k':'MaxVol'})
eddy_he_MaxVol = lu_2[['MaxVol_EdAbv25k']].dropna(axis=0)
eddy_he_MaxVol = eddy_he_MaxVol.rename(columns = {'MaxVol_EdAbv25k':'MaxVol'})

del lu_1, lu_2

#Append maxiumum volumes in subsets
data1= data[data.SitePart == 'Channel'].merge(chan_MaxVol,left_index=True,right_index=True,how='left')
data2= data[(data.SitePart == 'Eddy') & (data.Plane_Height == '8kto25k')].merge(eddy_fz_MaxVol,left_index=True,right_index=True,how='left')
data3= data[(data.SitePart == 'Eddy')] 
data3 = data3[data3['Plane_Height'].str.contains("minto")]
data3 = data3.merge(eddy_low_MaxVol,left_index=True,right_index=True,how='left')
data4= data[(data.SitePart == 'Eddy') & (data.Plane_Height == 'above25k')].merge(eddy_he_MaxVol,left_index=True,right_index=True,how='left')

del chan_MaxVol, eddy_fz_MaxVol, eddy_he_MaxVol, eddy_low_MaxVol

#Merge Appended data sets
frames = [data1,data2,data3,data4]
data = pd.concat(frames)

del data1, data2, data3, data4
#Get rid of total eddy records
data = data[np.isfinite(data['MaxVol'])]
data.to_csv(outFileName)