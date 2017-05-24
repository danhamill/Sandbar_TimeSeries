# -*- coding: utf-8 -*-
"""
Created on Thu May 18 14:49:57 2017

@author: dan
"""

from osgeo import ogr
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from scipy.stats import probplot
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import FormatStrFormatter


files = glob(r"C:\workspace\survey_stage\shp\*.shp")



ind_new = [18,20,28,34,37,38,45,50,73,74]
new_bt = ['u','u','r','s','r','s','r','r','r','u']
area_new = []

ind_lt = [6,7,14,17,24,27,41,46,54,63,64,67]
lt_bt = ['r','s','s','r','r','u','r','s','r','r','s','r']
area_old = []

for ind in ind_new:
    shp = files[ind]
    ds = ogr.Open(shp)
    layer = ds.GetLayer()
    for feat in layer:
        geom = feat.GetGeometryRef()
        area_new.append(geom.GetArea())
    del ds
        
for ind in ind_lt:
    shp = files[ind]
    ds = ogr.Open(shp)
    layer = ds.GetLayer()
    for feat in layer:
        geom = feat.GetGeometryRef()
        area_old.append(geom.GetArea())
    del ds
    
print'new ', np.max(area_new)
print 'old ', np.max(area_old)

combined = area_old + area_new
pd.DataFrame(area_new).describe()

df = pd.DataFrame(combined).merge(pd.DataFrame(area_old),how='left',left_index=True, right_index=True)
df = df.rename(columns={'0_x':'All Sites N=22','0_y':'Long Term Sites: N=12'})
df = df.merge(pd.DataFrame(area_new,columns=['Additional Sites N=10']), how='left',left_index=True, right_index=True)
fig, ax = plt.subplots(figsize=(7.5,5))

df.plot.box(ax=ax)
ax.set_ylabel('TOTAL EDDY AREA, IN METERS SQUARED')
ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.tight_layout()
plt.savefig(r"C:\workspace\Time_Series\Output\Joes_Figs\mc_area_boxplot.png",dpi=600)

from scipy.stats.mstats import normaltest, skewtest

print 'old ', normaltest(area_old)
print 'combined ', normaltest(combined)

print 'old ', skewtest(area_old)
print 'combined ', skewtest(combined)

a = probplot(area_old,dist='norm', plot=None)
b= probplot(combined,dist='norm', plot=None)
colors = {'r':'red','s':'blue', 'u':'green'}
markers = {'r':'*','s':'x', 'u':'o'}

old_df = pd.DataFrame(area_old, columns=['Long Term Sites: N=12'])
old_df['Bar_Type'] = lt_bt
old_df = old_df.sort_values(by='Long Term Sites: N=12')
old_df['quart']=a[0][0]

combined_df = pd.DataFrame(combined, columns=['ALL SITES N=22'])
combined_df['Bar_Type'] = lt_bt + new_bt
combined_df = combined_df.sort_values(by='ALL SITES N=22')
combined_df['quart']=b[0][0]


undif = plt.Line2D([0,0],[0,1], color='green',marker='o',linestyle=' ')
reatt = plt.Line2D([0,0],[0,1], color='red',marker='*',linestyle=' ')
sep = plt.Line2D([0,0],[0,1], color='blue',marker='x',linestyle=' ')

fontP = FontProperties()
fontP.set_size('x-small')

fig,(ax,ax1) = plt.subplots(figsize=(7.5,5),ncols=2,sharey=True)

#Plot each data point seperatly with different markers and colors
for i, thing in old_df.iterrows():
    ax.scatter(thing['quart'],thing['Long Term Sites: N=12'],c=colors[thing['Bar_Type']],marker=markers[thing['Bar_Type']],zorder=10,s=50)
del i, thing

for i , thing in combined_df.iterrows():
    ax1.scatter(thing['quart'],thing['ALL SITES N=22'],c=colors[thing['Bar_Type']],marker=markers[thing['Bar_Type']],zorder=10,s=50)
del i, thing

#Plot trend line
ax.plot(a[0][0],a[0][1],"w",a[0][0],a[0][0]*a[1][0] + a[1][1],'black')
ax.text(0.4,4600,"$R^2=%1.4f$" % a[1][-1] )
ax1.plot(b[0][0],b[0][1],"w",b[0][0],b[0][0]*b[1][0] + b[1][1],'black')
ax1.text(0.70,4600,"$R^2=%1.4f$" % b[1][-1] )


ax.set_title('LONG TERM SITES N=12')
ax1.set_title('ALL SITES N=22')
ax1.set_ylabel('')
ax.set_ylabel('TOTAL EDDY AREA, IN METERS SQUARED')
ax.set_ylim(0,35000)
ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))

legend = ax.legend([reatt,sep,undif],["Reattachment: N=7","Separation: N=6", "Undifferentiated: N=1"],loc=2,title='Bar Type',prop=fontP)
legend2 = ax1.legend([reatt,sep,undif],["Reattachment: N=12","Separation: N=8", "Undifferentiated: N=4"],loc=2,title='Bar Type',prop=fontP)

plt.setp(legend.get_title(),fontsize='x-small')
plt.setp(legend2.get_title(),fontsize='x-small')
ax.set_xlabel('QUANTILES')
ax1.set_xlabel('QUANTILES')
ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
plt.tight_layout()
plt.savefig(r"C:\workspace\Time_Series\Output\Joes_Figs\mc_area_probability_plot.png",dpi=600)



