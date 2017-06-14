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
import pytablewriter

def markdown_df(df):
    writer = pytablewriter.MarkdownTableWriter()
    writer.table_name = "example_table"
    writer.header_list = list(df.columns.values)
    writer.value_matrix = df.values.tolist()
    writer.write_table()
    
    
def query_df(df):
    '''
    Functon to subset data dataframe to Marble Canyon Sediment Enricnment Period
    '''
    tmp = df
    mc_query = 'Segment == ["1_UMC","2_LMC"]'
    tmp = tmp.query(mc_query)
    tmp['TripDate'] = pd.to_datetime(tmp['TripDate'], format='%Y-%m-%d')
    tmp = tmp[tmp['TripDate'] >= '2003-09-20']
    tmp = tmp[(tmp['Time_Series']!= 'na') & (tmp['SitePart'] == 'Eddy')]
    tmp = tmp[tmp['Plane_Height'] != 'eddyminto8k']
    tmp = tmp[(tmp['Site'] != '009l') &(tmp['Site'] != '035l_r')&(tmp['Site'] != '035l_r') & (tmp['Site'] != '045l_s')]
    return tmp

def vol_norm_data(df,section=None):
    if section is not None:
        df=df.query(section)
    df = pd.pivot_table(df,index=['Site','SurveyDate','SitePart','TripDate','SiteRange','Segment','Bar_type','Time_Series','Period'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()
    df['Norm_Vol'] = df['Volume']/df['MaxVol']
    tmp_pvt = pd.pivot_table(df, values=['Norm_Vol'], index=['TripDate'], aggfunc=np.std)
    tmp_pvt = tmp_pvt.rename(columns={'Norm_Vol':'std_dev'})
    tmp_count = pd.pivot_table(df,values=['Norm_Vol'], index=['TripDate'], aggfunc='count')
    tmp_count = tmp_count.rename(columns={'Norm_Vol':'count'})
    tmp_pvt['std_error'] = tmp_pvt['std_dev']/np.sqrt(tmp_count['count'])
    yerr = tmp_pvt[['std_error']]
    del tmp_count, tmp_pvt
    tmp_pvt = pd.pivot_table(df, values=['Norm_Vol'], index=['TripDate'], aggfunc=np.average)
    tmp_2 = pd.pivot_table(df, values=['Norm_Vol'], index=['TripDate'], aggfunc=[len,np.mean,np.std,np.min,np.max])
    
    tmp_pvt['y_err']=yerr
    return tmp_pvt, tmp_2
    
def pivot_df(df):
    lt_pvt = pd.pivot_table(df, values=['Volume','MaxVol','Area_2D','Max_Area'],index=['TripDate'],aggfunc=np.sum)
    lt_pvt['Norm_Vol'] = lt_pvt['Volume']/lt_pvt['MaxVol']
    lt_pvt['Norm_Error'] = lt_pvt['Area_2D']/lt_pvt['Max_Area']
    lt_pvt = lt_pvt[['Norm_Vol','Norm_Error']]
    return lt_pvt
    


def change_finder(extra_sites,long_term, all_sites):
    '''
    Function to calculate % difference between long term site time series 
    and bootstrapped all sties time series
    '''
    for n in xrange(len(extra_sites)):
        
        #subset all sites to drop one value
        drop_site = extra_sites.iloc[n][0]
        sites2test =all_sites[all_sites.Site != drop_site]
    
        #Find normal Volumes 
        long_t = pivot_df(long_term)
        all_s = pivot_df(sites2test)
        date_influence = (all_s['Norm_Vol'] - long_t['Norm_Vol'])/(all_s['Norm_Vol'])
        date_influence = date_influence.rename('Pct_Change')
        long_t= pd.pivot_table(long_t.reset_index(), index=['TripDate'], values=['Norm_Vol'])
        all_s = pd.pivot_table(all_s.reset_index(), index=['TripDate'], values=['Norm_Vol'])
        
        if n == 0:
            in_df=None
            in_df2 = None
            df_back, df2_back = merge_df(long_t,all_s,drop_site,in_df,date_influence,in_df2)
        else:
            df_back, df2_back = merge_df(long_t,all_s,drop_site,df_back,date_influence,df2_back)
        
    return df_back, df2_back
        
def merge_df(long_t,all_s, drop_site,in_df,date_influence,in_df2):
    if in_df is None:
        vol_diff = (-long_t['Norm_Vol'].sum(axis=0)+all_s['Norm_Vol'].sum(axis=0))/(all_s['Norm_Vol'].sum(axis=0))
        out_df = pd.DataFrame(data=[vol_diff], columns=['Vol_Change'],index=[drop_site])
        date_influence_out = pd.DataFrame({'Pct_Change':date_influence, 'Site':drop_site})
        return out_df, date_influence_out
    elif in_df is not None:
        vol_diff = (-long_t['Norm_Vol'].sum(axis=0)+all_s['Norm_Vol'].sum(axis=0))/(all_s['Norm_Vol'].sum(axis=0))
        out_df = pd.concat([in_df,pd.DataFrame(data=[vol_diff], columns=['Vol_Change'],index=[drop_site])])
        date_influence_out = pd.concat([in_df2,pd.DataFrame({'Pct_Change':date_influence, 'Site':drop_site})])
        return out_df, date_influence_out

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
    

    
#    #Find extra sites
#    all_site_df = pd.DataFrame(data=all_sites.Site.unique(),columns=['Site'])
#    lt_site_df = pd.DataFrame(data=long_term.Site.unique(),columns=['Site'])
#    extra_sites = all_site_df[~all_site_df.isin(set(lt_site_df['Site']))].dropna()
#    
#    #find influence of extra sites
#    influence_df, date_influence = change_finder(extra_sites,long_term,all_sites)
#    
#    #reformat date influence to be pivoted on site and display data columnwise
#    date_influence = pd.pivot_table(date_influence.reset_index(), index=['TripDate'],values=['Pct_Change'],columns=['Site'])
#    date_influence.columns = date_influence.columns.droplevel()
#    markdown_df(date_influence)
    #Data to plot                 
    long_term_plt,long_term_tbl = vol_norm_data(long_term)
    all_sites_plt,all_sites_tbl = vol_norm_data(all_sites)
    
    label_mc = 'Mable Canyon: N=' + str(len(long_term['Site'].unique()))
    label_mc1 ='Marble Canyon: N=' + str(len(all_sites['Site'].unique()))
    
    fig,ax = plt.subplots(figsize=(7.5,3.33))
    long_term_plt.plot(y = 'Norm_Vol', yerr='y_err',ax = ax, label = label_mc, color='blue',marker='o')
    all_sites_plt.plot(y = 'Norm_Vol', yerr='y_err',ax = ax, label = label_mc1, color='green',linestyle='--',marker='x')
    ax.set_ylabel('Normalized Sandbar Volume')
    ax.set_xlabel('Date')
    ax.set_xlim(pd.Timestamp('2003-01-01'), pd.Timestamp('2017-01-01'))
    ax.set_ylim(0.2,0.7)
    ax.legend(loc=9, ncol=2,fontsize=10)
    plt.tight_layout()
    plt.savefig(oName,dpi=600)
    

    
    df = pd.DataFrame(columns=['d','std'])
    df.loc[:,'d'] = long_term_plt.Norm_Vol-all_sites_plt.Norm_Vol
    
    t = np.mean(df['d'])/(np.std(df['d'])/np.sqrt(14))
    
    from scipy.stats import ttest_ind, wilcoxon
    
    t, p = ttest_ind(long_term_plt.Norm_Vol,all_sites_plt.Norm_Vol)
    t_w, p_w = wilcoxon(long_term_plt.Norm_Vol,all_sites_plt.Norm_Vol)
    
    fig, (ax,ax1) = plt.subplots(nrows=2)
    
    


