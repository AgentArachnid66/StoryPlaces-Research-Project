# -*- coding: utf-8 -*-

import pandas as pd

dataSet = pd.read_json("Modifiedlogevent-launchsubset.json", convert_dates=True)
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
#   Time active > Median +/- Standard Deviation = Deep Reader
#   Number of Pages Read Per User > Median +/- Standard Deviation = Deep Reader
# These assumptions are liable to change and will be tweak appropriately to 
# get the appropriate results

#%%

# This cell is for average distance walked by user

#%%

# This cell is for average distance to the next page
