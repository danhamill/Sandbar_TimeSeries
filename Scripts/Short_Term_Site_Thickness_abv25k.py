# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


#Read Database from file
data = pd.read_csv(r'C:\workspace\Time_Series\Merged_Sandbar_data.csv', sep =',')

#Set Trip dates to pandas datetime
data['TripDate'] = pd.to_datetime(data['TripDate'], format='%Y-%m-%d')

#Query to select 'long' time series and 'long trips\
query1 = data[data.SiteRange=='short']                      #time series Length
query1 = query1[query1.SitePart=='Eddy']                    #Channel or eddy
query1 = query1[query1.Plane_Height == 'eddyabove25k']       #Elevation bins
query1 = query1[query1['TripDate']>'2002-01-01']            #Drop all surveys before they were officially monitored

#Pivot and calculate thickness
table1 = pd.pivot_table(query1, values=['Volume','Area_2D'], index=['Site','TripDate'], aggfunc=np.sum)
table1['Thickness'] = table1.Volume/table1.Area_2D
table1 = table1.fillna(value=0)

#Subset master table for easier plotting
table1= table1.reset_index()
sub1 = table1[['Site','TripDate','Thickness']]
sub1= sub1.set_index(['Site','TripDate'])

#Count number of sites
n=0
for Site , new_df in sub1.groupby(level=0):
    n += 1
    
#create a list to interate through the number of sites
list1 = xrange(n)

#Unstack sites for plotting
t=sub1.unstack(level=0)

#counter for sites in t
plot_counter = 0
site_counter =0
with PdfPages(r'C:\workspace\Time_Series\Output\Short_Term_Site_Thickness_abv25k.pdf') as pdf:
    print 'pdf open'
    for i in list1:
        if site_counter == 0:                                   #This is the first run       
            print 'Making first plot'
            fig,axes = plt.subplots(figsize=(7,10.25),nrows=3)
            t[[site_counter]].dropna(axis=0).plot(ax=axes[plot_counter],rot=45,x_compat=True, marker='o')
            plot_counter += 1       
            print 'Plot counter is at %s' %(plot_counter,)               
        else:
            if plot_counter == 0:               #This is the first plot on a page
                fig,axes = plt.subplots(figsize=(7,10.25),nrows=3)
                t[[site_counter]].dropna(axis=0).plot(ax=axes[plot_counter],rot=45,x_compat=True, marker='o')
                print 'Plot counter is at %s at the first plot on page' %(plot_counter,)                
                plot_counter += 1    
            else:                               #Either this is the last plot on the page or the second plot on a page
                if plot_counter % 3 == 0:
                    print 'plot counter is at %s on the last plot on a page' %(plot_counter,)
                    t[[site_counter]].dropna(axis=0).plot(ax=axes[plot_counter-1],rot=45,x_compat=True, marker='o')
                    for ax in axes:
                        ax.set_xlabel('Trip Date')
                        ax.set_ylabel('Thickness [m]')
                    plt.suptitle('')
                    pdf.savefig()                                   # saves the current figure into a pdf page
                    plt.close()
                    plot_counter = 0
                    print 'Saved page'
                else:                                               #Keep on plotting                  
                    print 'Plot counter is at %s at the second plot' %(plot_counter,)
                    t[[site_counter]].dropna(axis=0).plot(ax=axes[plot_counter],rot=45,x_compat=True, marker='o')
                    plot_counter += 2
        site_counter += 1         
del pdf 
                    