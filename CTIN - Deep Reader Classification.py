# -*- coding: utf-8 -*-

#Imports the libraries

import pandas as pd
import numpy as np
import ShelleysHeart as sh
import CTINResearch as ctin

#%%

# Imports the original dataset

dataSet = pd.read_json("Modifiedlogevent-launchsubset.json", convert_dates=False)
dataSet.set_index("_id")

#%%

# This cell is for reading in the relevant dataframes so I don't have to run 
# other script to access them. I have also reformatted them here so that 
# they are easier to read. 

# The exit points DataFrame
exitPoints = pd.read_csv("ExitPoints.csv").drop('Unnamed: 0', 1)
exitPoints = exitPoints.rename(columns={"0" : "NumExitedHere"})

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
# extreme values. However, it might give results that are of no value as they,
# split the readers in half and therefore gives not meaningful results.

DetectDeepReads = DPRpagePerUser.copy(deep=True)

# My first step is to make a filter that stores these conditions

print(pd.to_timedelta(DPRtotalTimePerUser['TotalActiveTime']).describe())
DPRtotalTimePerUser['TotalActiveTime'] = pd.to_timedelta(DPRtotalTimePerUser['TotalActiveTime'])
outlierFilter = (DPRtotalTimePerUser['TotalActiveTime'] >= DPRtotalTimePerUser['TotalActiveTime'].describe()['25%'] * (2/3))& (DPRtotalTimePerUser['TotalActiveTime'] <= DPRtotalTimePerUser['TotalActiveTime'].describe()['75%'] * (1.5))


filteredTTPU = DPRtotalTimePerUser[outlierFilter]
# Finds the relevant conditions for the total active time variable
TAmean = pd.to_timedelta(filteredTTPU['TotalActiveTime']).mean()

# Adds the relevant data to the dataframe to be filtered, and removes NaNs
DetectDeepReads['TotalActiveTime'] = DetectDeepReads['user'].map(DPRtotalTimePerUser.set_index('user')['TotalActiveTime'])
DetectDeepReads = DetectDeepReads.dropna(subset=['TotalActiveTime'])

# I'll make a function that will take in the row and assign a new variable to
# the column called class. 


# I made a new dictionary that will hold the different classes of reader
# I did this to make it easily expandable and to make it easy to change the class
# types
classes = [
    [# z = 0
     ["Checker"        ,"Intense Reader" ], 
     ["Speed Reader"   ,"Avid Reader" ]],
    # z =1 
    [["Active Checker" , "Active Intense Reader"],
     ["Active Speed"   , "Active Avid"]]
           ]


    
    
    


# These are filters to make the function's job a lot easier. They store 
# a boolean on the dataframe so that all the function needs to do is assign
# classes based on these values. It also helps to make it expandable as I just
# need to make a new filter and conditions on the function.
DetectDeepReads['NumPageFilter'] = DetectDeepReads['pagesRead'] >= 9
DetectDeepReads['TotTimeActFilter'] = pd.to_timedelta(DetectDeepReads['TotalActiveTime']) > pd.to_timedelta('0 days 00:27:37.970000')

# The function works by taking in 2 columns and generating a key
# to access the dictionary above. It's pure if statements, but is easy to read
def get_class(NumPageFilter, TotActTimeFilter, DistTravelledFilter=False):
    if(NumPageFilter):
        key1 = 1
    else:
        key1 = 0
    if(TotActTimeFilter):
        key2 = 1
    else:
        key2 = 0
    key3 = 0
    if(DistTravelledFilter):
        key3 = 1
    else:
        key3 = 0
    

    
    return classes[key3][key1][key2]
    


DetectDeepReads['reader class'] = DetectDeepReads.apply(lambda x: get_class(x.NumPageFilter, x.TotTimeActFilter), axis = 1)

ReaderClass = DetectDeepReads.groupby('reader class').count()
ReaderClass = ReaderClass['user']

#%%
# This cell is for average distance walked by user

# I can achieve this by looking at the locations at each page and which 
# page the user went to and add up the distances between each page visited.


sampleData = ctin.validPages
pageData = sh.pageData

sampleData = sampleData.sort_values(by=['user', 'date'])

sampleData['Latitude'] = sampleData['pageId'].map(pageData.set_index('id')['Latitude'])
sampleData['Longitude'] = sampleData['pageId'].map(pageData.set_index('id')['Longitude'])

DistWalkSamp = sampleData[['user', 'pageId','date','Latitude','Longitude']].dropna(how='any', subset=['Latitude', 'Longitude'])

DistWalk = DistWalkSamp

DistWalk['LatitudeCoordinateDifference'] = DistWalkSamp.groupby('user')['Latitude'].apply(lambda x: x.shift(-1))
DistWalk['LongitudeCoordinateDifference'] = DistWalkSamp.groupby('user')['Longitude'].apply(lambda x: x.shift(-1))

# To calculate the distance between each row, I saved the current location and the one
# that follows location

DistWalk['ApproxDistance'] = DistWalk.apply(lambda x: sh.haversine(x.Latitude,x.Longitude,x.LatitudeCoordinateDifference,x.LongitudeCoordinateDifference), axis =1)

# I now have the approximate distance between pages. This isn't the most
# accurate method available, but I can work on optimising it later
DistWalk = DistWalk.dropna(subset=['ApproxDistance'])

distance = DistWalk.groupby('user')['ApproxDistance'].sum().reset_index().sort_values('user')

DetectDeepReads['ApproxDistanceTravelled'] = DetectDeepReads['user'].map(distance.set_index('user')['ApproxDistance'])
DetectDeepReads = DetectDeepReads.dropna(subset=['ApproxDistanceTravelled'])

DetectDeepReads['DistTravelledFilter'] = DetectDeepReads['ApproxDistanceTravelled'] > distance['ApproxDistance'].mean()

DetectDeepReads['reader class'] = DetectDeepReads.apply(lambda x: get_class(x.NumPageFilter, x.TotTimeActFilter, x.DistTravelledFilter), axis = 1)


print(ctin.organiseDescribe(DistWalk['ApproxDistance'].describe()))
print(ctin.organiseDescribe(distance['ApproxDistance'].describe()))


#%%
#If natsort can't be found, paste this into the console and run it: !pip install natsort
import natsort
# This cell is for Deeper Exit Point Analysis

# This is set up so that I can clearly see the coordinates and what each page is.
DPRexitPoints = exitPoints.sort_values(by=['pageId'])
DPRexitPoints['Latitude'] = DPRexitPoints['pageId'].map(pageData.set_index('id')['Latitude'])
DPRexitPoints['Longitude'] = DPRexitPoints['pageId'].map(pageData.set_index('id')['Longitude'])
# I added the page names so that I can easily tell where in the story it
# is placed
DPRexitPoints['PageName'] = DPRexitPoints['pageId'].map(pageData.set_index('id')['name'])


DPRexitPoints = DPRexitPoints.iloc[natsort.index_humansorted(DPRexitPoints.PageName)]
DPRexitPoints = DPRexitPoints[['PageName', 'NumExitedHere']]
DPRexitPoints.to_csv('Deeper Exit Point Analysis.csv')

