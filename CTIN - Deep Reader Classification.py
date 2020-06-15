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
#   Time active > Median = Deep Reader
#   Number of Pages Read Per User > Median = Deep Reader
#   
#   If I can access the locations, then:
#       Average walking distance per user > Median  = Deep Reader
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
# extreme values.

DetectDeepReads = DPRpagePerUser.copy(deep=True)

# My first step is to make a filter that stores these conditions

# Finds the relevant conditions for the total active time variable
TAmedian = pd.to_timedelta(DPRtotalTimePerUser['TotalActiveTime']).median()
# TAsd =  DPRtotalTimePerUser['TotalActiveTime'].std()

# Finds the relevant conditions for the time on page variable
ToPmedian = (DPRpagePerUser['pagesRead']).median()
# ToPsd = DPRtimeSpentOnPage['timeOnPage'].std()

# Adds the relevant data to the dataframe to be filtered, and removes NaNs
DetectDeepReads['TotalActiveTime'] = DetectDeepReads['user'].map(DPRtotalTimePerUser.set_index('user')['TotalActiveTime'])
DetectDeepReads = DetectDeepReads.dropna(subset=['TotalActiveTime'])

# I'll make a function that will take in the row and assign a new variable to
# the column called class. 


# I made a new dictionary that will hold the different classes of reader
# I did this to make it easily expandable and to make it easy to change the class
# types
classes = { "" : np.nan,
            "High Number Pages And High Total Active Time" : "Avid Reader",
           "High Number Pages And Low Total Active Time" : "Speed Reader",
           "Low Number Pages And High Total Active Time" : "Intense Reader",
           "Low Number Pages And Low Total Active Time" : "Checker"}


# These are filters to make the function's job a lot easier. They store 
# a boolean on the dataframe so that all the function needs to do is assign
# classes based on these values. It also helps to make it expandable as I just
# need to make a new filter and conditions on the function.
DetectDeepReads['NumPageFilter'] = DetectDeepReads['pagesRead'] > ToPmedian
DetectDeepReads['TotTimeActFilter'] = pd.to_timedelta(DetectDeepReads['TotalActiveTime']) > TAmedian

# The function works by taking in 2 columns and generating a key
# to access the dictionary above. It's pure if statements, but is easy to read
def get_class(NumPageFilter, TotActTimeFilter):
    key = ""
    if(NumPageFilter):
        key += "High Number Pages And "
    else:
        key += "Low Number Pages And "
    if(TotActTimeFilter):
        key += "High Total Active Time"
    else:
        key += "Low Total Active Time"
    
    return classes[key]
    
DetectDeepReads['reader class'] = DetectDeepReads.apply(lambda x: get_class(x.NumPageFilter, x.TotTimeActFilter), axis = 1)

ReaderClass = DetectDeepReads.groupby('reader class').count()
ReaderClass = ReaderClass['user']

#DeepReaders = dataSet[DRfilter]
#%%
# This cell is for average distance walked by user

# I can achieve this by looking at the locations at each page and which 
# page the user went to and add up the distances between each page visited.


#%%

# This cell is for average distance to the next page

# I can do this by looking at the location of each page and compare it to the
# one that comes after it.
