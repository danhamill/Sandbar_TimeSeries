# Marble Canyon Sample Size Analysis

## Problem Statement
Since 1990 NAU and USGS have been monitoring sandbars in Marble to determine how Glen Canyon Dam operations affect the size and volumes of exposed sand.  Initially, 12 long-term monitoring sites (Table 1) were estabilished as representative sample of the sandbars within Marble CAnyon.  The selected montoring sites were spaitally distributed throughout Marble Canyon and were surveyed using total stations at irregular time intervals to determine sand volumes.  In 2002, an addtional 11 sandbars were selected for long-term monitoring (Table 1) in efforts to obtain a sample that is more resprenative of Marble Canyon.  These sites were choosen using expert judgement and typically contained large volumes of sand.  Finally in 2008, an additional 4 sites (Table 1) were selected for long-term monitoring.  The effects of increasing sample size on long-term trends of sandbar volumes is largely unknown and will be anayzed throghout this vignette.  The data used in this anasis were collected between 11/2003 and 1/2016.

### Table 1: Marble Canyon Monitoring sites
| Sites Added in 1990 |Sites Added in 2002|Sites added in 2008|
|------| -----|----|
|003l  | 024l |009l|
|008l  | 029l |045_s|
|016l  | 033l |
|022r  | 035_s |
|030r  | 041l_s |
|032r  |041l_r |
|043l  | 044l_r |
|044l_s| 045l_s |
|047r  | 045l_r |
|050r_r| 055r |
|050r_s| 056_r |
|051l  |

## Methods
To determine the effects of increasing sample size, the trends associated with the long-term moniroting sites establised in 1990 will be compared to the trends associated with larger sample sizes.  A simple first cut analysis is to compare the trends associated with the sites established in 1990 (hereafter termed 'refernce series') against the trends of all of the moniroing sites (n=25)(Figure 1) for all elevations above 8k.
### Figure 1
![fig1][fig1]

Normalized Volumes and errors were calculated using Equation 1 and Equation 2, respectively.

### Equation 1

![eq1][eq1]

### Equation 2
![eq2][eq2]

Where:
- n = Site
- x = Trip Date

This approach to calculating normailzed volumes and normlized errors relies on several assumptions.  First, this approach relies on the fact that normalized metrics allow for the direct comparison of sites with different storage capacites and aerial extents.  Since the volumes measured at a paritlcar instance of time are realitve to the maximum volume ever surveyed over the either monitoing period, realtive chagnes in sandbar volumes at individual sites are preserved durig aggregration.  Second, reporting normalized errors as a function of area measured and the areas aassociated with the maximum surface at each site allows for uncertainites assocated with volume measurements to be preserved when mutiple sites are aggregrated.  These assumptions allow for normalized volumes and normalized errors to have similar units and occupy the same domain (e.g. [0-1]).  A major advantage of this approach is it reults in reporting raw data and each can be physically explained in terms of measured volumes and areas.

An alternative approach to aggregrating monitorig sites for time sereis analysis is to rely summary statistics (e.g. averages, medians, etc.). For each trip, this process would involve calculting the noramized volume at individual sites and reporting an summary statistic of the set of normlized volumes.  Summary statistics result in a metric that begins to loose its physical meaning (in temrs of measured volume and areas) and limit the ways uncertainites can be reported.  Any error bar attached to a summary statitic would have to rely on higher order statistics (e.g. standard deviation, standard error) and would have less of a physical explination than the summary statistic it attempts to describe.  Standard deviation describes how normalized volumes for a particular samople (i.e. survey trip) vary about the mean value of that sample, while standard error further complicates the explination by normilizing standard deviation by the sample size.

The effects of varying sample sizes were analyzed by comparing the trends assoicated with the referene sereis to a subset of all of the monitorin sites in Marble Canyon. The subset of sites (hereafter temred 'subset sereis') was aquired by removing one of the sites added after 2002 and comparing to the trends associated with the reference series.  Table 2 summarzes the percent change assocaited between the normalized volume calcultions betwen the subset series and reference series.

### Table 2
Site | Percent Change
------|---------:
009l  |   0.08215
024l  |   0.07867
029l  |   0.08141
033l  |   0.08085
035l_r|   0.08639
035l_s|   0.07981
041r_r|   0.06155
041r_s|   0.07195
044l_r|   0.06799
045l_r|   0.09351
045l_s|   0.08178
055r  |   0.03056
056r  |   0.07710

To determine the effect of individal sites on particular survey trips, percent change between the subset sereis and reference series are reported in Table 3.  Columns represent site removed from the subset sereis.
### Table 3
TripDate      |  009l   |  024l   |  029l   |  033l   |035l_r | 035l_s  | 041r_r  | 041r_s  | 044l_r  | 045l_r | 045l_s |  055r  |  056r|
--------------------|--------:|--------:|--------:|--------:|------:|--------:|--------:|--------:|--------:|-------:|-------:|-------:|--------:|
2004-12-02 |  0.08053|  0.08027|  0.07878|  0.07964|0.07744|  0.07977|  0.08160|  0.08235|  0.09138| 0.06029| 0.08284| 0.04112|  0.07904|
2005-05-07 |  0.00168|  0.00934| -0.00079|  0.00167|0.01726| -0.00217|  0.03470|  0.00086| -0.03018| 0.00103| 0.01678|-0.02983| -0.00377|
2006-10-07 | -0.00402|  0.00341|  0.00534| -0.00557|0.01166| -0.00220| -0.00016| -0.01204| -0.02437| 0.02596| 0.01117|-0.07786|  0.00679|
2007-10-13|  0.01424|  0.01834|  0.02625|  0.01457|0.02301|  0.01634|  0.02033|  0.00885| -0.00707| 0.04667| 0.02915|-0.07152|  0.02448|
2008-02-02 |  0.02444|  0.02349|  0.02453|  0.02337|0.03167|  0.02302|  0.03060|  0.02171|  0.00929| 0.03668| 0.02105|-0.02273|  0.02456|
2008-03-28 |  0.04633|  0.04877|  0.04697|  0.04873|0.04272|  0.04854|  0.04542|  0.04910|  0.05569| 0.04798| 0.05018| 0.02188|  0.04875|
2008-10-10 |  0.23134|  0.22385|  0.21918|  0.22974|0.23809|  0.22780|  0.19568|  0.22003|  0.19363| 0.22613| 0.22442| 0.18981|  0.22267|
2009-10-10 |  0.17255|  0.16962|  0.16900|  0.17163|0.17675|  0.17119|  0.13662|  0.15961|  0.15710| 0.17596| 0.17299| 0.11108|  0.16488|
2011-10-05 |  0.02207| -0.00214|  0.01916|  0.01622|0.02740|  0.01492|  0.00351| -0.00020|  0.03052| 0.05038| 0.00762|-0.06152|  0.01731|
2012-10-03 |  0.10138|  0.08734|  0.09204|  0.08845|0.08840|  0.08984|  0.05691|  0.07066|  0.08264| 0.11586| 0.09239| 0.01565|  0.08760|
2013-09-21 |  0.11348|  0.10259|  0.11011|  0.10714|0.11271|  0.10878|  0.06291|  0.09811|  0.11904| 0.10717| 0.10147| 0.06465|  0.10160|
2014-09-23 |  0.06860|  0.07145|  0.07545|  0.07414|0.07651|  0.07039|  0.01418|  0.05892|  0.04876| 0.11045| 0.07126| 0.03412|  0.05993|
2015-09-22 |  0.17823|  0.16970|  0.18027|  0.18037|0.18425|  0.17371|  0.11224|  0.15585|  0.14010| 0.20391| 0.17273| 0.13111|  0.15974|

[fig1]: Output/mc_variability.png
[eq1]: Output/mc_var/norm_vol.png
[eq2]: Output/mc_var/norm_area.png
