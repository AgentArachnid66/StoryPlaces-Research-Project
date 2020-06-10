# -*- coding: utf-8 -*-
#%%

#This cell gets the dataset and loads it into a variable. Much more efficient
# to do this once instead of doing it every time the program is run.
import pandas as pd

dataSet = pd.read_json("Modifiedlogevent-launchsubset.json", convert_dates=True)
dataSet.set_index("_id")

#%%
#This cell is to get required information for coding a lot quicker and easier
columns = dataSet.columns


#%%
#This cell is the Exploratory Data Analysis - Number of Users

userGrp = dataSet.groupby(dataSet["user"])
print("The number of users is " +str(userGrp.ngroups))

#%%
#This cell is the Exploratory Data Analysis - Pages Read Per User

# I made a new dataframe to save this data
pagePerUser  = pd.DataFrame()

# The first thing iI did was remove any rows that don't have any page IDs,
# Therefore they didn't read anything and shouldn't be included in the count
validPages = dataSet.copy().dropna(how='any', subset=['pageId'])

# After that, it was a simple case of grouping them by user and count the number
# Of occurances and store that as it's own variable
pagePerUser = validPages.groupby('user', as_index=False)['pageId'].count()
#Print the first 20 users with the pages read for each user
pagePerUser = pagePerUser[["user", "pageId"]]
pagePerUser.rename(columns={"pageId" : "pagesRead"}, inplace=True)
print("User: " +pagePerUser['user'].astype(str) +"    Pages Read: " +pagePerUser['pagesRead'].astype(str))

#%%
# This cell is the Exploratory Data Analysis - Page Reading Frequency 

pageFreq = validPages.groupby('pageId', as_index=False).size().reset_index()
pageFreq.columns = ['pageId', 'pageFreq']
print("Page: " +pageFreq['pageId'].astype(str) +"  Read Frequency: " +pageFreq['pageFreq'].astype(str))

