# -*- coding: utf-8 -*-
import pandas as pd
import CTINDeepReaderClassification as ctin
import CTINResearch as orctin
import re
import numpy as np
from ShelleysHeart import haversine
from scipy import stats

#%%
data = orctin.validPages
exitPoints = orctin.exitPoints[['pageId']]
pageData = ctin.sh.pageData

#%%

# This cell holds all the functions required for the choice analysis

# Saves the frequency attached to each page to the pageData dataframe
pageData['Frequency'] = pageData['id'].map(orctin.pageFreq.set_index('pageId')['pageFreq'])

# Class that holds the index and can get the number of people that went to 
# certain choices and the distance to those choices. I used a class as it
# will be useful later on when I need certain functionality to do analysis
class indexChoice():
    
    def __init__(self, index):
        self.index = index
    
    def getChoices(self):
        return checkBranch(self.index)[1]
        
    def setIndex(self, newIndex):
        self.index = newIndex
    
    def getIndex(self):
        return self.index

    # Instead of iterating through all the data, just look up the value in 
    # a series that already calculated it for me.
    def getNumUsers(self):
        page = pageData['Frequency'].iloc[self.index]
        return page
    
    # Gets the connected nodes and the optionally the distances to those 
    # nodes.
    def getBranches(self, distance=False):
        # I am overloading this function so I need a condition to let python
        # know that that it what I want
        if distance:
            branches = checkBranch(self.index)[:2]
        else:
            branches = checkBranch(self.index)[1:]

        # This is the last net to catch nodes that lead 
        # to this node. 
        localBranches = []
        for i in branches[1]:
            if i > self.index:
                localBranches.append(i)
            else:
                # deletes the locations with the relevant index
                del branches[0][branches[1].index(i)]
                
        return branches[0], localBranches
    
    # This function takes in the branch index and returns the number of people
    # who chose that route and the distance to that route
    def getBranchResult(self):
        frequency = []
        # Retrievest the branches to use in the calculations
        branches = self.getBranches(distance=True)
        # Iterates through the branches
        for i in branches[1]:
            # Slight bug occured when this wasn't in place. This seemed
            # to fix it so please DO NOT REMOVE IT
            indices[i].setIndex(i)
            # appends the number of users at a node to the list
            frequency.append(indices[i].getNumUsers())
        
        # retrieves and splits the tuple so that it can be used in an array
        # as separate elements
        distance, node = branches        
        return [node, distance, frequency]
                
# This function initialises the graphical representation of Shelley's Heart
def initial_graph():
    
    # Instead of typing out 77 integers in the array, I can just do a simple
    # iteration and get them done a lot quicker
    exitNode = [None] * 78
    for i in range (len(exitNode)):
        exitNode[i] = i
    
    
    # This dictinary holds of the page index in page data as a key and the 
    # connected node's index as a value. This should allow for relatively
    # easy traversion
        
    # The connection to the previous node is stored as it's last index on the 
    # value. I've also stored the connection to the exit story page as the 
    # second to last index. However, with some nodes, they have 2 previous 
    # node connections, which I will handle with some functions later.
        
    return { 
        
        0: [55, 35, 19, 1],
        
        # Byron Branch
        1: [2, 78, 0],
        2: [3, 78, 1],
        3: [6, 78, 2],
        4: [],
        5: [],
        6: [8, 7, 78, 3],
        7: [9, 78, 6],
        8: [9, 78, 6],
        9: [10, 8, 78, 7],
        10: [12, 11, 78, 9],
        11: [13, 78, 10],
        12: [13, 78, 10],
        13: [14, 12, 78, 11],
        14: [16, 15, 78, 13],
        15: [17, 78, 14],
        16: [18, 78, 14],
        17: [75, 78, 15],
        18: [75, 78, 16],
        
        # Percy Branch
        19: [21, 20, 78, 0],
        20: [23, 22, 78, 19],
        21: [23, 22, 78, 19],
        22: [24, 21, 78, 20],
        23: [24, 21, 78, 20],
        24: [25, 23, 78, 22],
        25: [26, 78, 24],
        26: [29, 28, 78, 25],
        27: [],
        28: [30, 78, 26],
        29: [30, 78, 26],
        30: [31, 29, 78, 28],
        31: [33, 32, 78, 30],
        32: [34, 78, 31],
        33: [34, 78, 31],
        34: [33, 76, 78, 32],
        
        # Mary Branch
        35: [36, 78, 0],
        36: [39, 38, 78, 35],
        37: [],
        38: [40, 78, 36],
        39: [40, 78, 36],
        40: [41, 39, 78, 38],
        41: [43, 42, 78, 40],
        42: [44, 78, 41],
        43: [44, 78, 41],
        44: [46, 45, 43, 78, 42],
        45: [47, 78, 44],
        46: [47, 78, 44],
        47: [48, 46, 78, 45],
        48: [50, 49, 78, 47],
        49: [51, 78, 48],
        50: [51, 78, 48],
        51: [53, 52, 50, 78, 49],
        52: [54, 78, 51],
        53: [54, 78, 51],
        54: [77, 52, 78, 53],
        
        # John Branch 
        55: [56, 78, 0],
        56: [59, 58, 57, 78, 55],
        57: [60, 78, 56],
        58: [60, 78, 56],
        59: [60, 78, 56],
        60: [61, 59, 58, 78, 57],
        61: [63, 78, 60],
        62: [],
        63: [64, 78, 61],
        64: [66, 65, 78, 63],
        65: [67, 78, 64],
        66: [67, 78, 64],
        67: [69, 68, 66, 78, 65],
        68: [70, 78, 67],
        69: [70, 78, 67],
        70: [72, 71, 69, 78, 68],
        71: [73, 78, 70],
        72: [73, 78, 70],
        73: [74, 72, 78, 71],

        74: [78, 73],
        75: [78, 18], 
        76: [78, 34],
        77: [78, 54],
        
        78: exitNode
        
        }

# This function converts the page Id to the index of the page ID on the 
# PageData dataframe. This makes it easier to read and allows me to use it as 
# a key to access the dictionary. It also retrieves the index of a list to
# get the index of a particular branch in the story for use in another function
def getIndex(value, useBranch = False):
    # As I am essentially overloading the function, I need a boolean to tell
    # Python that I want this function to do 2 separate things    
    if(useBranch):
        try:
            index = connections.index(value)
        except:
            index = np.nan
    else:
    # As I'm unsure as to how many times I'll have to run this, I'm
    # implementing a security measure that maintains the index if it's inputted
    # into the function multiple times
        try:
            index = pd.Index(pageData['id']).get_loc(value)
        except:
            index = value
            print('nope')
    # Returns the index of the page
    return index

# This function just compares 2 objects/values and returns NaN if they're the 
# same. This allows me to drop the NaNs after calling it. But doesn't outright
# delete the entry in case I want to do something interesting with them, like
# I did with the exit point analysis
def removeDuplicate(current, previous):
    if current == previous:
        return np.nan
    else:
        return current

# This function will look for a certain branch in the traversal and will return
# the location of all choices, and how many pages into the story the branch is
def checkBranch(branch):
    # First thing I'll do is get the connected nodes using the dictionary
    branches = graph[branch]
    # Get rid of the last 2 items as they are the exitStory and the
    # previously connected node. 
    if(branch != 0):
        branches = branches[:-1]
    
    # Gets the current node's location
    locations = [(pageData['Latitude'].iloc[branch],pageData['Longitude'].iloc[branch])]
    
    # Gets the following node's locations
    for i in branches:
        locations.append((pageData['Latitude'].iloc[i], pageData['Longitude'].iloc[i]))
    
    # The way that I have done this means that every element is it's own 
    # self contained location.
    
    # A separate array to hold the distances
    distance = []
    
    
    for i in range(len(locations)):
        # Long, but easy line to understand. It accesses the current branch and
        # the branches connected to it and then it compares the coordinates 
        # using the haversine formula get the distance between the 2.
        distance.append(haversine(locations[0][0], locations[0][1], locations[i][0], locations[i][1]))
    
    # Gets rid of the first element which is always 0 as it's the distance
    # between the current node and the current node.
    distance = distance[1:]
    

    # Gets the nodes between the root and the current node
    Nodes = getBackTrack(branch, end=0)
    # returns a tuple that holds the distances between the current node
    # and the consequent nodes (branches), the nodes that have come before this 
    # one and the number of nodes that have come before this. 
    return distance, branches, Nodes, len(Nodes)


# This function returns the nodes in between the root node and the
# node specified. It can save the path to a separate variable     
def backTracking(Node, end=0, path=None):
    # This is where the fact that I included the previous node in the 
    # dictionary becomes useful. Instead of searching the entire tree for one 
    # path, I can just track the tree back until I reach 0.
    
    # Checks if the path is null
    if path != None:
        path.append(Node)
    # Escape Clause, which is important for a recursive function
    if(Node == end):
        # Starts to go back up the stack when returns
        return Node
    else:
        #calls itself if the end hasn't been reached
        backTracking(graph[Node][-1])
 
    
# Calls the recursive function and returns the path between the 2 nodes
def getBackTrack(start, end):
    # Defines local list
    path = []
    # Calls the function passing the local list as path
    backTracking(start, end, path)
    # Returns the local list
    return path


# converts the list to a string with delinearators
def toStringAnalysis(value):
    # converts the list to a string
    listToStr = ' '.join(map(str, value))
    # converts the spaces to hypens
    listToStr = re.sub(r'\ ', r'-', listToStr)
    listToStr = "-"+listToStr+"-"
    return(listToStr)


# Recursive function to find path
def shortestDistance(start, end, path=None):
    # This function is a poor man's version of Djikstra's algorithm. 
    # It doesn't find the shortest distance overall, but instead the shortest
    # distance from node to node.     
    
    # Checks if the path is null
    if path != None:
        path.append(start)
    
  
    # Escape Clause
    if start == end:
        return
    
    # Gets the branch information and sets the value to beat to the first
    # index
    branches = checkBranch(start)
    lowest = branches[0][0]
    
    # Iterates through the branch information
    for i in branches[0]:
    # If the current item is less than the current lowest value, and the index
    # is lower than the current branch, it then becomes the new lowest value
       if i < lowest and branches[1][branches[0].index(i)] > start:
            lowest = i
    
    # It then calls itself with the start being the node closest to the 
    # current node and the end and path variables being maintained
    shortestDistance(branches[1][branches[0].index(lowest)], end, path)

    
# Uses the shortestDistance function to return a list of nodes
def findShortDist(start, end):
    # Local list to hold path
    path = []
    # Calls function, passing local variable as path
    shortestDistance(start, end, path)
    # Returns the local list
    return path
        

# This takes in multiple arguments to split up the pattern in differing
# sizes, with offset. Reverse is to check for patterns of back. Offset is
# so that you can do another round of splitting, but by offsetting the slices
# to check for slighly different patterns
def splitUpPath(path, segmentSize, reverse= False, withOffset = False, offset = 0):
    segments = []
    numSeg = 0
    reversedPath = path[::-1]
    # First pass is the regular splitting without offset and isn't reversed
    # The maths was simple. Number of segments so far * the segment size for 
    # index for the start of the slice and add the segment size for the end of 
    # slice
    for i in range(len(path)):
        if (i % segmentSize == 0):
            segments.append(path[numSeg * segmentSize : numSeg * segmentSize + segmentSize ])
            numSeg += 1
            
    # Second pass is the same except, it uses the offset to alter the slice 
    #values
    if(offset):
        numSeg = 0
        for i in range(len(path)):
            if i % segmentSize == 0:
                segments.append(path[(numSeg * segmentSize + offset) : (numSeg * segmentSize + segmentSize +offset)])
                numSeg += 1
    # This uses the reversed path variable and does exactly the same thing as
    # the first pass
    if(reverse):
        numSeg = 0
        for i in range(len(reversedPath)):
            if i % segmentSize == 0:
                segments.append(reversedPath[numSeg * segmentSize : numSeg * segmentSize + segmentSize ])
                numSeg += 1
                
    # This gets rid of all of the segments that have only one element
    # ie, they only contain a page.
    sortedSegments = [x for x in segments if len(x)>1]
    return sortedSegments


#I input the pattern to look for and the location to look for the pattern in
def lookForPattern(pattern, inputString):
    # Converts the pattern from a list/array to a string
    formatPattern = ' '.join(map(str, pattern))
    # Substitutes the spaces with hyphens
    formatPattern = re.sub(r'\ ', r'-', formatPattern)
    # Adds in hypens at beginning and end of string
    formatPattern = "-"+formatPattern+"-"
    # Looks for the pattern in the inputString
    matches = re.findall(formatPattern, inputString)
    # Returns all matches found
    return matches


# This checks if the pattern has branch inside. I used this to check if the 
# pattern had any choice.
def patternHasBranch(value):
    # Converts the pattern to a list
    integers = patternToList(value)
    # Initialises the local bool
    hasBranch = False
    # Iterates through the pattern
    for i in integers:
        # Simply checks if any of the integers are a valid branch and aren't
        # the last integer in the pattern. Ie the pattern doesn't end on
        # a branch in the story and has a valid choice to analyse
        if ((i in validBranchesIndex) and (i != integers[-1])):
            # Sets the local bool and breaks out of the loop to prevent
            # it being overwritten
            hasBranch = True
            break
    # Returns the local bool
    return hasBranch


# This retrieves the number of users at each node in a pattern
def getUsersAtEachNode(value):
    # Converts the pattern to a list
    integers = patternToList(value)
    # Local list
    numUsers = []
    # Iterates through the integers
    for i in integers:
        # Retrieves the number of users at each node 
        currentNodeUsers = indices[i].getNumUsers()
        # Appends that variable to the local list
        numUsers.append(currentNodeUsers)
    # Returns local list
    return numUsers
     
# This converts the string back into a list   
def patternToList(pattern, endPieces = False):
    # Firstly it determines if the end pieces should be included in the
    # conversion
    if endPieces:
        value = pattern
    else:
        value = pattern[1:-1]
    # It then splits the pattern based on the hypen, then converts
    # them to an integer as otherwise they'd still be strings
    integers = [int(x) for x in value.split('-')]
    # Returns the list of integers
    return integers


# This converts the number back into a page name
def patternToName(value):
    # Converts the pattern to a list of integers
    integers = patternToList(value)
    # List to hold the page names
    names = []
    # Iterates through the integers list
    for i in integers:
        # Appends the page name using the integer used in the iterator
        names.append(pageData.iloc[i, pageData.columns.get_loc("name")])
    # Returns the list of page names
    return names

def convertstr(string):
    # This function converts the string, that some columns comes in, to a
    # list so I can access the items within it
    
    # Removes the square brackets
    reformat = re.sub(r'\[', r'', string)
    reformat = re.sub(r'\]', r'', reformat)
    # Splits it into a list using the commas
    reformat = reformat.split(',')
    integers = []
    # Iterates through the new list of strings and converts them to
    # integers or floats.
    for i in reformat:
        # As I don't know which numeric format the data is going to come in
        # as, I have prepared for both.
        try:
            integers.append(int(i))
        except:
            integers.append(float(i))
    # Returns the list
    return integers

# This function will return the pages that are the shortest distance away
# from their previous one. It is different to the other shortest distance
# function I have implemented as this one will ignore choices that have
# identical distances. This is mainly to catch choices that don't require you
# to move for the choice, ergo the distance isn't relevant and shouldn't be
# considered in these situations
def shortestNodes():
    validNodes = []
    # Iterates through the valid branches and retrieves the nodes
    # distances and the frequency
    for i in validBranchesIndex:
        result = indices[i].getBranchResult()
        # Ignores 0 as it's irrelevant in this context
        if i == 0:
            continue
        # Gets the distances minus the last one
        locations = result[1][:-1]
        # Iterates through the locations
        for j in range(len(locations)-1):
            # Checks for duplicated data
            if locations[j] != locations[j + 1] or locations[j] != locations[j - 1]:
                # Saves the valid distance to local variable
                validDistance = locations[j]
                # Saves the node itself to a local variable
                node = result[0][j]
                # Appends the local variables to another local variable
                validNodes.append([node, validDistance])
    # I now know the nodes that were closest to the branch. Now I need to 
    # backtrack to the previous node and retrieve the possible branches
    # and then see how many chose these nodes
                
    # As they may have more then one previous node, I'll need to iterate 
    # over all of them. Luckiuly previous nodes are always less in index than
    # the current node
         
            
    # Iterates through the local variable
    for i in range(len(validNodes)):
        # Saves the node in question to a local variable
        index = validNodes[i][0]
        # Iterates through the node's connections
        for k in graph[index]:
            # If the connection is forward then it is disregarded
            if k > index:
                continue
            # Only interested in the connections backwards
            elif k < index:
                # Saves the relevant variables
                freq = indices[k].getBranchResult()[2]
                options = indices[k].getBranchResult()[0]
                validNodes[i].append(k)
                validNodes[i].append(freq[:-1])
                validNodes[i].append(options[:-1])

    # validNodes format = shortestNode, distance, root of choice, frequency of 
    # choice and finally the branches of that choice
    return validNodes
                

def getProportion(closestNode, freq, branches):
    # gets the index of the node in the branch list
    index = branches.index(closestNode)
    closest = 0
    furthest = 0
    # iterates through the frequency list
    for i in range (len(freq)):
        # checks if the current index is the same as the one for the 
        # closest node
        if i == index:
            closest += freq[i]
        else:
            furthest += freq[i]
    # returns both as they are both relevant results
    return closest, furthest


    
#%%


# This cell is for setting up the choice analysis, by saving relevant branch
# information as an array 

# Initialises the graph
graph = initial_graph()

# Empty list to store the connections between nodes
connections = []
# Iterates through the graph
for i in range(len(graph)):
    nodeConnect = []
    # Iterates through the nodes connected to the current node
    for j in graph[i]:
        # Checks if the nodes are the branches connected to it and aren't 
        # the exit story node
        if(j > i) and (j != 78):
            # Appends them to the variable in use for storing the current
            # node's connections
            nodeConnect.append(j)
    # Once it has finished iterating through all of the current node's 
    # connections, it saves them as a single element to the main global
    # variable
    connections.append(nodeConnect)

# As every node is connected to the exit story node, every node that has 
# at least 2 connections is a branch. So all I need to do
# is iterate through this new nested list and find the ones with at least 2
# connections. As the ones with only 1 isn't a branch
validBranches = [x for x in connections if len(x)>=2]

# Iterates through this new list to get the indices for the branches
validBranchesIndex = []
for i in validBranches:
    index = (getIndex(i, useBranch=True))
    # If there are any nodes that have identical connections, then they should
    # comes straight after one another, so tall I need to do is add one to the
    # index to get the one after the retrieved index
    if index in validBranchesIndex:
        index += 1
    # Again it appends it to a global variable
    validBranchesIndex.append(index)

# Now that I have a variable holding the branches in the story and a variable
# to compare them to, in order to find the index, as well as a variable to
# hold those indices, I can now start working on gaining some data contributed 
# to each branch and see what sort of patterns emerge from the users.

#%%

# This returns the user's page's visited as a list attached to each user

# It converts the pageId to the format required to traverse the graph
data['newPageId'] = data['pageId'].apply(lambda x: getIndex(x))
# It then saves these pages in a list for each user. This allows me to see
# the choices people made really easily.
dataList = data.groupby('user')['newPageId'].apply(list)
# Converts the list to a string able to be analysed
patterns = dataList.apply(lambda x: toStringAnalysis(x))
#Holds the indices for the branches class in a list
branchIndices = []
# Holds the indices for the entire graph
indices = []
# Iterates through all of the branches indices
for i in validBranchesIndex:
    branchIndices.append(indexChoice(i))
# Initialises the indices list
for i in connections:
    indices.append(indexChoice(getIndex(i, useBranch=True)))
    
#%%

# This cell applies the above code to make a dataframe to be displayed

branchDF = pd.DataFrame(validBranchesIndex)
branchDF.columns = ['branchIndex']
# Adds the relevant columns to the dataframe and retrieves the values for them
branchDF['Branches'] = branchDF['branchIndex'].apply(lambda x: indices[x].getBranchResult()[0])
branchDF['Distances'] = branchDF['branchIndex'].apply(lambda x: indices[x].getBranchResult()[1])
branchDF['Frequency'] = branchDF['branchIndex'].apply(lambda x: indices[x].getBranchResult()[2])
# Saves it to a csv for further use
branchDF.to_csv('BranchAnalysis.csv')

#%%

# This cell looks for specific patterns in the patterns variable


# Finds the shortest journey from one node to the next. In this case, from
# one major branch to the end of the story
byronPath = findShortDist(1, 18)
print("\n")
print(byronPath)
percyPath= findShortDist(19, 34)
print("\n")
print(percyPath)
maryPath = findShortDist(35, 54)
print("\n")
print(maryPath)
johnPath = findShortDist(55, 73)
print("\n")
print(johnPath)
print('Finished Generated Paths')

print(indices[0].getBranchResult())
#%%
visitedList = []
print('Start Traversal')


# Function that goes through the entire graph and retrieves all the paths
# that could be taken
def depthFirst(graph, currentVertex, visited):
    # Appends the current vertex to the list
    visited.append(currentVertex)
    # As 0 is a unique case, it requires a unique condition
    if currentVertex == 0:
        # Iterates through the connections of that vertex and checks if 
        # it is not already been visited
        for vertex in graph[currentVertex]:
            if vertex not in visited:
                # If it is a new vertex, it will call itself and create
                # a copy of the visited list. This is how it retrieves all 
                # possible paths
                depthFirst(graph, vertex, visited.copy())
    else:
        for vertex in graph[currentVertex][:-2]:
            if vertex not in visited:
                depthFirst(graph, vertex, visited.copy())
    visitedList.append(visited)
    

depthFirst(graph, 0, [])


#%%

validNodes = shortestNodes()

df5 = pd.DataFrame(validNodes)
# This will require minor alterations. When there are 2 identical nodes with different
# root nodes, move one of the copied values added by the shortestNodes function
# into the appropriate column. If I have more time, I'l dedicate it to making 
# this process more automated. It's the lowest numbered index first
# ie in this case, it goes 23-20 then 23-21
# 
#df5.to_csv('locationBasedChoice.csv')
#%%


# Appends them to a list
pathsToCheck = [byronPath, percyPath, maryPath, johnPath]

# New list to store the paths generated
newPaths = []
# Iterates through the range of the average length of a story line
for k in range(17):
    # Iterates through all of the paths generated so far
    for i in pathsToCheck:
        # Splits up the path using the iteration values to dynamically change
        # the values generated
        newPaths += splitUpPath(i, (k+1), reverse=True, withOffset = True, offset = 1)

# Adds the original paths so that they can be used in the choice analysis
newPaths += pathsToCheck
newPaths += visitedList
# A new list to store the paths to look for
toLook = []
# Bit of cleanup to reduce time and resources required to run. It removes
# duplicate paths and stores the valid paths to the toLook list
for i in newPaths:
    if i in toLook:
        continue
    else:
        toLook.append(i)
      
# List to store the matches to the paths to look for
match = []

# Iterates through the user patterns
for i in patterns:
    # Iterates through the paths to look for
    for j in toLook:
        # Calls the function to format and look for patterns and then return
        # the matches it found
        result = lookForPattern(j, i)
        # Appends the matches if the result is valid, otherwise I would
        # end up with a lot on blank elements on my list
        if result != None:
            match += result
            

# Converts the list to a data frame
allMatches = pd.DataFrame(match)
allMatches.columns = ['pattern']
# This counts how many users matched a certain pattern
allMatches = allMatches.groupby('pattern')['pattern'].count().rename('NumUsersMatchPattern').reset_index()

# Filter to get rid of frequency less than a threshold value to 
# only hold the patterns that occured the most often as these are the ones
# that I am interested in
freqFilter = allMatches["NumUsersMatchPattern"] >= 2
aboveThreshold = allMatches[freqFilter]

# Filters out the patterns without any choice
aboveThreshold = aboveThreshold[aboveThreshold['pattern'].apply(lambda x: patternHasBranch(x))]
# Gets the number of users at each node in total
aboveThreshold['NumUsersAtEachNode'] = aboveThreshold['pattern'].apply(lambda x : getUsersAtEachNode(x))
# Sorts the DataFrame by the frequency
aboveThreshold = aboveThreshold.sort_values('NumUsersMatchPattern', ascending=False)
# Adds the page names to the pattern
aboveThreshold['NamedPattern'] = aboveThreshold['pattern'].apply(lambda x : patternToName(x))
# Reorganises the DataFrame 
aboveThreshold = aboveThreshold[['pattern', 'NamedPattern', 'NumUsersMatchPattern', 'NumUsersAtEachNode']]
# Saves it to a csv
aboveThreshold.to_csv('ChoiceAnalysis.csv')

#%%

# Retrieves the dataframe from further up, but as it needed manual altering, this 
# is required
locationBasedChoice = pd.read_csv("locationBasedChoice.csv")
locationBasedChoice = locationBasedChoice.rename(columns={'0': 'ClosestChoice', '2': 'RootNode', '1': 'DistanceFromRoot' , '4': 'RootBranches', '3': 'RootBranchFrequency'})
math = locationBasedChoice
math['RootBranches'] = math['RootBranches'].apply(lambda x: convertstr(x))
math['RootBranchFrequency'] = math['RootBranchFrequency'].apply(lambda x: convertstr(x))

    
math['proportions'] = math.apply(lambda x: getProportion(x.ClosestChoice, x.RootBranchFrequency, x.RootBranches), axis =1)

# Converts it to a list of tuples
proportions = math['proportions'].tolist()
closest = 0
furthest = 0
for i in proportions:
    # As it's a tuple, I can access specific parts of it
    # and I know where the closest and furthest numbers are
    closest += i[0]
    furthest += i[1]

# This saves another tuple with total number of users who 
# went certain ways and total percentage of instances of users
# going the shorter way
percentageClosest = closest, furthest, (closest/(closest+furthest))

#%% 
from statistics import mean
import numpy
# This cell is for exploring the correlation relative distance and proportion
# of choice. To do this, I will need to get the relative distance between each
# node and also the proportion of the choice for each branch. 

# First I will get all the branches and their distance from the root
# then find their relative distance and the frequency they were visited
# then find the correlation

choiceDistDF = locationBasedChoice[['RootNode','RootBranchFrequency' ,'RootBranches']]
choiceDistDF['Distances'] = choiceDistDF['RootNode'].apply(lambda x: checkBranch(x)[0][:-1])

# Relative distance = average distance from root to brances - distance from branch to node

choiceDistDF['AverageDistance'] = choiceDistDF.apply(lambda x: mean(x.Distances), axis = 1)

def relativeDistance(average, points):
    relativeDistances = []
    for i in points:
        relativeDistances.append(round(i - average, 2))
    return relativeDistances

choiceDistDF['RelativeDistance'] = choiceDistDF.apply(lambda x: relativeDistance(x.AverageDistance, x.Distances), axis=1)

choiceDist = choiceDistDF[['RootBranchFrequency', 'RelativeDistance']]

#choiceDist['RootBranchFrequency'] = choiceDist['RootBranchFrequency'].apply(lambda x: convertstr(x))

freq = choiceDist['RootBranchFrequency'].tolist()
proportions = []
for i in freq:
    entire = sum(i)
    for j in i:
        proportions.append(round(j/entire,3))

    
    

relDist = choiceDist['RelativeDistance'].tolist()
rel2 = []
for i in relDist:
    for j in i:
        rel2.append(j)

choiceDist = pd.DataFrame(proportions, rel2[:-1]).reset_index().rename(columns={'index': 'Relative Distance', 0: 'Proportion'})
                                                                 
print(choiceDist.corr())
print(stats.pearsonr(proportions, rel2[:-1]))

#%%

# This cell will format the dataframes for analysis in R
# More specifically, it will do the following:
#   - Get the pages after the exit page as this might be the contributing
#   factor for users exiting
exitPoints['Frequency'] = exitPoints['pageId']
# Counts frequency of exit at each Page Id
branchGrp = exitPoints.groupby('pageId').count()
# Returns it as a dataframe
branchGrp = branchGrp.reset_index()
# Gets the branches
branchGrp['ExitBranches'] = branchGrp.apply(lambda x: checkBranch(getIndex(x.pageId))[1], axis=1)
# Gets the latitude
branchGrp['Latitude'] = branchGrp['pageId'].map(ctin.sh.pageData.set_index('id')['Latitude'])
# Gets the longitude
branchGrp['Longitude'] = branchGrp['pageId'].map(ctin.sh.pageData.set_index('id')['Longitude'])
branchGrp.to_csv('ExitPointBranchs.csv')
#

#This is necessary for later on in the code, but doesn't need to be exported



#%%


# This cell will format dataframes for use in making graphs

# First one is data for use in a heat map

exitExclusion = ["893861b0-fa80-483e-ed94-e405e91ee0b6",
             "5a428f8b-173c-4d48-ce72-b1d137234d5d",
             "8bf230cc-42fa-4cd2-3eb9-d16480cd7094",
             "f17e55aa-28d2-4596-3a3b-f4160fec8c37",
             "1ed5a659-7032-41cf-03e9-82effaf98552",
            ]



checkerFilter = branchGrp[~branchGrp['pageId'].isin(exitExclusion)]
exitPointHeatMap = checkerFilter[['Latitude', 'Longitude', 'Frequency']]
exitPointHeatMap.to_csv("exitPointHeatMapData.csv", index=False)


#%%
# Next is formatting the graph to generate the routes between nodes

# To do this, I will iterate through the keys and add them as a tuple containing
# the root and the destination node's latitiude and longitude coordinates
# I'll then save this as a dataframe as a csv for use in R

routes = []
for i in range(len(graph)):
    for j in graph[i]:
        valid = False
        rootLat = pageData.iloc[i,8]
        rootLon = pageData.iloc[i,9]
        desLat = pageData.iloc[j,8]
        desLon = pageData.iloc[j,9]
        tag = pageData.iloc[j, 10]
        if desLat != np.nan and desLon != np.nan:
            if rootLat != np.nan and rootLon != np.nan:
                routes.append((rootLat, rootLon, desLat, desLon, tag))

routesDF = pd.DataFrame(routes).rename(columns={0: "RootLat", 1: "RootLon", 2: "DestinationLat", 3: "DestinationLon", 4: "Index"})
routesDF = routesDF.dropna()
routesDF.to_csv("Routes.csv")

# Second one is for exit branches. It holds the branches from the exit points
# to analyse if these choices were a contributing factor towards users exiting
# on that branch

exitBranches = []
for i in branchGrp['ExitBranches'].tolist():
    for j in i:
        exitBranches.append(j)
      
def getLocationAtIndex(index, Lon=False):  
    # Gets the right coordinate for the right node
    if Lon:
        Lon = pageData.iloc[index,9]
        return Lon
    else:
        Lat = pageData.iloc[index,8]
        return Lat
    
                
                
test = pd.DataFrame(exitBranches)
exitBranchesDF = test[0].value_counts().reset_index().rename(columns = {'index': 'exitBranchIndex', 0: 'Frequency'})
exitBranchesDF['Lat'] = exitBranchesDF['exitBranchIndex'].apply(lambda x:getLocationAtIndex(x))
exitBranchesDF['Lon'] = exitBranchesDF['exitBranchIndex'].apply(lambda x:getLocationAtIndex(x, Lon=True))
exitBranchesDF = exitBranchesDF.dropna()

def getBaseRoots(value):
    branches = graph[value]
    roots = []
    for i in branches:
        if i > value:
            continue
        else:
            roots.append(i)
    return roots

exitBranchesDF['BaseRoot'] = exitBranchesDF['exitBranchIndex'].apply(lambda x : getBaseRoots(x))
branches = []


#exitBranchesDF['BaseRootLat'] = exitBranchesDF['BaseRoot'].apply(lambda x:getLocationAtIndex(x))
#exitBranchesDF['BaseRootLon'] = exitBranchesDF['BaseRoot'].apply(lambda x:getLocationAtIndex(x, Lon=True))
#exitBranchesDF.to_csv('ExitBranchesWLocations.csv')


# Third one is just for the branches and their options. 
branches = []
for i in branchDF['branchIndex']:
    for j in graph[int(i)]:
        if j > i and j != 78:
            rootLat = pageData.iloc[i,8]
            rootLon = pageData.iloc[i,9]
            desLat = pageData.iloc[j,8]
            desLon = pageData.iloc[j,9]
            tag = pageData.iloc[j, 10]

            if desLat != np.nan and desLon != np.nan:
                if rootLat != np.nan and rootLon != np.nan:
                    branches.append((rootLat, rootLon, desLat, desLon, tag, i, j))

branchesDF = pd.DataFrame(branches).rename(columns={0: "RootLat", 1: "RootLon", 2: 'DesLat', 3: "DesLon", 4: "Tag", 5: "RootIndex", 6: "DesIndex"}).dropna()

branchesDF.to_csv('BranchesWOptionsLocation.csv')

# Filters out all of the mandatory choices and leaves only the choices 
branchFilter = ctin.sh.pageData['OriginalIndex'].isin(branchesDF['DesIndex'])
heatmapData = ctin.sh.pageData[branchFilter][['Latitude', 'Longitude', 'Frequency']]
heatmapData.to_csv("heatMapData.csv")


#%% 

# This is for finding out the distance between branches and the branch root
# ie find out if the user has to backtrack

# This is iterates through all the valid branches and finds their root
# and adds to an array with their branches
pairs = []
for i in exitBranchesDF['exitBranchIndex']:
    for j in graph[i]:
        if j != 78 and j < i:
                for k in graph[i]:
                    if k != 78 and j!= k:
                        index = pd.Index(exitBranchesDF['exitBranchIndex']).get_loc(i)
                        exitFreq = exitBranchesDF.iloc[index, 1]
                        branchFreq = pageData.iloc[k, 12]
                        rootFreq = pageData.iloc[i, 12]
                        baseRootFreq = pageData.iloc[j,12]
                        pairs.append([j,k,i, exitFreq, rootFreq, branchFreq, baseRootFreq])
        
        
        
#%%
                        
def getChoiceProportion(num, deno):
    return num/deno

# What I'm looking at here is if the distance between the base root node and 
# the branches affect exit points
    
# What I mean by base root is best put like this:
    # A -> B -> C
    #        -> D

# I'm looking at the distance between A->C and A->D as this will let me know
# if the player is back tracking. 
# A in this case is the base root node
# B would be the root node
# C and D would be the branches

exitPointPairsDF = pd.DataFrame(pairs).rename(columns={0:"BaseRoot", 1:"Branch", 2: 'Root', 3:"FrequencyExited", 4: "RootFreq", 5: "BranchFreq", 6: "BaseRootFreq"})
exitPointPairsDF['BaseRootLat'] = exitPointPairsDF['BaseRoot'].apply(lambda x:getLocationAtIndex(x))
exitPointPairsDF['BaseRootLon'] = exitPointPairsDF['BaseRoot'].apply(lambda x:getLocationAtIndex(x, Lon=True))
exitPointPairsDF['BranchLat'] = exitPointPairsDF['Branch'].apply(lambda x:getLocationAtIndex(x))
exitPointPairsDF['BranchLon'] = exitPointPairsDF['Branch'].apply(lambda x:getLocationAtIndex(x, Lon=True))
exitPointPairsDF['Distance'] = exitPointPairsDF.apply(lambda x: haversine(x.BaseRootLat, x.BaseRootLon, x.BranchLat, x.BranchLon), axis=1)

# ProportionExited is calculated by getting the number of people at the 
# root node and the number of people who exited at the root node
exitPointPairsDF['ProportionExited'] = exitPointPairsDF.apply(lambda x: getChoiceProportion(x.FrequencyExited, x.RootFreq), axis=1)

# ProportionPerBranch is calculated by getting the number of people
# at each branch and dividing them by the number of people at the root node
exitPointPairsDF['ProportionPerBranch'] = exitPointPairsDF.apply(lambda x: getChoiceProportion(x.BranchFreq, x.RootFreq), axis=1)
# A proportion of higher than 1 could be explained by a merging of storylines
# at a node, therefore more people would be able to access it compared to
# a node in a mirrorworld hypertext pattern for example.

exitPointPairsDF = exitPointPairsDF.dropna()
print(orctin.organiseDescribe(exitPointPairsDF['Distance'].describe()))
print(stats.pearsonr(exitPointPairsDF['Distance'],exitPointPairsDF['ProportionExited']))
exitPointPairsDF.to_csv("ExitPoints_CheckBackTrack.csv")

#%% 

# Generate a table to convert page index to page id to page name

pageLookUp = pageData[['id', 'name']].reset_index()

pageLookUp.to_csv("PageLookUp.csv")