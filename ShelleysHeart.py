# -*- coding: utf-8 -*-

import pandas as pd
import json
import re
import numpy as np

with open("Dataset/shelleysheart-v5.json") as json_data:
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

pageData['Latitude'] = pageData['hint.locations'].map(locationData.set_index('id')['lat'])
pageData['Longitude'] = pageData['hint.locations'].map(locationData.set_index('id')['lon'])

def haversine(lat1, lon1, lat2, lon2):
    if(lat1, lon1, lat2, lon2) == np.nan:
        return np.nan
    r = 6371000
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
    res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
    return np.round(res, 2)
# credit to https://towardsdatascience.com/heres-how-to-calculate-distance-between-2-geolocations-in-python-93ecab5bbba4


conditionsData = pd.json_normalize(data['conditions'])