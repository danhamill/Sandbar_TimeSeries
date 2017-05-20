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
files = glob(r"C:\workspace\survey_stage\shp\*.shp")



ind_new = [18,20,28,34,37,38,45,50,73,74]
area_new = []

ind_lt = [6,7,14,17,24,27,41,46,54,63,64,67]
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

from scipy.stats import probplot

fig,(ax,ax1) = plt.subplots(figsize=(7.5,5),ncols=2,sharey=True)
a = probplot(area_old,dist='norm', plot=ax)
b= probplot(combined,dist='norm', plot=ax1)
ax.set_title('LONG TERM SITES N=12')
ax1.set_title('ALL SITES N=22')
ax1.set_ylabel('')
ax.set_ylabel('TOTAL EDDY AREA, IN METERS SQUARED')
ax.set_ylim(0,35000)
ax.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',')))

ax.text(-1.5,31000,'R$^2$ = 0.83')
ax1.text(-1.5,31000,'R$^2$ = 0.90')

ax.set_xlabel('QUANTILES')
ax1.set_xlabel('QUANTILES')
plt.tight_layout()
plt.savefig(r"C:\workspace\Time_Series\Output\Joes_Figs\mc_area_qqplot.png",dpi=600)
