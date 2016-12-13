## We’re not plotting the right trips.
 
First, I don’t think you are plotting the data for post 2004 HFE?  This would have a trip date of 12/12/2004.  But there is a trip being plotted for 2004 right?  

- Three Trips in 2004
    - 2004-06-01
        - Surveyed 9 sites (8 with low elevation)
    - 2004-11-13
        - Surveyed 14 sites (all with low elevation)
    - 2004-12-02
        - Surveyed 33 sites (14 with low elevation)
	-  Need to come up with converiton to sort complete trips from non-complete trips
### Questions 
- What is the cut off for a complet trip (i.e how many sites need to be surveyed to be considered a "complete" trip.)
	- Peviously I had the cut off at 35
	- Went through LU_Time_Series.xlsx
		- Changed all trips to use to 'long'
		- Found several trips that can only be used in Marble Canyon

#### Answers: Which trips to use
- 11/6/1997 
	- Can only use above 25k

- 8/19/2000 and 9/9/2000 and 12/2/2004
	-Can only use in Marble canyon time series
- 5/17/2008
	- Dont use 1D backwater survey

*******
## Time Periods

And why does the sediment deficit period end at 2001?  I suggest we end it at 2003 so both periods have the same ending and starting date.  Deficit ends at Oct 2003 and Enrichment begins at 2003.  Does that make sense?
 
- I have added a field to the sandbar database "Period"
	- Sediment Deficit (1990-01-01 - 2003-11-01)
	- Sediment Enrichment (2003-11-01 - Present)

- - What sites do we not want to include in the analysis?
	- We have talked about:
		- M006R 
		- 033L
		- 062R
		- 068R
		- 167L
    - You have also suggested:
    	- 063L_r
    	- 063L_s

	- Change 'Time_Series' to reflect short or long term moniroting site
	- D
### Questions
- What do we want to do sites that got added in 2002 for the sediment deficit period?
	- Answer here


## Plot ideas
1. Site Variability
That does bring some other analyses to mind that might be interesting.  One paradigm has been that variability decreases with increasing distance from Glen Canyon Dam.  What about a plot that shows the standard error (or std. dev.) of all normalized values for each site plotted against distance for all surveys.  I would assume 003L would have the greatest variability since it is closest to the Paria.  Some sites are pretty stable.  It might make sense to just look at reattachment bars.

- One per bar type
	-Std. Error vs. River mile (plot all surveys, one point per site)
- This will help determine if we should use:
	- 009L (started surveying in 2008)
	- 045 separation (surveyed in 2002, 2004 and 2008+)
	- 070R (started surveying in 2008)
	- 167L (debris flow wiped it out so not good for dam related changes)

2. plot showing sample size difference in marble canyon
	- Sediment Enrichment Period
	- Long Term vs. All sites in marble canyon
		- See how they track
		
### Questions 
- Do we want one plot per complete trip?
- Or should I make one plot for the enitre time series?
	- Per period?



****
### which sites to use

- 044l_r 
	- No surveys 1990, 1991-1995
- 202r_r
	- Always exclude
- 035l_s
	- Use in sediment deficit period
	- Need to decide on what to do with sample size



***




