# -*- coding: utf-8 -*-
#%%


import pandas as pd
import re


#%%
#This cell gets the dataset and loads it into a variable. Much more efficient
# to do this once instead of doing it every time the program is run.
dataSet = pd.read_json("Modifiedlogevent-launchsubset.json", convert_dates=True)
dataSet.set_index("_id")

#%%
#This cell is to get required information for coding a lot quicker and easier.
#This includes functions and variables that I need quick access to.

columns = dataSet.columns

def organiseDescribe(value):
    removeWhiteSpace = re.sub(r'  ', r'', str(value))
    addColon  = re.sub(r' ', r':', removeWhiteSpace)
    rewriteSTD = re.sub("std", "Standard Deviation:", addColon)
    rewriteMedian = re.sub(r'50\%', "Median", rewriteSTD)
    return rewriteMedian



#%%
#This cell is the Exploratory Data Analysis - Number of Users

userGrp = dataSet.groupby(dataSet["user"])
print("The number of users is " +str(userGrp.ngroups))

#%%
#This cell is the Exploratory Data Analysis - Pages Read Per User

# I made a new dataframe to save this data
pagePerUser  = pd.DataFrame()

# The first thing I did was remove any rows that don't have any page IDs,
# Therefore they didn't read anything and shouldn't be included in the count
validPages = dataSet.copy().dropna(how='any', subset=['pageId'])

# After that, it was a simple case of grouping them by user and count the number
# Of occurances and store that as it's own variable
pagePerUser = validPages.groupby('user', as_index=False)['pageId'].count()
#Print the first 20 users with the pages read for each user
pagePerUser = pagePerUser[["user", "pageId"]]
pagePerUser.rename(columns={"pageId" : "pagesRead"}, inplace=True)

print("User: " +pagePerUser['user'].astype(str) +"    Pages Read: " +pagePerUser['pagesRead'].astype(str))

print(pagePerUser.describe())
#%%
# This cell is the Exploratory Data Analysis - Page Reading Frequency 

# Like the cell above, I split them  this time by page ID and the size of the
# new groups. This should get the number of times it showed up in the logs
# therefore the number of times players went onto that page 
# therefore the page reading frequency.
pageFreq = validPages.groupby('pageId', as_index=False).size().reset_index()
#In the generated DataFrame above, the pageFreq column was named 0 and this 
# just changes it back to human readable terms and lets me reference it in
# other parts of the script
pageFreq.columns = ['pageId', 'pageFreq']
print("  Read Frequency: " +pageFreq['pageFreq'].astype(str))

print(pageFreq['pageFreq'].describe())

#%%
#This cell is the Exploratory Data Analysis - Story Frequency

# Check if any rows have no story Id
validStories = dataSet.copy().dropna(how='any', subset=['storyId', 'user'])
#Group by the story ID and count the number of users in each group
storyFreq = validStories.groupby('storyId')

storyFrequency = storyFreq['user'].count()

#To separate by user, I will group by story Id first and then by user
storyFreqU = validStories[["user", "storyId"]].groupby(['storyId','user'])
print(storyFreqU['storyId'])

#%%
# This cell is the Exploratory Data Analysis - Time Spent on each Page

# Checks if any rows have no date information or page Id.
validPageTimes = dataSet.copy().dropna(how='any', subset=['date', 'pageId'])

#timePage = validPageTimes


timePage = validPageTimes[['user', 'date', 'pageId']].groupby(['user', 'date','pageId']).count().reset_index()

timePage['date'] = pd.to_datetime(timePage['date'])
timePage['timeOnPage'] = timePage.groupby('user')['date'].apply(lambda x: x.diff().bfill().shift(-1))

#ExitPoints = timePage.groupby('user').tail('timeOnPage')

# Drops NaN values from the data set
timePage = timePage.dropna(how='any', subset = ['timeOnPage'])
print(organiseDescribe(timePage['timeOnPage'].describe()))
#%%
# Exit Point Frequency



