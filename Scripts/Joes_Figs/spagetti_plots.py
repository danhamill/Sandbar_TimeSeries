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
from scipy.stats import linregress

if __name__ =='__main__':
    
    if platform.system() == 'Darwin':
        sandbar_root = '/Users/danielhamill/git_clones/sandbar_process'
        time_root = '/Users/danielhamill/git_clones/Time_Series'
        out_root = time_root + os.sep + 'Output/Joes_figs'
    elif platform.system() == 'Windows':
        sandbar_root = r'C:\workspace\sandbar_process'
        time_root = r'C:\workspace\Time_Series'
        out_root = time_root + os.sep + r'Output\Joes_figs'

    #Read Data from file
    data_file = sandbar_root + os.sep + 'Merged_Sandbar_data.csv'
    data = pd.read_csv(data_file, sep =',')
    
    data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')
    
    #designate groups       
    g_1a = np.array(['145l','022r','213l','084r','030r','081l','137l','119r','122r'])
    g_1b = np.array(['009l','123l','172l','044l_r','045l_r','044l_r','183r','220r','050r_r','065r','047r'])
    g_1c = np.array(['070r','194l','068r','051l','055r'])
    g_2 = np.array(['008l','024l','029l','032r','056r','167l'])
    g_3 = np.array(['044lr_s','087l','093l','139r','225r','104r'])
    g_4 = np.array(['016l','033l','035l_s','062r','091r','202r_s'])
    
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
        
    [t.set_title('Group 1a') for t in axes[0]]
    [t.set_title('Group 1b') for t in axes[1]]
    [t.set_title('Group 1c') for t in axes[2]]
    [t.set_title('Group 2') for t in axes[3]]
    [t.set_title('Group 3') for t in axes[4]]
    [t.set_title('Group 4') for t in axes[5]]
    fig_0.suptitle('Volume: eddyminto8k')    
    fig_1.suptitle('Volume: eddy8kto25k') 
    fig_2.suptitle('Area: eddyabove8k') 
    fig_3.suptitle('Volume: eddyabove8k') 
    fig_0.tight_layout()
    fig_0.subplots_adjust(top=0.92,right=0.83,wspace=0.73)
    fig_1.tight_layout()
    fig_1.subplots_adjust(top=0.92,right=0.83,wspace=0.73)
    fig_2.tight_layout()
    fig_2.subplots_adjust(top=0.92,right=0.83,wspace=0.73)
    fig_3.tight_layout()
    fig_3.subplots_adjust(top=0.92,right=0.83,wspace=0.73)
    fig_0.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddyminto8k.png')
    fig_1.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddy8kto25k.png')
    fig_2.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'area_eddyabove8k.png')
    fig_3.savefig(out_root + os.sep + 'spagetti_plots' + os.sep + 'vol_eddyabove8k.png')
    
    
    data = data[(data.Time_Series == 'long') & (data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k')]
    
    #subset to two bar sites
    data = data[data.Site.str.len()>4]
    
    #Get Rid of zeros
    data = data[data['Area_2D']>0]
    
    data = pd.pivot_table(data,index=['Site','SurveyDate','SitePart','TripDate','SiteRange','Segment','Bar_type','Time_Series','Period'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()
    
    
    #Group by bar type
    grouped = data.groupby('Bar_type')
    reatt = grouped.get_group('Reattachment')
    sep = grouped.get_group('Separation')
    
    for r_site, s_site in zip(reatt.Site.unique(),sep.Site.unique()):
        r_subset = reatt[reatt['Site'] == r_site]
        s_subset = sep[sep['Site'] == s_site]
    
        #find dates where both high elevation and fluctuating zone
        common_dates = np.intersect1d(r_subset.SurveyDate.unique(),s_subset.SurveyDate.unique())
        r_subset = r_subset[r_subset['SurveyDate'].isin(common_dates)]
        s_subset = s_subset[s_subset['SurveyDate'].isin(common_dates)]
        
        fig, (ax) = plt.subplots(figsize=(7.5,2.5))
        s,i,r,p,stderr = linregress(s_subset['Volume'], s_subset['Area_2D'])
        s_subset.plot(kind='scatter', x='Volume',y='Area_2D',ax=ax,label='Separation',c='k')
        ax.plot(s_subset['Volume'], i +s*s_subset['Volume'],'k')
        #ax.set_ylim(3000,7000)    
#        ax.text(1125,5000,'R$_{sep}$$^2$=%1.4f' % r )
#        ax.text(1125,4500,'m$_{sep}$=%1.4f' % s )
        
        s,i,r,p,stderr = linregress(r_subset['Volume'], r_subset['Area_2D'])
        r_subset.plot(kind='scatter', x='Volume',y='Area_2D',ax=ax,label='Reattachment',marker='x',c='green')
        ax.plot(r_subset['Volume'], i +s*r_subset['Volume'],'green',ls=':')
        ax.set_title(r_site[0:-2])
#        ax.text(7250,4000,'R$_{reatt}$$^2$=%1.4f' % r )
#        ax.text(7250,3519,'m$_{sep}$=%1.4f' % s )
        ax.set_autoscale_on(False)
        ax.set_xlabel('Volume m$^3$')
        ax.set_ylabel('Area m$^2$')
        plt.tight_layout()
        plt.savefig(out_root + os.sep +'two_bar_sites_analysis' + os.sep + r_site[0:-2] +'_area_vol.png')
        
#    sep = data[(data.Time_Series == 'long') & (data.Site =='044l_s') & (data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k')]
#    reatt = data[(data.Time_Series == 'long') & (data.Site =='044l_r') & (data.SitePart == 'Eddy') & (data.Plane_Height != 'eddyminto8k')]
#    sep = pd.pivot_table(sep,index=['Site','SurveyDate','SitePart','TripDate','SiteRange','Segment','Bar_type','Time_Series','Period'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()
#    reatt =pd.pivot_table(reatt,index=['Site','SurveyDate','SitePart','TripDate','SiteRange','Segment','Bar_type','Time_Series','Period'],values=['Area_2D','Area_3D','Volume','Errors','MaxVol','Max_Area'],aggfunc=np.sum).reset_index()
#    reatt = reatt[reatt['Volume']>0] 
#    
#    fig, (ax,ax1) = plt.subplots(nrows=2,figsize=(7.5,5))
#    s,i,r,p,stderr = linregress(sep['Volume'], sep['Area_2D'])
#    sep.plot(kind='scatter', x='Volume',y='Area_2D',ax=ax,label='Separation')
#    ax.plot(sep['Volume'], i +s*sep['Volume'],'k')
#    ax.set_ylim(3600,4600)    
#    ax.text(1125,4200,'R$_{sep}$$^2$=%1.4f' % r )
#    ax.text(1125,4100,'m$_{sep}$=%1.4f' % s )
#    s,i,r,p,stderr = linregress(reatt['Volume'], reatt['Area_2D'])
#    
#    reatt.plot(kind='scatter', x='Volume',y='Area_2D',ax=ax1,label='Reattachment')
#    
#    ax1.plot(reatt['Volume'], i +s*reatt['Volume'],'k')
#    ax.set_title('044L')
#    ax1.text(7250,4000,'R$_{reatt}$$^2$=%1.4f' % r )
#    ax1.text(7250,3519,'m$_{sep}$=%1.4f' % s )
#    ax.set_autoscale_on(False)
#    ax1.set_autoscale_on(False)
#
#    plt.tight_layout()
#    
#    
#    #one plot
#    fig, (ax) = plt.subplots(figsize=(7.5,2.5))
#    s,i,r,p,stderr = linregress(sep['Volume'], sep['Area_2D'])
#    sep.plot(kind='scatter', x='Volume',y='Area_2D',ax=ax,label='Separation',c='k')
#    ax.plot(sep['Volume'], i +s*sep['Volume'],'k')
#    ax.set_ylim(3000,7000)    
#    ax.text(1125,5000,'R$_{sep}$$^2$=%1.4f' % r )
#    ax.text(1125,4500,'m$_{sep}$=%1.4f' % s )
#    s,i,r,p,stderr = linregress(reatt['Volume'], reatt['Area_2D'])
#    
#    reatt.plot(kind='scatter', x='Volume',y='Area_2D',ax=ax,label='Reattachment',marker='x',c='green')
#    
#    ax.plot(reatt['Volume'], i +s*reatt['Volume'],'green',ls=':')
#    ax.set_title('044L')
#    ax.text(7250,4000,'R$_{reatt}$$^2$=%1.4f' % r )
#    ax.text(7250,3519,'m$_{sep}$=%1.4f' % s )
#    ax.set_autoscale_on(False)
#    ax.set_xlabel('Volume m$^3$')
#    ax.set_ylabel('Area m$^2$')
#    plt.tight_layout()
#    plt.savefig(out_root + os.sep + '44l_area_vs_vol_1plot.png')
#    
    
    