# -*- coding: utf-8 -*-

import pandas as pd
import json
import re
import numpy as np
import math

with open("Dataset/sh(1).json") as json_data:
    data = json.load(json_data)
    
functionData = pd.json_normalize(data['functions'])

locationData = pd.json_normalize(data['locations'])

def remove_brackets(value):
    value = str(value)
    value = re.sub(r'\'', r'', value)
    value = re.sub(r'\[', r'', value)
    value = re.sub(r'\]', r'', value)
    value = re.sub(r'\'',r'',value)
    if value == "":
        return np.nan
    else:
        return value



pageData = pd.json_normalize(data['pages'])

pageData['hint.locations'] = pageData['hint.locations'].apply(lambda x:remove_brackets(x))
pageData = pageData.dropna(subset=["hint.locations"])

#pageData['LocationId'] = locationData['id'].map(pageData['hint.locations'])
pageData['Latitude'] = pageData['hint.locations'].map(locationData.set_index('id')['lat'])
pageData['Longitude'] = pageData['hint.locations'].map(locationData.set_index('id')['lon'])

#print(pageData[['Latitude', 'Longitude']].head())



def haversine(lat1, lon1, lat2, lon2): 
   R =  6373000
   dlon = lon2 - lon1
   print(dlon)
   dlat = lat2 - lat1
   print(dlat)
   a = math.pow(math.sin(dlat/2),2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlon/2),2)
   print(a)
   c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) )
   print(c)
   d = R * c 
   return d


print(haversine(50.7203,-1.87599,50.7203, -1.87582))
S
conditionsData = pd.json_normalize(data['conditions'])