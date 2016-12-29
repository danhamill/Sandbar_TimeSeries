#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:07:11 2016

@author: danielhamill
"""

import pandas as pd
import platform
import numpy as np
import matplotlib.pyplot as plt


def query_df(df):
    '''
    Functon to subset data dataframe to Marble Canyon Sediment Enricnment Period
    '''
    tmp = df
    mc_query = 'Segment == ["1_UMC","2_LMC"]'
    tmp.query(mc_query,inplace=True)
    tmp.query('Period == ["Sediment_Enrichment"]',inplace = True)
    tmp.query('Time_Series ==["long"]')
    tmp['TripDate'] = pd.to_datetime(tmp['TripDate'], format='%Y-%m-%d')
    return tmp

    
def pivot_df(df):
    lt_pvt = pd.pivot_table(df, values=['Volume','MaxVol','Area_2D','Max_Area'],index=['TripDate'],aggfunc=np.sum)
    lt_pvt['Norm_Vol'] = lt_pvt['Volume']/lt_pvt['MaxVol']
    lt_pvt['Norm_Error'] = lt_pvt['Area_2D']/lt_pvt['Max_Area']
    lt_pvt = lt_pvt[['Norm_Vol','Norm_Error']]
    return lt_pvt
    


def change_finder(extra_sites,long_term, all_sites):
    
    for n in xrange(len(extra_sites)):
        
        #subset all sites to drop one value
        drop_site = extra_sites.iloc[n][0]
        sites2test =all_sites[all_sites.Site != drop_site]
    
        #Find normal Volumes 
        long_t = pivot_df(long_term)
        all_s = pivot_df(sites2test)
    
        long_t= pd.pivot_table(long_t.reset_index(), index=['TripDate'], values=['Norm_Vol'])
        all_s = pd.pivot_table(all_s.reset_index(), index=['TripDate'], values=['Norm_Vol'])
        
        if n == 0:
            in_df=None
            df_back = merge_df(long_t,all_s,drop_site,in_df)
        else:
            df_back = merge_df(long_t,all_s,drop_site,df_back)
        
    return df_back
        
def merge_df(long_t,all_s, drop_site,in_df):
    if in_df is None:
        vol_diff = (-long_t['Norm_Vol'].sum(axis=0)+all_s['Norm_Vol'].sum(axis=0))/(all_s['Norm_Vol'].sum(axis=0))
        out_df = pd.DataFrame(data=[vol_diff], columns=['Vol_Change'],index=[drop_site])
        return out_df
    elif in_df is not None:
        vol_diff = (-long_t['Norm_Vol'].sum(axis=0)+all_s['Norm_Vol'].sum(axis=0))/(all_s['Norm_Vol'].sum(axis=0))
        out_df = pd.concat([in_df,pd.DataFrame(data=[vol_diff], columns=['Vol_Change'],index=[drop_site])])
        return out_df

if __name__ == '__main__':
    if platform.system() == 'Darwin':
        db_file = '/Users/danielhamill/git_clones/sandbar_process/Merged_Sandbar_data.csv'
        lt_sites ='/Users/danielhamill/git_clones/Time_Series/sites.xlsx'
        oName = '/Users/danielhamill/git_clones/Time_Series/output/mc_variability.png'
    elif platform.system() == 'Windows':
        db_file = r'C:\workspace\sandbar_process\Merged_Sandbar_data.csv'
        lt_sites = r"C:\workspace\Time_Series\sites.xlsx"
        oName = r'C:\workspace\Time_Series\output\mc_variability.png'
        
    #Load Database    
    data = pd.read_csv(db_file,sep=',')    
    
    #Load long term monitoring sites
    lu_sites = pd.read_excel(lt_sites)
    lu_sites = lu_sites[['Sediment Deficit Sites']].dropna()
    
    
    #Subset long term monitoring sites
    long_term = data[data['Site'].isin(set(lu_sites['Sediment Deficit Sites']))]
      
    
    #Get data for plotting
    long_term = query_df(long_term)
    all_sites = query_df(data)
    all_sites = all_sites.query('Bar_type != "Total"')
    
    #Find extra sites
    all_site_df = pd.DataFrame(data=all_sites.Site.unique(),columns=['Site'])
    lt_site_df = pd.DataFrame(data=long_term.Site.unique(),columns=['Site'])
    extra_sites = all_site_df[~all_site_df.isin(set(lt_site_df['Site']))].dropna()
    
    #find influence of extra sites
    influence_df = change_finder(extra_sites,long_term,all_sites)
    
    #Data to plot                 
    long_term = pivot_df(long_term)
    all_sites = pivot_df(all_sites)
    
    fig,ax = plt.subplots()
    long_term.plot(y = 'Norm_Vol', yerr='Norm_Error',ax = ax, label = 'Marble Canyon N=12',color='blue',marker='o')
    all_sites.plot(y = 'Norm_Vol', yerr='Norm_Error',ax = ax, label = 'Marble Canyon N=30',color='green',linestyle='--',marker='x')
    plt.tight_layout()
    #plt.savefig(oName,dpi=600)
    plt.show()




