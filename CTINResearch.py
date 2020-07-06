# -*- coding: utf-8 -*-
#%%

# This cell imports the necessary libraries
import pandas as pd
import re
import numpy as np
import ShelleysHeart as sh

#%%
# This cell gets the dataset and loads it into a variable. Much more efficient
# to do this once instead of doing it every time the program is run.
dataSet = pd.read_json("Modifiedlogevent-launchsubset.json", convert_dates=False)
dataSet.set_index("_id")
dataSet['date'] = pd.to_datetime(dataSet['date'])

#%%
# This cell is to get required information for coding a lot quicker and easier.
# This includes functions and variables that I need quick access to.

columns = dataSet.columns

# I wrote a function to re organise the describe values so that they are easier
# to paste into the main document
def organiseDescribe(value):
    removeWhiteSpace = re.sub(r'  ', r'', str(value))
    addColon  = re.sub(r' ', r':', removeWhiteSpace)
    rewriteSTD = re.sub("std", "Standard Deviation:", addColon)
    return rewriteSTD

def removeDuplicate(current, previous):
    if current == previous:
        return np.nan
    else:
        return current

#%%
# This cell is the Exploratory Data Analysis - Number of Users

userGrp = dataSet.groupby(dataSet["user"])

print("The number of users is: " +str(userGrp.ngroups))

#%%

# This cell is for data cleanup

# I made a new dataframe to save this data
pagePerUser  = pd.DataFrame()

# The first thing I did was remove any rows that don't have any page IDs,
# Therefore they didn't read anything and shouldn't be included in the count.
validPages = dataSet.copy(deep=True).dropna(how='any', subset=['pageId'])
validPages = validPages.drop_duplicates(subset = ['date', 'user']).drop_duplicates(subset = ['pageId', 'user', 'date'], keep = 'last')
# I also got rid of the duplicates of pages at once. For example, if they read
# the same page 3 times, without switching, I would get rid of the following
# duplicates to get an accurate conclusion
validPages = validPages.sort_values(['user', 'date'])
validPages['NextPage'] = validPages.groupby('user')['pageId'].apply(lambda x: x.shift(-1))
validPages['pageId'] = validPages.apply(lambda x: removeDuplicate(x.pageId, x.NextPage), axis=1 )
validPages = validPages.dropna(subset=['pageId'])

#%%

# This cell is the Exploratory Data Analysis - Pages Read Per User

# It was a simple case of grouping the validPages by user and count the number
# Of occurances and store that as it's own variable
pagePerUser = validPages.groupby('user', as_index=False)['pageId'].count()
# Removes all columns except the relevant ones
pagePerUser = pagePerUser[["user", "pageId"]]
# Changes the pages Id column to pagesRead as it's now a count of how many
# pages were read by a user.
pagePerUser.rename(columns={"pageId" : "pagesRead"}, inplace=True)

# Save this Data Frame as a csv
pagePerUser.to_csv("PagePerUserDF.csv")

print("User: " +pagePerUser['user'].astype(str) +"    Pages Read: " +pagePerUser['pagesRead'].astype(str))

print(organiseDescribe(pagePerUser.describe()))
#%%
# This cell is the Exploratory Data Analysis - Page Reading Frequency 

# Like the cell above, I split them  this time by page ID and the size of the
# new groups. This should get the number of times it showed up in the logs
# therefore the number of times players went onto that page 
# therefore the page reading frequency.
pageFreq = validPages.groupby('pageId', as_index=False).size().reset_index()
# In the generated DataFrame above, the pageFreq column was named 0 and this 
# just changes it back to human readable terms and lets me reference it in
# other parts of the script
pageFreq.columns = ['pageId', 'pageFreq']

sh.pageData['Frequency'] = sh.pageData['id'].map(pageFreq.set_index('pageId')['pageFreq'])
sh.pageData.to_csv('PageData.csv')

# Saves it to a csv for further analysis
pageFreq.to_csv("PageReadingFrequency.csv")

print("Page: " +pageFreq['pageId'].astype(str) +"  Read Frequency: " +pageFreq['pageFreq'].astype(str))
print(organiseDescribe(pageFreq['pageFreq'].describe()))

#%%
# This cell is the Exploratory Data Analysis - Story Frequency

# Check if any rows have no story Id
validStories = dataSet.copy().dropna(how='any', subset=['storyId', 'user'])
# Group by the story ID and count the number of users in each group
storyFreq = validStories.groupby('storyId')

# Counts the number of users that accessed each story
storyFrequency = storyFreq['user'].count()
print(storyFrequency.head())
storyFrequency.to_csv("StoryFrequency.csv")


# To separate by user, I will group by story Id first and then by user
storyFreqU = validStories[["user", "storyId"]].groupby(['storyId','user'])
#%%
# This cell is the Exploratory Data Analysis - Time Spent on each Page

# Checks if any rows have no date information or page Id and copies the 
# data frame to the variable. Then drop any that duplicate dates
validPageTimes = validPages.copy(deep=True)

# Generates a new DataFrame for the time spent on each page based on user, 
# date and page id. 
timePage = validPageTimes[['user', 'date', 'pageId']].groupby(['user', 'date','pageId']).count().reset_index()

# Converts the date series into datetime
timePage['date'] = pd.to_datetime(timePage['date'])

# Copy the Data frame to another variable for further manipulation in another
# cell.
userPage = timePage.copy(deep=True)

# Goes through the group and calculates the difference between the dates and 
# shifts it up one row so that it matches to the correct pageId
timePage['timeOnPage'] = timePage.groupby('user')['date'].apply(lambda x: x.diff().bfill().shift(-1))


# This dataframe will be useful in the exit point analysis and deep reader 
# classification as it tells me when people stopped reading
exitPoints = timePage[timePage['timeOnPage'].isnull()]
exitPoints = exitPoints.drop('timeOnPage', 1)


# Drops NaN values from the data set
timePage = timePage.dropna(how='any', subset = ['timeOnPage'])
timePage.to_csv("TimeSpentOnPage.csv")

print(organiseDescribe(timePage['timeOnPage'].describe()))


#%%

# This cell is the Exploratory Data Analysis - Exit Point Frequency
# This is where each user stops reading. I can use the exitPoints dataframe
# I made in a previous cell as a basis for this. I just need to group it by
# page and count if there are any pages that are the most likely to be the 
# exit point.

exitPoints['Latitude'] = exitPoints['pageId'].map(sh.pageData.set_index('id')['Latitude'])
exitPoints['Longitude'] = exitPoints['pageId'].map(sh.pageData.set_index('id')['Longitude'])

sortExit = (exitPoints.groupby('pageId').size().sort_values(ascending=False)).reset_index()
sortExit.to_csv("ExitPoints.csv")

#%%

#This cell is the Exploratory Data Analysis - Total Time Per User

# Groups by user and gets the first and last date values in the group
userTime = userPage.groupby('user')['date'].agg(['first','last'])
# Renames the columns to more appropriate terms
userTime.columns = ["login time","logout time"]
# Filter to get rid of the users who didn't read beyond one page
# It works under the assumption that if you only read one page, then 
# you wouldn't have another timestamp from a different page, 
# Therefore the first and last timestamps would be identical
timeFilter = userTime['logout time'] != userTime['login time']
filteredUserTime = userTime[timeFilter]

# Calculates the time difference between timestamps
filteredUserTime["TotalActiveTime"] = userTime['logout time'] - userTime['login time']
#filteredUserTime['TotalActiveTime'] = pd.to_datetime(filteredUserTime['TotalActiveTime'])
# If I had left in the users who only looked at one page,
# These results would have been skewed
print(organiseDescribe(filteredUserTime['TotalActiveTime'].describe()))
filteredUserTime.to_csv("TotalTimePerUser.csv")

#%%

#This cell is the Exploratory Data Analysis - Page Visits Reader Frequency

#This is how many people visited a certain number of pages

pageVisitPerUser = pagePerUser.copy(deep=True)['pagesRead'].value_counts().reset_index().sort_values(['index']).reset_index()
pageVisitPerUser = pageVisitPerUser[['index', 'pagesRead']].rename(columns={'index':'NumberPagesRead','pagesRead' : 'Frequency'})
print(pageVisitPerUser)

pageVisitPerUser.to_csv("PageVisitsReaderFrequency.csv")