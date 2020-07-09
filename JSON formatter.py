# -*- coding: utf-8 -*-
import re
import os


def get_file_as_String(fileToConvert):
    # Retrieves the file and depending on file type will perform the 
    # appropriate conversions to a str that can be used in the regexs
    data = open(file = fileToConvert)
    data = data.read()
    return data

# Place file path here and run the code to get the formatted JSON file
# It will be stored as a JSON file local to the project
fileName = "logevent-launchmonthsubset.json"



dataSet = get_file_as_String(fileName)

# I used Regular Expressions to replace parts of the data set with the correct
# formatting counter parts
idReformatting = re.sub(r'\{\"\$oid\"\:', "", dataSet)
idReformatting = re.sub(r'\}\,', r',', idReformatting)
dateReformatting = re.sub(r'\{\"\$date\"\:', "", idReformatting)
dataReformatting = re.sub(r'\"data\"\:\{', "", dateReformatting)

#The first step to convert it into an array that can be read in to a 
# data frame is to add the commans after every entry
addCommas = re.sub(r'\_\_v\"\:0\}', r'__v":0},', dataReformatting)

# I'll remove the last comma on the end entry so that I don't have
# to remove manually or corrupt my JSON data file. I did this the most
# efficient way I could think of as the alternative was making it a list which
# would be highly inefficient with larger data sets.
addCommas = addCommas[:-2]


# Then I will use square brackets and add them onto the sides of the string.
# First I will check that they don't already have them. Since I have removed 
#the last 2 elements of the string, they will need to be added back on, but
# the front one still needs a check
finalString = addCommas
if addCommas[0] != "[":
    finalString = "[" +addCommas +"]"
    
# I remove the file extension so that I can write is as a JSON using the 
# original file name with the prefix "Modified" to differentiate it from the 
# original file
fileNameWOext = os.path.splitext(fileName)[0]
# I saved my dataSets in a separate folder, so I had to remove that directory
fileNameWOext = re.sub(r'DataSet\/', r'', fileNameWOext)
saveFile = "Modified" +fileNameWOext +".json"

#%%
#This final part of the code will save the string as a JSON file
# As the string is valid JSON already, this won't cause any issues
# But I had issues when I used json.dump
with open(saveFile, "w") as f:
    f.write(finalString)
print("Produced JSON file")
    