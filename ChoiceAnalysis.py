# -*- coding: utf-8 -*-
import pandas as pd
import CTINDeepReaderClassification as ctin
import CTINResearch as orctin
import re

data = orctin.validPages

pageData = ctin.sh.pageData

#%%

# This cell holds all the functions required for the choice analysis

import numpy as np
from ShelleysHeart import haversine as haversine

# Initialses the list for use in the recursive function
Nodes = []

pageData['Frequency'] = pageData['id'].map(orctin.pageFreq.set_index('pageId')['pageFreq'])

# Class that holds the index and can get the number of people that went to 
# certain choices and the distance to those choices
class indexChoice():
    
    def __init__(self, index):
        self.index = index
    
    def getChoices(self):
        return checkBranch(self.index)[1]
        
    def setIndex(self, newIndex):
        self.index = newIndex
    
    def getIndex(self):
        return self.index

    def getNumUsers(self):
        page = pageData['Frequency'].iloc[self.index]
        return page
    
    # Gets the connected nodes and the optionally the distances to those 
    # nodes.
    def getBranches(self, distance=False):
        if distance:
            branches = checkBranch(self.index)[:2]
        else:
            branches = checkBranch(self.index)[1]
        print(branches)

        # This is the last net to catch nodes that lead 
        # to this node. 
        for i in range(len(branches[1])):
            if branches[1][i] <= self.index:
                del branches[1][i]
                del branches[0][i]
       
        return branches
    
    # This function takes in the branch index and returns the number of people
    # who chose that route
    def getBranchResult(self):
        frequency = []
        branches = self.getBranches(distance=True)
        for i in branches[1]:
            indices[i].setIndex(i)
            frequency.append(indices[i].getNumUsers())
        
        distance, node = branches        
        return [node, distance, frequency]
                
# This function initialises the graphical representation of Shelley's Heart
def initial_graph():
    
    exitNode = [None] * 78
    for i in range (len(exitNode)):
        exitNode[i] = i
    
    
    # This dictinary holds of the page index in page data as a key and the 
    # connected node's index as a value. This should allow for relatively
    # easy traversion
        
    # The connection to the previous node is stored as it's last index on the 
    # value. I've also stored the connection to the exit story page as the 
    # second to last index.
        
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
    
    return index

# This function just compares 2 objects/values and returns NaN if they're the 
# same. This allows me to drop the NaNs after calling it.
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
    Nodes.clear()
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
        # compares the coordinates using the haversine formula get the 
        # distance between the 2.
        distance.append(haversine(locations[0][0], locations[0][1], locations[i][0], locations[i][1]))
    
    # Gets rid of the first element which is always 0 as it's the distance
    # between the current node and the current node.
    distance = distance[1:]
    
    backTracking(branch)
    
    # returns a tuple that holds the distances between the current node
    # and the consequent nodes, the nodes that have come before this one and
    # the number of nodes that have come before this. 
    return distance, branches, Nodes, len(Nodes)

# This function returns the nodes in between the root node and the
# node specified.     
def backTracking(Node, end=0):
    # This is where the fact that I included the previous node in the 
    # dictionary becomes useful. Instead of searching the entire tree for one 
    # path, I can just track the tree back until I reach 0.
    
    # Store the node to a global variable
    Nodes.append(Node)
    # Escape Clause, which is important for a recursive function
    if(Node == end):
        return Node
    else:
        backTracking(graph[Node][-1])


def toStringAnalysis(value):
    listToStr = ' '.join(map(str, value))
    listToStr = re.sub(r'\ ', r'-', listToStr)
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
    lowest= branches[0][0]
    
    # Iterates through the branch information
    for i in branches[0]:
    # If the current item is less than the current lowest value, and the index
    # is lower than the current branch, it then becomes the new lowest value
       if i <= lowest and branches[1][branches[0].index(i)] > start:
            lowest = i
        
    # It then calls itself with the start being the node closest to the 
    # current node and the end and path variables being maintained
    shortestDistance(branches[1][branches[0].index(lowest)], end, path)
        
# Uses the shortestDistance function to return a list of nodes
def findShortDist(start, end):
    path = []
    shortestDistance(start, end, path)
    return path
        

def splitUpPath(path, segmentSize, reverse= False, withOffset = False, offset = 0):
    segments = []
    numSeg = 0
    reversedPath = path[::-1]
    for i in range(len(path)):
        if (i % segmentSize == 0):
            segments.append(path[numSeg * segmentSize : numSeg * segmentSize + segmentSize ])
            numSeg += 1
            
    if(offset):
        numSeg = 0
        for i in range(len(path)):
            if i % segmentSize == 0:
                segments.append(path[(numSeg * segmentSize + offset) : (numSeg * segmentSize + segmentSize +offset)])
                numSeg += 1

    if(reverse):
        numSeg = 0
        for i in range(len(reversedPath)):
            if i % segmentSize == 0:
                segments.append(reversedPath[numSeg * segmentSize : numSeg * segmentSize + segmentSize ])
                numSeg += 1

    sortedSegments = [x for x in segments if len(x)>1]
    return sortedSegments


def lookForPattern(pattern, inputString):
    # Copy the code that converts the users pages to the same format
    formatPattern = ' '.join(map(str, pattern))
    formatPattern = re.sub(r'\ ', r'\-', formatPattern)
    matches = re.findall(formatPattern, str(inputString))
    return matches
    


#%%
# Initialises the graph
graph = initial_graph()

#%%

# This cell is for setting up the choice analysis, by saving relevant branch
# information as an array 

connections = []
for i in range(len(graph)):
    nodeConnect = []
    for j in graph[i]:
        if(j > i) and (j != 78):
            nodeConnect.append(j)
    connections.append(nodeConnect)

# As every node is connected to the exit story node, every node that has 
# at least 2 connections, excluding 78, is a branch. So all I need to do
# is iterate through this new nested list and find the ones with at least 3
# connections.
validBranches = [x for x in connections if len(x)>=2]

validBranchesIndex = []
for i in validBranches:
    index = (getIndex(i, useBranch=True))
    if index in validBranchesIndex:
        index += 1
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
# Adds the relevant columns to 

branchDF['Branches'] = branchDF['branchIndex'].apply(lambda x: indices[x].getBranchResult()[0])
branchDF['Distances'] = branchDF['branchIndex'].apply(lambda x: indices[x].getBranchResult()[1])
branchDF['Frequency'] = branchDF['branchIndex'].apply(lambda x: indices[x].getBranchResult()[2])

branchDF.to_csv('BranchAnalysis.csv')

#%%

# This cell looks for specific patterns in the patterns variable


# Finds the shortest journey from one node to the next. In this case, from
# one major branch to the end of the story
byronPath = findShortDist(1, 18)
percyPath= findShortDist(19, 34)
maryPath = findShortDist(35, 54)
johnPath = findShortDist(55, 73)

pathsToCheck = [byronPath, percyPath, maryPath, johnPath]

newPaths = []
for k in range(17):
    for i in pathsToCheck:
        newPaths += splitUpPath(i, (k+1), reverse=True, withOffset = True, offset = 1)

newPaths += pathsToCheck

toLook = []

for i in newPaths:
    if i in toLook:
        continue
    else:
        toLook.append(i)
        
match = []

for i in patterns:
    for j in toLook:
        result = lookForPattern(j, i)
        if result != None:
            match += result
            
match.sort()
       
def countChoices(listToCount):
    df = pd.DataFrame(listToCount)
    df.columns = ['pattern']
    df['NumPages'] = df['pattern'].apply(lambda x: stringToList(x))
    return df

def stringToList(value):
    toint = re.sub(r'-', r'\'\'\"\'', value)
    
    numericList = [toint]
    
    return numericList

    
df1 = countChoices(match)
