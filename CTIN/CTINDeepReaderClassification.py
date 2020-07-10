# -*- coding: utf-8 -*-

#Imports the libraries

import pandas as pd
import numpy as np
import ShelleysHeart as sh
import CTINResearch as ctin
import natsort


#%%

# Imports the original dataset

# INPUT FILE PATH HERE!! - Same data file as the CTINResearch script
dataSet = pd.read_json("", convert_dates=False)
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


# I made a multi dimensional array to hold the values of each class
# To add in a new classification, add a new dimension. To add a column, 
# add a new array to the required dimension. 
classes = [[
     ["Checker"                        ,"Intense Reader" ], 
     ["Light Reader"                   , "Slow Reader"],
     ["Speed Reader"                   ,"Avid Reader" ],
     ["Multi Story Speed Reader"       , "Dedicated Reader"]],
    [["Active Checker"                 , "Active Intense Reader"],
     ["Active Light Reader"            , "Active Slow Reader"],
     ["Active Speed"                   , "Active Avid"],
     ["Active Multi Story Speed Reader", "Active Dedicated Reader"]]
           ]

classDf = pd.DataFrame(classes[0]).append(pd.DataFrame(classes[1]))
classDf.to_csv("class.csv")

# The function works by taking in n columns and generating a key
# to access the n-dimensional array above. 
# It's pure if statements, but is easy to read. To access a newly added 
# classification, add in the variable to the parameters and set up the 
# if statement to check if it's None and if it has a value do the classification
def get_class(NumPage, TotActTime, DistTravelled=None, reachedEndPage=False):
    if(reachedEndPage):
        x = 3
    elif(NumPage >= 9):
        x = 2
    elif(NumPage > 3):
        x = 1

    else:
        x = 0
    if(pd.to_timedelta(TotActTime) > pd.to_timedelta(('0 days 00:30:00.000000'))):
        y = 1
    else:
        y = 0
    z = 0
    if(DistTravelled != None):
        if(DistTravelled > 200.0):
            z = 1
        else:
            z=0
    else:
        z = 0
    
    return classes[z][x][y]
    


DetectDeepReads['reader class'] = DetectDeepReads.apply(lambda x: get_class(x.pagesRead, x.TotalActiveTime), axis = 1)

ReaderClass = DetectDeepReads.groupby('reader class').count()
ReaderClass = ReaderClass['user']
ReaderClass.to_csv('ReaderClass.csv')

#%%
# This cell is for average distance walked by user

# I can achieve this by looking at the locations at each page and which 
# page the user went to and add up the distances between each page visited.

# DistWalk is the Distance by User per Page
# distance is the total Distance per user

# imports relevant variables from other modules
sampleData = ctin.validPages
pageData = sh.pageData

# Sorts the dataset by the relevant values
sampleData = sampleData.sort_values(by=['user', 'date'])

# Adds in the location information by mapping the relevant information
# from the page data dataframe to a new column.
sampleData['Latitude'] = sampleData['pageId'].map(pageData.set_index('id')['Latitude'])
sampleData['Longitude'] = sampleData['pageId'].map(pageData.set_index('id')['Longitude'])

# Dropping the irrelevant data
DistWalkSamp = sampleData[['user', 'pageId','date','Latitude','Longitude']]

# Saves it in another variable in case I want to do further analysis on the
# original dataset
DistWalk = DistWalkSamp

# I saved the coordinates of the page each user read next. I did this as I 
# couldn't figure out in the time limit how to compare separate rows at
# once. 
DistWalk['LatitudeCoordinateDifference'] = DistWalkSamp.groupby('user')['Latitude'].apply(lambda x: x.shift(-1))
DistWalk['LongitudeCoordinateDifference'] = DistWalkSamp.groupby('user')['Longitude'].apply(lambda x: x.shift(-1))

# To calculate the distance between each row, I saved the current location and 
# the one that follows. I then applied the haversine function that I defined
# in a separate module.
DistWalk['ApproxDistance'] = DistWalk.apply(lambda x: sh.haversine(x.Latitude,x.Longitude,x.LatitudeCoordinateDifference,x.LongitudeCoordinateDifference), axis =1)

# I now have the approximate distance between pages. This isn't the most
# accurate method available, but I can work on optimising it later

# Up until now, I have NaNs in my data so I'm just going to fill them in with
# 0 as they are the end of a reading, therefore they haven't moved and 
# therefore they have moved 0m.
DistWalk = DistWalk.fillna(0)

# Now I just add up each user's distance travelled, reset the index to 
# get a dataframe and sort by the user.
distance = DistWalk.groupby('user')['ApproxDistance'].sum().reset_index().sort_values('user')

# Now I map these distances to the main deep reader dataframe for use in 
# further classification.
DetectDeepReads['ApproxDistanceTravelled'] = DetectDeepReads['user'].map(distance.set_index('user')['ApproxDistance'])


# I then call the function to classify the readers using this new classification
DetectDeepReads['reader class'] = DetectDeepReads.apply(lambda x: get_class(x.pagesRead, x.TotalActiveTime, x.ApproxDistanceTravelled), axis = 1)

# Counting how many of each reader class there are
DeeperReaderClass = DetectDeepReads.groupby('reader class').count()
DeeperReaderClass = DeeperReaderClass['user']
 
# Getting rid of the outliers for the describe function to properly function
distanceOutlierFilter = (distance['ApproxDistance'] >= distance['ApproxDistance'].describe()['25%'] * (2/3)) & (distance['ApproxDistance'] <= distance['ApproxDistance'].describe()['75%'] * (1.5))
filteredDistance = distance[distanceOutlierFilter]
# Get the distance walked between pages
print(ctin.organiseDescribe(DistWalk['ApproxDistance'].describe()))
# Get the total distance per user
print(ctin.organiseDescribe(filteredDistance['ApproxDistance'].describe()))

# Saves to a csv so that I can easily display it.
DeeperReaderClass.to_csv("DeepReaderClass.csv")
#%%
# This cell is to explore how many users reached the end page

# An important decision to make is what consists of the end page? Is it the
# Page that the story ends? Is it the page that thanks the player for playing?
# Or is it the page that is named Exit Story? 
# 
# For the time being, I'll include all 3 with the intention of making this 
# decision later. 

# To do this, I'll simply filter for the page id in the pages that each user 
# read and count the number of instances


# To change pages to analyse, change page ID here. Can be accessed from pageData
# variable for reference
endPages = ["47480a57-3aee-4176-c171-7a02b2572a57",
            "16b83f63-1263-4069-643a-01f7029b1f49",
            "c05eacac-cf06-4eb2-dd60-323e08aaf064",
            "5eb7c764-0aa4-4984-2b27-2515b92cb252",
            "c56a29d1-0564-403b-8a82-0697a3d40080",
            "1e4f4680-20d8-4df4-1828-00550dec362e",
            "bbc0da17-194b-473a-b865-c9efb8ae94f6",
            "981468a4-d38f-4fd3-4b4c-dbb03637ef32",
            "3bfc772a-2257-4244-3e75-51c181bee1a9",
            "dafd6c3f-9bed-4879-d90b-20001528504b"
            ]

test = ctin.validPages

endPageFilter = ctin.validPages.pageId.isin(endPages)
UserReachedEnd = ctin.validPages[endPageFilter]


# Tests to see if the user reached the end page in a realistic time frame
timeFrame = "0 days 00:20:04.079000"
#UserReachedEnd = UserReachedEnd[['user', 'pageId', 'pageName']]
UserReachedEnd['NextEndDate']= UserReachedEnd.groupby('user')['date'].apply(lambda x: x.shift(-1))
UserReachedEnd['TimeDifference'] = pd.to_datetime(UserReachedEnd['NextEndDate']) - pd.to_datetime(UserReachedEnd['date'])
UserReachedEnd['TimeDifference'] = UserReachedEnd['TimeDifference'].fillna(pd.to_timedelta("0 days 00:30:04.079000"))
endPageDupFilter = UserReachedEnd['TimeDifference'] > pd.to_timedelta(timeFrame)

# Filters out those who didn't get to the end in the time frame specified
UserReachedEnd = UserReachedEnd[endPageDupFilter]
# Uses this filtered DataFrame to compare users to save if they reached the
# end page in a realisitic time frame
DetectDeepReads['reachedEndPage'] = DetectDeepReads.user.isin(UserReachedEnd['user'])

# I then call the function to classify the readers using this new classification
DetectDeepReads['reader class'] = DetectDeepReads.apply(lambda x: get_class(x.pagesRead, x.TotalActiveTime, x.ApproxDistanceTravelled ,x.reachedEndPage), axis = 1)

# Counting how many of each reader class there are
DeeperReaderClass = DetectDeepReads.groupby('reader class').count()
DeeperReaderClass = DeeperReaderClass['user']

DeeperReaderClass.to_csv("DeepReaderClass.csv")

# Page name attached to the page ID
UserReachedEnd['pageName'] = UserReachedEnd['pageId'].map(pageData.set_index('id')['name'])


#%%
# If natsort can't be found, paste this into the console and run it: 
# !pip install natsort


# This cell is for Deeper Exit Point Analysis

# This is set up so that I can clearly see the coordinates and what each page is.
DPRexitPoints = exitPoints.sort_values(by=['pageId'])
DPRexitPoints['Latitude'] = DPRexitPoints['pageId'].map(pageData.set_index('id')['Latitude'])
DPRexitPoints['Longitude'] = DPRexitPoints['pageId'].map(pageData.set_index('id')['Longitude'])
# I added the page names so that I can easily tell where in the story it
# is placed
DPRexitPoints['PageName'] = DPRexitPoints['pageId'].map(pageData.set_index('id')['name'])

# Sorts the page names by number then letter
DPRexitPoints = DPRexitPoints.iloc[natsort.index_humansorted(DPRexitPoints.PageName)]
# Drops unnecessary columns
DPRexitPoints = DPRexitPoints[['PageName', 'NumExitedHere']]
DPRexitPoints.to_csv('Deeper Exit Point Analysis.csv')

#%%

# This cell is to explore the average time spent on each page

# List of each page and frequency of time on each page

# Drops unnecessary columns then sorts them by ID
AvTimeOnPage = DPRtimeSpentOnPage.drop(['user', 'date'], axis=1).sort_values('pageId')

# Changes the dtype of the timeOnPage columns to timeDelta
AvTimeOnPage['timeOnPage'] = AvTimeOnPage.apply(lambda x: pd.to_timedelta(x.timeOnPage), axis=1)
# Maps the page names to the page Ids to make the column easier to read
AvTimeOnPage['PageName'] = AvTimeOnPage['pageId'].map(pageData.set_index('id')['name'])
# Groups by the page id so that I can aggragate by the right groups
AvTimeOnPageGrp = AvTimeOnPage.groupby('pageId')
# Finds average time spent on each page and then resets index to return a 
# dataframe
AvTimeOnPageGrpMean = AvTimeOnPageGrp['timeOnPage'].mean(numeric_only=False).reset_index()
# Maps the page names back to the dataframe I just created
AvTimeOnPageGrpMean['PageName'] = AvTimeOnPageGrpMean['pageId'].map(pageData.set_index('id')['name'])
# Sorts the dataframe by the page name by number then letter
AvTimeOnPageGrpMean = AvTimeOnPageGrpMean.iloc[natsort.index_humansorted(AvTimeOnPageGrpMean.PageName)].set_index('PageName')

# Saves this dataframe as a csv
AvTimeOnPageGrpMean.to_csv('AverageTimeOnPage')


#%%

# This cell is for average time spent per page for each user
DetectDeepReads['AverageTimePerPage'] = DetectDeepReads['TotalActiveTime'] / DetectDeepReads['pagesRead']
print(ctin.organiseDescribe(DetectDeepReads['AverageTimePerPage'].describe()))
#%%

# This cell is to add in the exit page for each user.

userExit = ctin.exitPoints

DetectDeepReads['ExitPoints'] = DetectDeepReads['user'].map(userExit.set_index('user')['pageId'])

DetectDeepReads['ExitPointsName'] = DetectDeepReads['ExitPoints'].map(pageData.set_index('id')['name'])

DetectDeepReads.to_csv('DeepReaderClassificationTable.csv')