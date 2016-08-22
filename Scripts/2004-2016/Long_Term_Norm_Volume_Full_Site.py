# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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

#Query to select 'long' time series and 'long trips\
query1 = data[data.SiteRange=='long']                   #time series Length
query1 = query1[query1.SitePart=='Eddy']                #Channel or eddy
query1 = query1[query1.Plane_Height != 'eddyminto8k']
query1 = query1[query1['TripDate'] >= '2004-01-01']       #Elevation bins



#Determine Volume and max_volume sum
table1 = pd.pivot_table(query1, values=['Volume'], index=['Site','TripDate'], aggfunc=np.sum)
table2 = pd.pivot_table(query1, values=['MaxVol'], index=['Site','TripDate'], aggfunc=np.sum)

#Determine what the earliest survey was for each site
table3 = pd.pivot_table(query1,values=['TripDate'], index=['Site'], aggfunc=np.min)

#Associate Early_Vol with early dates
table3 = pd.merge(table3.reset_index(),table1.reset_index(),on=['Site','TripDate'],how='left')
table3 = table3.rename(columns = {'Volume':'Early_Vol'})

#Merge the Volume and max volume pivot tables
merge1 = table1.merge(table2,left_index=True,right_index=True,how='left')

#Merge the Early_vol to the merged volume table
merge2 = pd.merge(merge1.reset_index(),table3.reset_index(),on=['Site'],how='left')

#Reformat tables to look nice
merge2 = merge2.drop(merge2.columns[[-2]], axis=1)
merge2 = merge2.drop(merge2.columns[[-2]], axis=1)
merge2 = merge2.rename(columns = {'TripDate_x':'TripDate'})

#Normalize the Volumes
merge2['Norm_vol'] = merge2.Volume/merge2.MaxVol

#Calculate percent Volume
merge2['Percent_Vol']=(merge2.Volume-merge2.Early_Vol)/merge2.Early_Vol
merge2 = merge2.set_index(['Site','TripDate'])


#Subset master table for easier plotting
merge2= merge2.reset_index()
sub1 = merge2[['Site','TripDate','Norm_vol']]
sub1= sub1.set_index(['Site','TripDate'])

#Count number of sites
n=0
for Site , new_df in sub1.groupby(level=0):
    n += 1
    
#create a list to interate through the number of sites
list1 = xrange(n)

#Unstack sites for plotting
t=sub1.unstack(level=0)
t.columns = t.columns.droplevel()

#counter for sites in t
plot_counter = 0
site_counter =0
with PdfPages(r'C:\workspace\Time_Series\Output\Long_Term_Site_norm_vol_2004.pdf') as pdf:
    print 'pdf open'
    for i in list1:
        if site_counter == 0:                                   #This is the first run       
            print 'Making first plot'
            fig,axes = plt.subplots(figsize=(7,10.25), nrows=3, sharex=True)
            t[[site_counter]].dropna(axis=0).plot(ax=axes[plot_counter],rot=45,x_compat=True, marker='o', fontsize=8)
            plot_counter += 1       
            print 'Plot counter is at %s' %(plot_counter,)               
        else:
            if plot_counter == 0:               #This is the first plot on a page
                fig,axes = plt.subplots(figsize=(7,10.25),nrows=3, sharex=True)
                t[[site_counter]].dropna(axis=0).plot(ax=axes[plot_counter],rot=45,x_compat=True, marker='o', fontsize=8)
                print 'Plot counter is at %s at the first plot on page' %(plot_counter,)                
                plot_counter += 1    
            else:                               #Either this is the last plot on the page or the second plot on a page
                if plot_counter % 3 == 0:
                    print 'plot counter is at %s on the last plot on a page' %(plot_counter,)
                    t[[site_counter]].dropna(axis=0).plot(ax=axes[plot_counter-1],rot=45,x_compat=True, marker='o', fontsize=8)
                    for ax in axes:
                        ax.set_xlabel('Trip Date')
                        ax.set_ylabel('Normalized Volume')
                    pdf.savefig()                                   # saves the current figure into a pdf page
                    plt.close()
                    plot_counter = 0
                    print 'Saved page'
                else:                                               #Keep on plotting                  
                    print 'Plot counter is at %s at the second plot' %(plot_counter,)
                    t[[site_counter]].dropna(axis=0).plot(ax=axes[plot_counter],rot=45,x_compat=True, marker='o', fontsize=8)
                    plot_counter += 2
        site_counter += 1         
del pdf 
                    