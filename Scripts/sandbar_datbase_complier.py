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
trip_dates = r'C:\workspace\Sandbar_Process\Date_Error_lookup.xlsx'
ts_length = r'C:\workspace\sandbar_process\LU_Time_Series.xlsx'
outFileName = r'C:\workspace\Sandbar_Process\Merged_Sandbar_data.csv'

#Load in bar compile
data = pd.read_csv(bar_compile, sep=',')
data = data.drop(data.columns[[0]],axis=1)
data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y')
data = data.rename(columns={'Date':'SurveyDate'})

#Format plane Height for trip date merge
data1 = data[data.SitePart=='Eddy']
data1 = data1[data1['Plane_Height'].str.contains("minto")]
data1 = data1.assign(Plane_Height='eddyminto8k')
data2 = data[(data.SitePart=='Eddy') & (data.Plane_Height == '8kto25k')]
data2 = data2.assign(Plane_Height='eddy8kto25k')
data3 = data[(data.SitePart=='Eddy') & (data.Plane_Height == 'above25k')]
data3 = data3.assign(Plane_Height='eddyabove25k')
data4 = data[data.SitePart=='Channel']
data4 = data4.assign(Plane_Height='chanminto8k')
frames = [data1,data2,data3,data4]
data = pd.concat(frames)
del frames
del data1, data2, data3, data4


#Load trip date lookup table
lu_3 = pd.read_excel(trip_dates)
lu_3['SurveyDate']= pd.to_datetime(lu_3['SurveyDate'], format='%m/%d/%Y')
lu_3['TripDate']= pd.to_datetime(lu_3['TripDate'], format='%m/%d/%Y')
lu_3 = lu_3[['Site','SurveyDate','Bin','TripDate']]
lu_3 = lu_3.rename(columns={'Bin':'Plane_Height'})

#Drop Duplicates
lu_3 = lu_3.groupby(['Site','SurveyDate','Plane_Height']).first().reset_index()
lu_3['Site']=lu_3['Site'].str.lower()
lu_3 = lu_3.reset_index()
data = data.merge(lu_3,left_on = ['Site','SurveyDate','Plane_Height'],right_on = ['Site','SurveyDate','Plane_Height'],how='left')
data = data.drop(data.columns[[-2]],axis=1)

#Add Dates for sep and reatt bars
data1 = data[data.TripDate.isnull()]
data1 = data1.reset_index()
data1['tmpsite'] = data1['Site'].str[:4]
data1 = data1.merge(lu_3,left_on = ['tmpsite','SurveyDate','Plane_Height'],right_on = ['Site','SurveyDate','Plane_Height'],how='left')
data1 = data1.drop(data1.columns[-5:-1],axis=1)
data1 = data1.drop(data1.columns[0],axis=1)
data1 = data1.rename(columns = {'TripDate_y': 'TripDate'})
data1 = data1.rename(columns = {'Site_x': 'Site'})
data2 = data[data.TripDate.notnull()]
data = pd.concat([data1,data2])

del lu_3, data1, data2

#Merge bar_compile with bar_trip
data = data.set_index(['Site'])
lu_1 = pd.read_csv(bar_trip, sep=',',index_col=[0])
lu_1 = lu_1.rename(columns={'Range':'SiteRange'})
data = pd.merge(data,lu_1,left_index=True,right_index=True,how='left')

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
eddy_max_area = lu_2[['Max_Area_Eddy']].dropna(axis=0)
eddy_max_area = eddy_max_area.rename(columns={'Max_Area_Eddy':'Max_Area'})
chan_max_area = lu_2[['Max_Area_Channel']].dropna(axis=0)
chan_max_area = chan_max_area.rename(columns={'Max_Area_Channel':'Max_Area'})
del lu_1, lu_2

#Append maxiumum volumes in subsets
data1= data[data.SitePart == 'Channel'].merge(chan_MaxVol,left_index=True,right_index=True,how='left')
data2= data[(data.SitePart == 'Eddy') & (data.Plane_Height == 'eddy8kto25k')].merge(eddy_fz_MaxVol,left_index=True,right_index=True,how='left')
data3= data[(data.SitePart == 'Eddy')] 
data3 = data3[data3['Plane_Height'].str.contains("minto")]
data3 = data3.merge(eddy_low_MaxVol,left_index=True,right_index=True,how='left')
data4= data[(data.SitePart == 'Eddy') & (data.Plane_Height == 'eddyabove25k')].merge(eddy_he_MaxVol,left_index=True,right_index=True,how='left')

del chan_MaxVol, eddy_fz_MaxVol, eddy_he_MaxVol, eddy_low_MaxVol

#Merge Appended data sets
frames = [data1,data2,data3,data4]
data = pd.concat(frames)

del data1, data2, data3, data4, frames
#Get rid of total eddy records

data = data[np.isfinite(data['MaxVol'])]

#Merge max areas
data1= data[(data.SitePart == 'Eddy')] 
data1 = data1.merge(eddy_max_area,left_index=True,right_index=True,how='left')
data2= data[(data.SitePart == 'Channel')] 
data2 = data2.merge(chan_max_area,left_index=True,right_index=True,how='left')
data = pd.concat([data1,data2])

del data1,data2,chan_max_area,eddy_max_area

lu_4 = pd.read_excel(ts_length)
lu_4 = lu_4[['Trip_Date','Time_Series']]
lu_4 = lu_4.rename(columns={'Trip_Date':'TripDate'})
data = data.reset_index()
data= data.merge(lu_4, on=['TripDate'], how='left' )
data = data.set_index(['Site'])
del lu_4
data.to_csv(outFileName)