# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 15:26:23 2017

@author: dan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform
import os
from matplotlib import dates
import matplotlib.ticker as tkr

def std_err_calc(df,metric):
        mc_std = pd.pivot_table(df, values=[metric], index=['TripDate'], aggfunc=np.std)
        mc_std = mc_std.rename(columns={metric:'std_dev'})
        mc_count = pd.pivot_table(df, values=[metric], index=['TripDate'], aggfunc='count')
        mc_count = mc_count.rename(columns={metric:'count'})    
        return mc_std.std_dev/np.sqrt(mc_count['count'])
    
def format_xaxis(fig):
     years = dates.YearLocator(10,month=1,day=1)
     years1=dates.YearLocator(2,month=1,day=1)
     dfmt = dates.DateFormatter('%Y')
     dfmt1 = dates.DateFormatter('%y')
    
     [i.xaxis.set_major_locator(years) for i in fig.axes]
     [i.xaxis.set_minor_locator(years1) for i in fig.axes]
     [i.xaxis.set_major_formatter(dfmt) for i in fig.axes]
     [i.xaxis.set_minor_formatter(dfmt1) for i in fig.axes]
     [i.get_xaxis().set_tick_params(which='major', pad=15) for i in fig.axes]
    
     for t in fig.axes:
         for tick in t.xaxis.get_major_ticks():
             tick.label1.set_horizontalalignment('center')
         for label in t.get_xmajorticklabels() :
             label.set_rotation(0)
             label.set_weight('bold')
         for label in t.xaxis.get_minorticklabels():
             label.set_fontsize('small')
         for label in t.xaxis.get_minorticklabels()[::5]:
             label.set_visible(False)
 

    

if __name__ =='__main__':
    
    if platform.system() == 'Darwin':
        sandbar_root = '/Users/danielhamill/git_clones/sandbar_process'
        time_root = '/Users/danielhamill/git_clones/Time_Series'
        out_root = time_root + os.sep + 'Output/Joes_figs'
    elif platform.system() == 'Windows':
        sandbar_root = r'C:\workspace\sandbar_process'
        time_root = r'C:\workspace\Time_Series'
        out_root = time_root + os.sep + r'Output\Joes_figs'
        
    #designate groups       
    g_1a = np.array(['145l','022r','213l','084r','030r','081l','137l','119r','122r'])
    g_1b = np.array(['009l','123l','172l','044l','045l','044l','183r','220r','050r','065r','047r'])
    g_1c = np.array(['070r','194l','068r','051l','055r'])
    g_2 = np.array(['008l','024l','029l','032r','056r','167l'])
    g_3 = np.array(['044lr','087l','093l','139r','225r','104r'])
    g_4 = np.array(['016l','033l','035l','062r','091r','202r'])        
        
##########################################################################################################################################   
###############################    All Available Data Plots     ############################################################################
#########################################################################################################################################    #Read Data from file
    data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
    data = pd.read_csv(data_file, sep =',')
    
    data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

    #Preallocate Figures
    
    fig_0, ((ax_0,ax1_0),(ax2_0,ax3_0),(ax4_0,ax5_0)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_1, ((ax_1,ax1_1),(ax2_1,ax3_1),(ax4_1,ax5_1)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_2, ((ax_2,ax1_2),(ax2_2,ax3_2),(ax4_2,ax5_2)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_3, ((ax_3,ax1_3),(ax2_3,ax3_3),(ax4_3,ax5_3)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))

    
    axes = [[ax_0,ax_1,ax_2,ax_3],
            [ax1_0,ax1_1,ax1_2,ax1_3],
            [ax2_0,ax2_1,ax2_2,ax2_3],
            [ax3_0,ax3_1,ax3_2,ax3_3],
            [ax4_0,ax4_1,ax4_2,ax4_3],
            [ax5_0,ax5_1,ax5_2,ax5_3,]] 
    n=0
    for group1 in [g_1a,g_1b,g_1c,g_2,g_3,g_4]:
        if np.array_equal(g_1b,group1): 
            group1 = np.append(g_1b,[['003l']])
            print group1
        ax_plot = axes[n]
        subset = data[data['Site'].isin(group1)]
        
        #Page 1 Volume less than 8
        for name, group in subset[subset['Plane_Height'] == 'eddyminto8k'].groupby('Site'):
            group.plot(x='TripDate',y='Volume',ax=ax_plot[0],label=name)
        # Shrink current axis by 20%
        box = ax_plot[0].get_position()
        ax_plot[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax_plot[0].legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize='small',handlelength=1)    
        
        #page 2 FZ Volume
        for name, group in subset[subset['Plane_Height'] == 'eddy8kto25k'].groupby('Site'):
            group.plot(x='TripDate',y='Volume',ax=ax_plot[1],label=name)
        box = ax_plot[1].get_position()
        ax_plot[1].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax_plot[1].legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize='small',handlelength=1) 
        
        subset = subset[(subset.Plane_Height != 'eddyminto8k') & (subset['SitePart'] == 'Eddy')]     
        date_fz = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddy8kto25k') ].SurveyDate.unique()
        date_he = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddyabove25k') ].SurveyDate.unique()
        common_dates = np.intersect1d(date_fz,date_he)
        subset = subset[subset['SurveyDate'].isin(common_dates)]
        subset =  pd.pivot_table(subset,index=['Site','SurveyDate','SitePart','TripDate','SiteRange','Segment','Bar_type','Time_Series','Period'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()
        #page 3 Area above 8k
        for name, group in subset[subset['SitePart'] == 'Eddy'].groupby('Site'):
            group.plot(x='TripDate',y='Area_2D',ax=ax_plot[2],label=name)        
        ax_plot[2].legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize='small',handlelength=1) 
        box = ax_plot[2].get_position()
        ax_plot[2].set_position([box.x0, box.y0, box.width * 0.8, box.height])        
        #page 4 volume above 8k
        for name, group in subset[subset['SitePart'] == 'Eddy'].groupby('Site'):
            group.plot(x='TripDate',y='Volume',ax=ax_plot[3],label=name) 
        box = ax_plot[3].get_position()
        ax_plot[3].set_position([box.x0, box.y0, box.width * 0.8, box.height])            
        ax_plot[3].legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize='small',handlelength=1) 
        n+=1
        
    [t.set_title('Group 1a') for t in axes[0]]
    [t.set_title('Group 1b') for t in axes[1]]
    [t.set_title('Group 1c') for t in axes[2]]
    [t.set_title('Group 2') for t in axes[3]]
    [t.set_title('Group 3') for t in axes[4]]
    [t.set_title('Group 4') for t in axes[5]]
    
    
    [t.set_xlabel('') for t in axes[0]]
    [t.set_xlabel('') for t in axes[1]]
    [t.set_xlabel('') for t in axes[2]]
    [t.set_xlabel('') for t in axes[3]]
    [t.set_xlabel('') for t in axes[4]]
    [t.set_xlabel('') for t in axes[5]]
    
    for i , ax in enumerate(fig_3.axes):
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
        ax.set_ylabel('VOLUME, IN CUBIC METERS')
    for i , ax in enumerate(fig_2.axes):
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
        ax.set_ylabel('AREA, IN METERS SQUARED')
    for i , ax in enumerate(fig_1.axes):
        ax.set_ylabel('VOLUME, IN CUBIC METERS')
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))   
    #Eddy Min to 8k <---- ends at 2010 because that was the last time 
    for i , ax in enumerate(fig_0.axes):
        ax.set_ylabel('VOLUME, IN CUBIC METERS')
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2010,01,01)) 
        
        
    [format_xaxis(t) for t in [fig_0,fig_1,fig_2,fig_3]]
    
    
    [t.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ','))) for t in fig_0.axes]
    [t.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ','))) for t in fig_1.axes]
    [t.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ','))) for t in fig_2.axes]
    [t.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ','))) for t in fig_3.axes]
    fig_0.axes[0].set_ylim(0,14000)
    fig_0.axes[1].set_ylim(0,100000)
    fig_0.axes[2].set_ylim(0,80000)
    fig_0.axes[3].set_ylim(0,25000)
    fig_0.axes[4].set_ylim(0,13000)
    fig_0.axes[5].set_ylim(0,80000)
    
    fig_1.axes[0].set_ylim(0,8000)
    fig_1.axes[1].set_ylim(0,10000)
    fig_1.axes[2].set_ylim(0,8000)
    fig_1.axes[3].set_ylim(0,3000)
    fig_1.axes[4].set_ylim(0,4000)
    fig_1.axes[5].set_ylim(0,15000)
    
    fig_2.axes[0].set_ylim(0,7000)
    fig_2.axes[1].set_ylim(0,15000)
    fig_2.axes[2].set_ylim(0,15000)
    fig_2.axes[3].set_ylim(0,6000)
    fig_2.axes[4].set_ylim(0,4000)
    fig_2.axes[5].set_ylim(0,8000)
    
    fig_3.axes[0].set_ylim(0,10000)
    fig_3.axes[1].set_ylim(0,12000)    
    fig_3.axes[2].set_ylim(0,12000)
    fig_3.axes[3].set_ylim(0,4000)
    fig_3.axes[4].set_ylim(0,5000)
    fig_3.axes[5].set_ylim(0,15000)
    
    
    
         
    
    
    fig_0.suptitle('Volume: eddyminto8k')    
    fig_1.suptitle('Volume: eddy8kto25k') 
    fig_2.suptitle('Area: eddyabove8k') 
    fig_3.suptitle('Volume: eddyabove8k') 
    fig_0.tight_layout()
    fig_0.subplots_adjust(top=0.92,right=0.90,wspace=0.71)
    fig_1.tight_layout()
    fig_1.subplots_adjust(top=0.92,right=0.90,wspace=0.71)
    fig_2.tight_layout()
    fig_2.subplots_adjust(top=0.92,right=0.90,wspace=0.71)
    fig_3.tight_layout()
    fig_3.subplots_adjust(top=0.92,right=0.90,wspace=0.71)
    fig_0.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddyminto8k_all_combined_style.png')
    fig_1.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddy8kto25k_all_combined_style.png')
    fig_2.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'area_eddyabove8k_all_combined_style.png')
    fig_3.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddyabove8k_all_combined_style.png')
    
    del n, group, group1, subset, fig_0, fig_1, fig_2, fig_3, name, axes
##########################################################################################################################################   
################################### Only Long Trips  ################################################################
#########################################################################################################################################
    data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
    data = pd.read_csv(data_file, sep =',')
    
    data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

    data = data[(data.Time_Series == 'long') & (data.SitePart == 'Eddy')] 
    #Preallocate Figures
    
    fig_0, ((ax_0,ax1_0),(ax2_0,ax3_0),(ax4_0,ax5_0)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_1, ((ax_1,ax1_1),(ax2_1,ax3_1),(ax4_1,ax5_1)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_2, ((ax_2,ax1_2),(ax2_2,ax3_2),(ax4_2,ax5_2)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_3, ((ax_3,ax1_3),(ax2_3,ax3_3),(ax4_3,ax5_3)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))

    
    axes = [[ax_0,ax_1,ax_2,ax_3],
            [ax1_0,ax1_1,ax1_2,ax1_3],
            [ax2_0,ax2_1,ax2_2,ax2_3],
            [ax3_0,ax3_1,ax3_2,ax3_3],
            [ax4_0,ax4_1,ax4_2,ax4_3],
            [ax5_0,ax5_1,ax5_2,ax5_3,]] 
    n=0
    for group1 in [g_1a,g_1b,g_1c,g_2,g_3,g_4][2:3]:
        
        ax_plot = axes[n]
        subset = data[data['Site'].isin(group1)]
        
        #Page 1 Volume less than 8
        for name, group in subset[subset['Plane_Height'] == 'eddyminto8k'].groupby('Site'):
            group.plot(x='TripDate',y='Volume',ax=ax_plot[0],label=name)
        # Shrink current axis by 20%
        box = ax_plot[0].get_position()
        ax_plot[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax_plot[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))    
        
        #page 2 FZ Volume
        for name, group in subset[subset['Plane_Height'] == 'eddy8kto25k'].groupby('Site'):
            group.plot(x='TripDate',y='Volume',ax=ax_plot[1],label=name)
        box = ax_plot[1].get_position()
        ax_plot[1].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax_plot[1].legend(loc='center left', bbox_to_anchor=(1, 0.5)) 
        
        
        subset = subset[subset.Plane_Height != 'eddyminto8k']     
        date_fz = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddy8kto25k') ].SurveyDate.unique()
        date_he = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddyabove25k') ].SurveyDate.unique()
        common_dates = np.intersect1d(date_fz,date_he)
        subset = subset[subset['SurveyDate'].isin(common_dates)]
        
        subset =  pd.pivot_table(subset,index=['Site','SurveyDate','SitePart','TripDate','SiteRange','Segment','Bar_type','Time_Series','Period'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()
        #page 3 Area above 8k
        for name, group in subset[subset['SitePart'] == 'Eddy'].groupby('Site'):
            group.plot(x='TripDate',y='Area_2D',ax=ax_plot[2],label=name)        
        ax_plot[2].legend(loc='center left', bbox_to_anchor=(1, 0.5)) 
        box = ax_plot[2].get_position()
        ax_plot[2].set_position([box.x0, box.y0, box.width * 0.8, box.height])        
        #page 4 volume above 8k
        for name, group in subset[subset['SitePart'] == 'Eddy'].groupby('Site'):
            group.plot(x='TripDate',y='Volume',ax=ax_plot[3],label=name) 
        box = ax_plot[3].get_position()
        ax_plot[3].set_position([box.x0, box.y0, box.width * 0.8, box.height])            
        ax_plot[3].legend(loc='center left', bbox_to_anchor=(1, 0.5)) 
        n+=1
    

    # Add group labels    
    [t.set_title('Group 1a') for t in axes[0]]
    [t.set_title('Group 1b') for t in axes[1]]
    [t.set_title('Group 1c') for t in axes[2]]
    [t.set_title('Group 2') for t in axes[3]]
    [t.set_title('Group 3') for t in axes[4]]
    [t.set_title('Group 4') for t in axes[5]]
    
    for i , ax in enumerate(fig_3.axes):
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
        ax.set_ylabel('VOLUME, IN CUBIC METERS')
    for i , ax in enumerate(fig_2.axes):
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
        ax.set_ylabel('AREA, IN METERS SQUARED')
    for i , ax in enumerate(fig_1.axes):
        ax.set_ylabel('VOLUME, IN CUBIC METERS')
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))        
    for i , ax in enumerate(fig_0.axes):
        ax.set_ylabel('VOLUME, IN CUBIC METERS')
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2010,01,01)) 
        
        
    fig_0.axes[0].set_ylim(0,14000)
    fig_0.axes[1].set_ylim(0,100000)
    fig_0.axes[2].set_ylim(0,80000)
    fig_0.axes[3].set_ylim(0,25000)
    fig_0.axes[4].set_ylim(0,13000)
    fig_0.axes[5].set_ylim(0,80000)
    
    fig_1.axes[0].set_ylim(0,8000)
    fig_1.axes[1].set_ylim(0,10000)
    fig_1.axes[2].set_ylim(0,8000)
    fig_1.axes[3].set_ylim(0,3000)
    fig_1.axes[4].set_ylim(0,4000)
    fig_1.axes[5].set_ylim(0,3000)
    
    fig_2.axes[0].set_ylim(0,7000)
    fig_2.axes[1].set_ylim(0,15000)
    fig_2.axes[2].set_ylim(0,15000)
    fig_2.axes[3].set_ylim(0,6000)
    fig_2.axes[4].set_ylim(0,4000)
    fig_2.axes[5].set_ylim(0,6000)
    
    fig_3.axes[0].set_ylim(0,10000)
    fig_3.axes[1].set_ylim(0,12000)    
    fig_3.axes[2].set_ylim(0,12000)
    fig_3.axes[3].set_ylim(0,4000)
    fig_3.axes[4].set_ylim(0,5000)
    fig_3.axes[5].set_ylim(0,4000)
        
    fig_0.suptitle('Volume: eddyminto8k')    
    fig_1.suptitle('Volume: eddy8kto25k') 
    fig_2.suptitle('Area: eddyabove8k') 
    fig_3.suptitle('Volume: eddyabove8k') 
    fig_0.tight_layout()
    fig_0.subplots_adjust(top=0.92,right=0.83,wspace=0.93)
    fig_1.tight_layout()
    fig_1.subplots_adjust(top=0.92,right=0.83,wspace=0.93)
    fig_2.tight_layout()
    fig_2.subplots_adjust(top=0.92,right=0.83,wspace=0.93)
    fig_3.tight_layout()
    fig_3.subplots_adjust(top=0.92,right=0.83,wspace=0.93)
    fig_0.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddyminto8k_long_combined.png')
    fig_1.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddy8kto25k_long_combined.png')
    fig_2.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'area_eddyabove8k_long_combined.png')
    fig_3.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddyabove8k_long_combined.png')
    
    del n, group, group1, subset, fig_0, fig_1, fig_2, fig_3, name, axes
##########################################################################################################################################   
################################### Only Long Trips with no zeros ################################################################
#########################################################################################################################################

    data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
    data = pd.read_csv(data_file, sep =',')
    
    data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

    data = data[(data.Time_Series == 'long') & (data.SitePart == 'Eddy')] 
    #Preallocate Figures
    
    fig_0, ((ax_0,ax1_0),(ax2_0,ax3_0),(ax4_0,ax5_0)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_1, ((ax_1,ax1_1),(ax2_1,ax3_1),(ax4_1,ax5_1)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_2, ((ax_2,ax1_2),(ax2_2,ax3_2),(ax4_2,ax5_2)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_3, ((ax_3,ax1_3),(ax2_3,ax3_3),(ax4_3,ax5_3)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))

    
    axes = [[ax_0,ax_1,ax_2,ax_3],
            [ax1_0,ax1_1,ax1_2,ax1_3],
            [ax2_0,ax2_1,ax2_2,ax2_3],
            [ax3_0,ax3_1,ax3_2,ax3_3],
            [ax4_0,ax4_1,ax4_2,ax4_3],
            [ax5_0,ax5_1,ax5_2,ax5_3,]] 
    n=0
    
    writer = pd.ExcelWriter(out_root + os.sep + "spagetti_plots" + os.sep +'eddyabv8kdata.xlsx',engine='xlsxwriter')
    r = ['g_1a','g_1b','g_1c','g_2','g_3','g_4']
    for group1 in [g_1a,g_1b,g_1c,g_2,g_3,g_4]:
        
        ax_plot = axes[n]
        subset = data[data['Site'].isin(group1)]
        
        #Page 1 Volume less than 8
        for name, group in subset[(subset['Plane_Height'] == 'eddyminto8k') & (data['Volume'] >0)].groupby('Site'):
            group.plot(x='TripDate',y='Volume',ax=ax_plot[0],label=name)
        # Shrink current axis by 20%
        box = ax_plot[0].get_position()
        ax_plot[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax_plot[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))    
        
        #page 2 FZ Volume
        for name, group in subset[(subset['Plane_Height'] == 'eddy8kto25k') & (data['Volume'] >0)].groupby('Site'):
            group.plot(x='TripDate',y='Volume',ax=ax_plot[1],label=name)
        box = ax_plot[1].get_position()
        ax_plot[1].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax_plot[1].legend(loc='center left', bbox_to_anchor=(1, 0.5)) 

        subset = subset[subset.Plane_Height != 'eddyminto8k']        
        date_fz = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddy8kto25k') ].SurveyDate.unique()
        date_he = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddyabove25k') ].SurveyDate.unique()
        common_dates = np.intersect1d(date_fz,date_he)
        subset = subset[subset['SurveyDate'].isin(common_dates)]

        subset =  pd.pivot_table(subset,index=['Site','SurveyDate','SitePart','TripDate','SiteRange','Segment','Bar_type','Time_Series','Period'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()
        subset.to_excel(writer,sheet_name = r[n])
        #page 3 Area above 8k
        for name, group in subset[subset['SitePart'] == 'Eddy'].groupby('Site'):
            group.plot(x='TripDate',y='Area_2D',ax=ax_plot[2],label=name)        
        ax_plot[2].legend(loc='center left', bbox_to_anchor=(1, 0.5)) 
        box = ax_plot[2].get_position()
        ax_plot[2].set_position([box.x0, box.y0, box.width * 0.8, box.height])        
        #page 4 volume above 8k
        for name, group in subset[subset['SitePart'] == 'Eddy'].groupby('Site'):
            group.plot(x='TripDate',y='Volume',ax=ax_plot[3],label=name) 
        box = ax_plot[3].get_position()
        ax_plot[3].set_position([box.x0, box.y0, box.width * 0.8, box.height])            
        ax_plot[3].legend(loc='center left', bbox_to_anchor=(1, 0.5)) 
        n+=1
    

    # Add group labels    
    [t.set_title('Group 1a') for t in axes[0]]
    [t.set_title('Group 1b') for t in axes[1]]
    [t.set_title('Group 1c') for t in axes[2]]
    [t.set_title('Group 2') for t in axes[3]]
    [t.set_title('Group 3') for t in axes[4]]
    [t.set_title('Group 4') for t in axes[5]]
    
    fig_3.axes[1].set_ylim(0,12000)
    fig_3.axes[0].set_ylim(0,10000)
    fig_3.axes[2].set_ylim(0,12000)
    fig_3.axes[3].set_ylim(0,4000)
    fig_3.axes[4].set_ylim(0,5000)
    fig_3.axes[5].set_ylim(0,4000)
    
    fig_2.axes[0].set_ylim(0,8000)
    fig_2.axes[1].set_ylim(0,12500)
    fig_2.axes[2].set_ylim(0,15000)
    fig_2.axes[3].set_ylim(0,6000)
    fig_2.axes[4].set_ylim(0,4000)
    fig_2.axes[5].set_ylim(0,5000)
    
    for i , ax in enumerate(fig_3.axes):
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
        ax.set_ylabel('VOLUME, IN CUBIC METERS')
    for i , ax in enumerate(fig_2.axes):
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
        ax.set_ylabel('AREA, IN METERS SQUARED')
    for i , ax in enumerate(fig_1.axes):
        ax.set_ylabel('VOLUME, IN CUBIC METERS')
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))        
    for i , ax in enumerate(fig_0.axes):
        ax.set_ylabel('VOLUME, IN CUBIC METERS')
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2010,01,01)) 
        
    fig_0.suptitle('Volume: eddyminto8k')    
    fig_1.suptitle('Volume: eddy8kto25k') 
    fig_2.suptitle('Area: eddyabove8k') 
    fig_3.suptitle('Volume: eddyabove8k') 
    fig_0.tight_layout()
    fig_0.subplots_adjust(top=0.92,right=0.83,wspace=0.93)
    fig_1.tight_layout()
    fig_1.subplots_adjust(top=0.92,right=0.83,wspace=0.93)
    fig_2.tight_layout()
    fig_2.subplots_adjust(top=0.92,right=0.83,wspace=0.93)
    fig_3.tight_layout()
    fig_3.subplots_adjust(top=0.92,right=0.83,wspace=0.93)
    fig_0.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddyminto8k_long_no_zeros_combined.png')
    fig_1.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddy8kto25k_long_no_zeros_combined.png')
    fig_2.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'area_eddyabove8k_long_no_zeros_combined.png')
    fig_3.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddyabove8k_long_no_zeros_combined.png')
    
    del n, group, group1, subset, fig_0, fig_1, fig_2, fig_3, name, axes, i , ax, date_fz, date_he, common_dates
    
    ##########################################################################################################################################   
################################### Only Long Trips with no zeros ################################################################
#########################################################################################################################################

    data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
    data = pd.read_csv(data_file, sep =',')
    
    data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

    data = data[(data.Time_Series == 'long') & (data.SitePart == 'Eddy')] 
    #Preallocate Figures
    
    fig_0, ((ax_0,ax1_0),(ax2_0,ax3_0),(ax4_0,ax5_0)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_1, ((ax_1,ax1_1),(ax2_1,ax3_1),(ax4_1,ax5_1)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_2, ((ax_2,ax1_2),(ax2_2,ax3_2),(ax4_2,ax5_2)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))
    fig_3, ((ax_3,ax1_3),(ax2_3,ax3_3),(ax4_3,ax5_3)) = plt.subplots(nrows=3,ncols=2,figsize=(7.5,9))

    
    axes = [[ax_0,ax_1,ax_2,ax_3],
            [ax1_0,ax1_1,ax1_2,ax1_3],
            [ax2_0,ax2_1,ax2_2,ax2_3],
            [ax3_0,ax3_1,ax3_2,ax3_3],
            [ax4_0,ax4_1,ax4_2,ax4_3],
            [ax5_0,ax5_1,ax5_2,ax5_3,]] 
    n=0
    for group1 in [g_1a,g_1b,g_1c,g_2,g_3,g_4]:
        
        ax_plot = axes[n]
        subset = data[data['Site'].isin(group1)]
        subset.loc[:,'Norm_Area']=subset.loc[:,'Area_2D']/subset.loc[:,'Max_Area']
        subset.loc[:,'Nrom_Volume']=subset.loc[:,'Volume']/subset.loc[:,'MaxVol']
        #Page 1 Volume less than 8
        for name, group in subset[(subset['Plane_Height'] == 'eddyminto8k') & (data['Volume'] >0)].groupby('Site'):
            group.plot(x='TripDate',y='Nrom_Volume',ax=ax_plot[0],label=name)
        # Shrink current axis by 20%
        box = ax_plot[0].get_position()
        ax_plot[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax_plot[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))    
        
        #page 2 FZ Volume
        for name, group in subset[(subset['Plane_Height'] == 'eddy8kto25k') & (data['Volume'] >0)].groupby('Site'):
            group.plot(x='TripDate',y='Nrom_Volume',ax=ax_plot[1],label=name)
        box = ax_plot[1].get_position()
        ax_plot[1].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax_plot[1].legend(loc='center left', bbox_to_anchor=(1, 0.5)) 
        
        subset = subset[subset.Plane_Height != 'eddyminto8k']
        date_fz = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddy8kto25k') ].SurveyDate.unique()
        date_he = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddyabove25k') ].SurveyDate.unique()
        common_dates = np.intersect1d(date_fz,date_he)
        subset = subset[subset['SurveyDate'].isin(common_dates)]
        subset =  pd.pivot_table(subset,index=['Site','SurveyDate','SitePart','TripDate','SiteRange','Segment','Bar_type','Time_Series','Period'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()
        subset.loc[:,'Norm_Area']=subset.loc[:,'Area_2D']/subset.loc[:,'Max_Area']
        subset.loc[:,'Nrom_Volume']=subset.loc[:,'Volume']/subset.loc[:,'MaxVol']        
        #page 3 Area above 8k
        for name, group in subset[subset['SitePart'] == 'Eddy'].groupby('Site'):
            group.plot(x='TripDate',y='Norm_Area',ax=ax_plot[2],label=name)        
        ax_plot[2].legend(loc='center left', bbox_to_anchor=(1, 0.5)) 
        box = ax_plot[2].get_position()
        ax_plot[2].set_position([box.x0, box.y0, box.width * 0.8, box.height])        
        #page 4 volume above 8k
        for name, group in subset[subset['SitePart'] == 'Eddy'].groupby('Site'):
            group.plot(x='TripDate',y='Nrom_Volume',ax=ax_plot[3],label=name) 
        box = ax_plot[3].get_position()
        ax_plot[3].set_position([box.x0, box.y0, box.width * 0.8, box.height])            
        ax_plot[3].legend(loc='center left', bbox_to_anchor=(1, 0.5)) 
        n+=1
    

    # Add group labels    
    [t.set_title('Group 1a') for t in axes[0]]
    [t.set_title('Group 1b') for t in axes[1]]
    [t.set_title('Group 1c') for t in axes[2]]
    [t.set_title('Group 2') for t in axes[3]]
    [t.set_title('Group 3') for t in axes[4]]
    [t.set_title('Group 4') for t in axes[5]]
    
    for i , ax in enumerate(fig_3.axes):
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
        ax.set_ylabel('NORMALIZED SANDBAR VOLUME')
    for i , ax in enumerate(fig_2.axes):
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
        ax.set_ylabel('NOMRALIZED SANDBAR AREA')
    for i , ax in enumerate(fig_1.axes):
        ax.set_ylabel('NORMALIZED SANDBAR VOLUME')
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))        
    for i , ax in enumerate(fig_0.axes):
        ax.set_ylabel('NORMALIZED SANDBAR VOLUME')
        ax.set_xlim(pd.datetime(1990,01,01), pd.datetime(2010,01,01)) 
        
    fig_0.suptitle('Volume: eddyminto8k')    
    fig_1.suptitle('Volume: eddy8kto25k') 
    fig_2.suptitle('Area: eddyabove8k') 
    fig_3.suptitle('Volume: eddyabove8k') 
    fig_0.tight_layout()
    fig_0.subplots_adjust(top=0.92,right=0.83,wspace=0.89)
    fig_1.tight_layout()
    fig_1.subplots_adjust(top=0.92,right=0.83,wspace=0.89)
    fig_2.tight_layout()
    fig_2.subplots_adjust(top=0.92,right=0.83,wspace=0.89)
    fig_3.tight_layout()
    fig_3.subplots_adjust(top=0.92,right=0.83,wspace=0.89)
    fig_0.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'Normvol_eddyminto8k_long_no_zeros_combined.png')
    fig_1.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'Normvol_eddy8kto25k_long_no_zeros_combined.png')
    fig_2.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'Normarea_eddyabove8k_long_no_zeros_combined.png')
    fig_3.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'Normvol_eddyabove8k_long_no_zeros_combined.png')
    
    del n, group, group1, subset, fig_0, fig_1, fig_2, fig_3, name, axes, i , ax, date_fz, date_he, common_dates
    
    
    ##########################################################################################################################################   
################################### Summation Plots Only Long Trips with no zeros ################################################################
#########################################################################################################################################

    data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
    data = pd.read_csv(data_file, sep =',')
    
    data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

    data = data[(data.Time_Series == 'long') & (data.SitePart == 'Eddy')] 
    #Preallocate Figures
    
    fig_0, ((ax_0,ax1_0),(ax2_0,ax3_0)) = plt.subplots(nrows=2,ncols=2,figsize=(7.5,9))

    n=0
    
    writer = pd.ExcelWriter(out_root + os.sep + "spagetti_plots" + os.sep +'eddyabv8kdata_cum.xlsx',engine='xlsxwriter')
    r = ['g_1a','g_1b','g_1c','g_2','g_3','g_4']
    for group1 in [g_1a,g_1b,g_1c,g_2,g_3,g_4]:
        
        subset = data[data['Site'].isin(group1)]
        
        tmp = pd.pivot_table(subset, index=['TripDate','Plane_Height'], values=['Volume','Area_2D'],aggfunc=np.sum).reset_index()
        
        name = r[n] + ': N=' + str(len(group1))
        tmp[(tmp['Plane_Height'] == 'eddyminto8k') & (tmp['Volume'] >0)].plot(x='TripDate',y='Volume',ax=fig_0.axes[0],label=name)
 
        
        tmp[(tmp['Plane_Height'] == 'eddy8kto25k') & (tmp['Volume'] >0)].plot(x='TripDate',y='Volume',ax=fig_0.axes[1],label=name)


        subset = subset[subset.Plane_Height != 'eddyminto8k']        
        date_fz = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddy8kto25k') ].SurveyDate.unique()
        date_he = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddyabove25k') ].SurveyDate.unique()
        common_dates = np.intersect1d(date_fz,date_he)
        subset = subset[subset['SurveyDate'].isin(common_dates)]

        subset =  pd.pivot_table(subset,index=['TripDate','SitePart'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()

        subset[subset['SitePart'] == 'Eddy'].plot(x='TripDate',y='Area_2D',ax=fig_0.axes[2],label=name)
        
     

        subset[subset['SitePart'] == 'Eddy'].plot(x='TripDate',y='Volume',ax=fig_0.axes[3],label=name)
        
      

        n+=1
    
    fig_0.axes[0].set_xlim(pd.datetime(1990,01,01), pd.datetime(2010,01,01))
    fig_0.axes[1].set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
    fig_0.axes[2].set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
    fig_0.axes[3].set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
    
    
    fig_0.axes[0].set_title('Volume: eddyminto8k')
    fig_0.axes[1].set_title('Volume: eddy8kto25k')
    fig_0.axes[2].set_title('Area: eddyabove8k')
    fig_0.axes[3].set_title('Volume: eddyabove8k')
    
    fig_0.axes[0].set_ylabel('VOLUME, IN CUBIC METERS')
    fig_0.axes[1].set_ylabel('VOLUME, IN CUBIC METERS')
    fig_0.axes[2].set_ylabel('AREA, IN METERS SQUARED')
    fig_0.axes[3].set_ylabel('VOLUME, IN CUBIC METERS')
    [i.legend_.remove() for i in fig_0.axes]
    [i.set_xlabel('Date') for i in fig_0.axes]
    fig_0.axes[0].set_ylim(0,180000)
    fig_0.axes[1].set_ylim(0,50000)
    fig_0.axes[2].set_ylim(0,50000)
    fig_0.axes[3].set_ylim(0,70000)

    fig_0.legend(handles = ax_0.get_legend_handles_labels()[0], labels=ax_0.get_legend_handles_labels()[1], loc = 'lower center', bbox_to_anchor = (0,0.05,1,1),
            bbox_transform = fig_0.transFigure,ncol=3)

    fig_0.tight_layout()
    fig_0.subplots_adjust(bottom=0.18)

    fig_0.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'Aggregrated_Group_metrics.png')

    
    del n, group, group1, subset, fig_0, fig_1, fig_2, fig_3, name, axes, i , ax, date_fz, date_he, common_dates
    

#########################################################################################################################################  
################################### Summation Plots Only Long Trips with no zeros #######################################################
#########################################################################################################################################

    data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
    data = pd.read_csv(data_file, sep =',')
    
    data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

    data = data[(data.Time_Series == 'long') & (data.SitePart == 'Eddy')] 
    #Preallocate Figures
    
    fig_0, ((ax_0,ax1_0),(ax2_0,ax3_0)) = plt.subplots(nrows=2,ncols=2,figsize=(7.5,9))

    n=0
    
    writer = pd.ExcelWriter(out_root + os.sep + "spagetti_plots" + os.sep +'eddyabv8kdata_cum.xlsx',engine='xlsxwriter')
    r = ['g_1a','g_1b','g_1c','g_2','g_3','g_4']
    for group1 in [g_1a,g_1b,g_1c,g_2,g_3,g_4]:
        
        subset = data[data['Site'].isin(group1)]
        
        tmp = pd.pivot_table(subset, index=['TripDate','Plane_Height'], values=['Volume','Area_2D','Errors'],aggfunc=np.sum).reset_index()
        
        name = r[n] + ': N=' + str(len(group1))
        tmp[(tmp['Plane_Height'] == 'eddyminto8k') & (tmp['Volume'] >0)].plot(x='TripDate',y='Volume',yerr='Errors', ax=fig_0.axes[0],label=name)
 
        
        tmp[(tmp['Plane_Height'] == 'eddy8kto25k') & (tmp['Volume'] >0)].plot(x='TripDate',y='Volume',yerr='Errors', ax=fig_0.axes[1],label=name)


        date_fz = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddy8kto25k') ].SurveyDate.unique()
        date_he = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddyabove25k') ].SurveyDate.unique()
        subset = subset[subset.Plane_Height != 'eddyminto8k']        
        common_dates = np.intersect1d(date_fz,date_he)
        subset = subset[subset['SurveyDate'].isin(common_dates)]

        subset =  pd.pivot_table(subset,index=['TripDate','SitePart'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()

        subset[subset['SitePart'] == 'Eddy'].plot(x='TripDate',y='Area_2D',ax=fig_0.axes[2],label=name)
        
     

        subset[subset['SitePart'] == 'Eddy'].plot(x='TripDate',y='Volume',yerr='Errors',ax=fig_0.axes[3],label=name)
        
      

        n+=1
    
    fig_0.axes[0].set_xlim(pd.datetime(1990,01,01), pd.datetime(2010,01,01))
    fig_0.axes[1].set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
    fig_0.axes[2].set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
    fig_0.axes[3].set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
    
    
    fig_0.axes[0].set_title('eddyminto8k')
    fig_0.axes[1].set_title('eddy8kto25k')
    fig_0.axes[2].set_title('eddyabove8k')
    fig_0.axes[3].set_title('eddyabove8k')
    
    fig_0.axes[0].set_ylabel('VOLUME, IN CUBIC METERS')
    fig_0.axes[1].set_ylabel('VOLUME, IN CUBIC METERS')
    fig_0.axes[2].set_ylabel('AREA, IN METERS SQUARED')
    fig_0.axes[3].set_ylabel('VOLUME, IN CUBIC METERS')
    [i.legend_.remove() for i in fig_0.axes]
    [i.set_xlabel('Date') for i in fig_0.axes]
    fig_0.axes[0].set_ylim(0,200000)
    fig_0.axes[1].set_ylim(0,50000)
    fig_0.axes[2].set_ylim(0,50000)
    fig_0.axes[3].set_ylim(0,70000)

    fig_0.legend(handles = ax_0.get_legend_handles_labels()[0], labels=ax_0.get_legend_handles_labels()[1], loc = 'lower center', bbox_to_anchor = (0,0.05,1,1),
            bbox_transform = fig_0.transFigure,ncol=3)

    fig_0.tight_layout()
    fig_0.subplots_adjust(bottom=0.18)

    fig_0.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'Aggregrated_Group_metrics_w_errors.png')

    
    del n, group1, subset, fig_0, name, i , date_fz, date_he, common_dates,ls,m,r,tmp
    

##########################################################################################################################################   
################################### Normalized Plots Only Long Trips with no zeros ################################################################
#########################################################################################################################################

    data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
    data = pd.read_csv(data_file, sep =',')
    
    data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

    data = data[(data.Time_Series == 'long') & (data.SitePart == 'Eddy')] 
    #Preallocate Figures
    
    fig_0, ((ax_0,ax1_0),(ax2_0,ax3_0)) = plt.subplots(nrows=2,ncols=2,figsize=(7.5,9))

    n=0
    
    writer = pd.ExcelWriter(out_root + os.sep + "spagetti_plots" + os.sep +'eddyabv8kdata_cum.xlsx',engine='xlsxwriter')
    r = ['g_1a','g_1b','g_1c','g_2','g_3','g_4']
    m = ['x','o','^','s','*','d']
    ls = ['-', '-','-','-','-','-',]#'--', '-.', ':','-', '--'
    for group1 in [g_1a,g_1b,g_1c,g_2,g_3,g_4]:
        
        
        subset = data[data['Site'].isin(group1)]
        subset.loc[:,'Norm_Area']=subset.loc[:,'Area_2D']/subset.loc[:,'Max_Area']
        subset.loc[:,'Norm_Vol'] = subset.loc[:,'Volume']/subset.loc[:,'MaxVol']
        tmp = pd.pivot_table(subset, index=['TripDate','Plane_Height'], values=['Norm_Vol','Area_2D'],aggfunc=np.average).reset_index()
        
        name = r[n] + ': N=' + str(len(group1))
        tmp[(tmp['Plane_Height'] == 'eddyminto8k') & (tmp['Norm_Vol'] >0)].plot(linestyle=ls[n],marker=m[n], x='TripDate',y='Norm_Vol', 
            yerr=std_err_calc(subset[(subset['Plane_Height'] == 'eddyminto8k') & (subset['Norm_Vol'] >0)],'Norm_Vol'), ax=fig_0.axes[0],label=name)
 
        
        tmp[(tmp['Plane_Height'] == 'eddy8kto25k') & (tmp['Norm_Vol'] >0)].plot(linestyle=ls[n],marker=m[n], x='TripDate',y='Norm_Vol',
            yerr=std_err_calc(subset[(subset['Plane_Height'] == 'eddy8kto25k') & (subset['Norm_Vol'] >0)],'Norm_Vol'), ax=fig_0.axes[1],label=name)


        subset = subset[subset.Plane_Height != 'eddyminto8k']        
        date_fz = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddy8kto25k') ].SurveyDate.unique()
        date_he = subset[(subset['Volume']>0) & (subset['Plane_Height'] == 'eddyabove25k') ].SurveyDate.unique()
        common_dates = np.intersect1d(date_fz,date_he)
        subset = subset[subset['SurveyDate'].isin(common_dates)]

        subset =  pd.pivot_table(subset,index=['TripDate','SitePart','Site'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()
        subset.loc[:,'Norm_Area']=subset.loc[:,'Area_2D']/subset.loc[:,'Max_Area']
        subset.loc[:,'Norm_Vol'] = subset.loc[:,'Volume']/subset.loc[:,'MaxVol']
        tmp = pd.pivot_table(subset, index=['TripDate','SitePart'], values=['Norm_Vol','Norm_Area'],aggfunc=np.average).reset_index()
        
        tmp[tmp['SitePart'] == 'Eddy'].plot(linestyle=ls[n],marker=m[n], x='TripDate',y='Norm_Area',
           yerr=std_err_calc(subset,'Norm_Area'),ax=fig_0.axes[2],label=name)
        
     

        tmp[tmp['SitePart'] == 'Eddy'].plot(linestyle=ls[n],marker=m[n], x='TripDate',y='Norm_Vol',
            yerr=std_err_calc(subset,'Norm_Vol'), ax=fig_0.axes[3],label=name)
        
      

        n+=1
    
    fig_0.axes[0].set_xlim(pd.datetime(1992,01,01), pd.datetime(2010,01,01))
    fig_0.axes[1].set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
    fig_0.axes[2].set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
    fig_0.axes[3].set_xlim(pd.datetime(1990,01,01), pd.datetime(2018,01,01))
    
    
    fig_0.axes[0].set_title('eddyminto8k')
    fig_0.axes[1].set_title('eddy8kto25k')
    fig_0.axes[2].set_title('eddyabove8k')
    fig_0.axes[3].set_title('eddyabove8k')
#    
    fig_0.axes[0].set_ylabel('NORMALIZED VOLUME')
    fig_0.axes[1].set_ylabel('NORMALIZED VOLUME')
    fig_0.axes[2].set_ylabel('NORMALIZED AREA')
    fig_0.axes[3].set_ylabel('NORMALIZED VOLUME')
    [i.legend_.remove() for i in fig_0.axes]
    [i.set_xlabel('Date') for i in fig_0.axes]
    fig_0.axes[0].set_ylim(0,0.8)
    fig_0.axes[1].set_ylim(0,0.8)
    fig_0.axes[2].set_ylim(0,0.5)
    fig_0.axes[3].set_ylim(0,0.8)

    fig_0.legend(handles = ax_0.get_legend_handles_labels()[0], labels=ax_0.get_legend_handles_labels()[1], loc = 'lower center', bbox_to_anchor = (0,0.05,1,1),
            bbox_transform = fig_0.transFigure,ncol=3)

    fig_0.tight_layout()
    fig_0.subplots_adjust(bottom=0.18)

    fig_0.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'Normalized_Group_metrics_with_Errors.png')

    
    del n, group1, subset, fig_0, name, i , date_fz, date_he, common_dates,ls,m,r,tmp
    