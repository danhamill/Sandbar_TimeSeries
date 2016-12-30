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
To determine the effects of increasing sample size, the trends associated with the long-term moniroting sites establised in 1990 will be compared to the trends associated with larger sample sizes.  A simple first cut analysis is to compare the trends associated with the sites established in 1990 against the trends of all of the moniroing sites(Figure 1).
### Figure 1
![fig1][fig1]


Only river tirps where where of the long term sites in marbel canyon were included in the time sereis presentented in Figure 1 were included in the time sereis analysis.  Normalized Volumes and errors were calculated using Equation 1 and Equation 2, respectively.

### Equation 1

![eq1][eq1]

Where:
- n= Site
- x = Date

### Equation 2
![eq2][eq2]



[fig1]: Time_Series/Output/mc_variability.png
[eq1]: Time_Series/Output/mc_var/norm_vol.png
[eq2]: Time_Series/Output/mc_var/norm_area.png
