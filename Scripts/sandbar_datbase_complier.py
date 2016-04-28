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
trip_dates = r'C:\workspace\Sandbar_Process\Date_Error_lookup.xlsx'

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
data = data.set_index(['Site','SurveyDate','Plane_Height'])
del data1, data2, data3, data4


#Load trip date lookup table
lu_3 = pd.read_excel(trip_dates)
lu_3['SurveyDate']= pd.to_datetime(lu_3['SurveyDate'], format='%m/%d/%Y')
lu_3['TripDate']= pd.to_datetime(lu_3['TripDate'], format='%m/%d/%Y')
lu_3 = lu_3[['Site','SurveyDate','Bin','TripDate']]
lu_3 = lu_3.rename(columns={'Bin':'Plane_Height'})
lu_3 = lu_3.set_index(['Site','SurveyDate','Plane_Height'])



##############Need to sort out the trip date lookup duplicates!!!!!!!!!!!!!!!!!!!!!
tmp = data.update(lu_3,join='left')

#tmp = data.reset_index().merge(lu_3.reset_index(), on=['Site','SurveyDate','Plane_Height'], how = 'left')
#tmp1 = data.merge(lu_3, how='left', left_on=['Site','SurveyDate','Plane_Height'], right_on=['Site','SurveyDate','Plane_Height'])

tmp = data.merge(lu_3,left_index=True,right_index=True,how='left')
tmp = tmp.drop(tmp.columns[[2]], axis=1)
tmp = tmp.rename(columns={'Site_x':'Site'})

tmp = tmp_data.merge(lu_3,on=['Site','SurveyDate'], how='left').set_index('Site')
tmp = data.merge(lu_3,left_index=True,right_index=True,how='left', on=['SurveyDate'])
tmp = data.merge(lu_3, left_on='SurveyDate', right_on='SurveyDate',left_index=True,right_index=True)

#Merge bar_compile with bar_trip
lu_1 = pd.read_csv(bar_trip, sep=',',index_col=[0])
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