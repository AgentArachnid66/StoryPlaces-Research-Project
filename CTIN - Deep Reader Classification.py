# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

dataSet = pd.read_json("Modifiedlogevent-launchsubset.json", convert_dates=False)
dataSet.set_index("_id")

#%%

# This cell is for reading in the relevant dataframes so I don't have to run 
# other script to access them. I have also reformatted them here so that 
# they are easier to read. 

# The exit points DataFrame
DPRexitPoints = pd.read_csv("ExitPoints.csv").drop('Unnamed: 0', 1)
DPRexitPoints = DPRexitPoints.rename(columns={"0" : "NumExitedHere"})

# The Page Per User DataFrame
DPRpagePerUser = pd.read_csv("PagePerUserDF.csv").drop('Unnamed: 0', 1)

# The Page Reading Frequency
DPRpageReadingFrequency = pd.read_csv("PageReadingFrequency.csv").drop('Unnamed: 0', 1)

# The Page Visits Reading Frequency
DPRpageVisitsReaderFrequency = pd.read_csv("PageVisitsReaderFrequency.csv").drop('Unnamed: 0', 1)

# The Story Frequency
DPRstoryFrequency = pd.read_csv("StoryFrequency.csv")

# The Time Spent per Page
DPRtimeSpentOnPage = pd.read_csv("TimeSpentOnPage.csv").drop('Unnamed: 0', 1)

# The total time spent per user
DPRtotalTimePerUser = pd.read_csv("TotalTimePerUser.csv")

#%%

# This cell is for Detecting Deep Reads
# Have to make assumptions about what they are
# These assumptions will based on the dataset that I have access to, but as they 
# are likely to have to able to change, I'll store them in a variable

# I will make the following assumptions:
#   Time active > Median - Standard Deviation = Deep Reader
#   Number of Pages Read Per User > Median +/- Standard Deviation = Deep Reader
#   
#   If I can access the locations, then:
#       Average walking distance per user > Median - Standard Deviation = Deep Reader
#
#   Since I'm using 2/3 variables to classify deep readers, assuming I have 1
#   cut off point, I can have 4 to 9 different classes of readers based on these
#   variables. If a member has a high number of pages read, but low activity
#   time, they can be classed as a speed reader. The reverse of this would be
#   someone who takes their time with each page to absorb the narrative, but 
#   gets bored with it quite early on. If both occur, we can infer that they
#   are highly invested in the story. 
#
#   The location will help to classify them further as we can determine if
#   the highest visited pages are beciade they are close together and how
#   many users are 
#
# These assumptions are liable to change and will be tweak appropriately to 
# get the appropriate results. I'm using the Median as it's less effected by 
# extreme values and the standard deviaton will allow me to scale this up.


# My first step is to make a filter that stores these conditions
# As it is a date, it isn't as easy to get the median as calling the function.
# So I had to make it a list and find the middle value that way
DRconditionsTA = list(DPRtotalTimePerUser.sort_values(['TotalActiveTime'])['TotalActiveTime'])
# As the list could be even, I need a way to find the midpoint between dates

def try_totime(t):
    try:
        return pd.Timestamp(t)
    except:
        return np.nan

def date_median(date_list):
    length = len(date_list)
    print(length)
    if length % 2 != 0:
        return date_list[length//2]
    else:
        print((length//2), (length//2+1))
        lower = date_list[length//2]
        upper = date_list[(length//2) +1]
        return (lower + upper)/2
    
DRconditionsTA = DRconditionsTA[:-1]
TAmedian = date_median(DRconditionsTA)

#DRfilter = DPRtotalTimePerUser[DPRtotalTimePerUser['TotalActiveTime'] ]



#%%

# This cell is for average distance walked by user

#%%

# This cell is for average distance to the next page
