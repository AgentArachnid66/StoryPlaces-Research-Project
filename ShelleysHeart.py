# -*- coding: utf-8 -*-

import pandas as pd
from pandas.io.json import json_normalize
import json
import re
import numpy as np

# Opens the data set and loads it in as JSON data
with open("Dataset/sh(1).json") as json_data:
    data = json.load(json_data)
    
# Normalises the json to separate DataFrames
functionData = pd.json_normalize(data['functions'])

locationData = pd.json_normalize(data['locations'])

conditionsData = pd.json_normalize(data['conditions'])

# Function to remove the brackers around a value
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

# Loads in the page data as JSON data
with open("Dataset/pageData.json") as json_data:
    pageData = json.load(json_data)
    

# I had to manually add back the JSON that wouldn't normalise as part of 
# of the original data set. If the same occurs, just append this variable to 
# the data set and remove the duplicates
missingJSON = \
    [
    {
		"id": "893861b0-fa80-483e-ed94-e405e91ee0b6",
		"content": "<p>Turn on cellular data<br/>View in horizontal mode (phone sideways)<br/>Used headphones for optimal 360-degree audio<br/>Approach red markers, when they turn green, unlock scene.<br/>If 2 or more markers appear, walk to the option that sounds most interesting.</p><br/><p>TROUBLE SHOOTING:<br/>If GPS is sluggish, refresh<br/>If marker wonâ€™t turn green, select 'advanced' and click 'demo mode'.<br/></p><br/><p>Secret Scenes: each story-path contains at least one secret scene. These can only be revealed by exploring other paths and making different choices. Happy hunting!</p><p>To get started, click on the markers to find the path you want to follow.</p><img src='http://nht.ecs.soton.ac.uk/misc/sh-donotdelete.png'/>",
		"name": "INSTRUCTIONS",
		"pageTransition": "next",
		"hint": {
			"locations": [],
			"direction": ""
		},
		"functions": [
			"page-read-893861b0-fa80-483e-ed94-e405e91ee0b6",
			"chapter-chain-function-94d1e0f3-30de-4e6d-e5c4-98e98724170c",
			"chapter-chain-function-f26bde04-5aa3-4706-835f-785f7a431699",
			"adv-94cc8c22-97e8-42b5-43a6-7430c9dc9c04",
			"adv-563f0928-f63b-406c-04cd-1e39a39154df",
			"adv-5623df20-d2f7-4e54-e47b-49005da9bd0e",
			"adv-84a41f89-b5e0-4bb6-c432-d028b3bedc14"
		],
		"conditions": [
			"page-not-read-893861b0-fa80-483e-ed94-e405e91ee0b6"
		]
	},	{
		"id": "81c5c751-857b-488a-d88f-fda3d4413bfe",
		"content": "<a style=\"background-color: #80ac7b; color: #f7f7f7; padding: 4px; border-radius: 4px;font-size: 40px;\" href=\"https://cemp.ac.uk/projects/Shelleys_heart/john/9b/index.html\" target=\"_blank\">Start Scene</a>",
		"name": "9B Expose",
		"pageTransition": "next",
		"hint": {
			"locations": [
				"adv-06469e92-5c62-4671-73fa-41590d4086ce"
			],
			"direction": "far southwest corner of churchyard"
		},
		"functions": [
			"page-read-81c5c751-857b-488a-d88f-fda3d4413bfe",
			"chapter-chain-function-c1a6eb3c-5906-4635-5c09-b21d3f4a5807"
		],
		"conditions": [
			"page-chapters-81c5c751-857b-488a-d88f-fda3d4413bfe",
			"page-unlocked-81c5c751-857b-488a-d88f-fda3d4413bfe",
			"adv-95408e97-50a5-4eb1-6d65-c75cf42e349b",
			"adv-613c918b-b901-4698-383d-6db79edff308"
		]
	},
	{
		"id": "1e4f4680-20d8-4df4-1828-00550dec362e",
		"content": "<a style=\"background-color: #80ac7b; color: #f7f7f7; padding: 4px; border-radius: 4px;font-size: 40px;\" href=\"https://cemp.ac.uk/projects/Shelleys_heart/john/10/index.html\" target=\"_blank\">Start Scene</a>",
		"name": "10. Depart",
		"pageTransition": "next",
		"hint": {
			"locations": [
				"adv-4add3116-63fa-47e3-e494-29939c3266e2"
			],
			"direction": "centre of churchyard"
		},
		"functions": [
			"page-read-1e4f4680-20d8-4df4-1828-00550dec362e",
			"chapter-chain-function-031e66b6-f741-4513-adb2-eeb332e20949"
		],
		"conditions": [
			"page-chapters-1e4f4680-20d8-4df4-1828-00550dec362e",
			"page-unlocked-1e4f4680-20d8-4df4-1828-00550dec362e",
			"adv-95408e97-50a5-4eb1-6d65-c75cf42e349b",
			"adv-0463f898-dd01-47ad-6713-961c494a706e"
		]
	},
	{
		"id": "bbc0da17-194b-473a-b865-c9efb8ae94f6",
		"content": "<p>Special thanks to St. Peter's Church for hosting the story world of Shelley's Heart, and thank you for exploring it! </p>\n",
		"name": "Thank You",
		"pageTransition": "next",
		"hint": {
			"locations": [],
			"direction": ""
		},
		"functions": [
			"page-read-bbc0da17-194b-473a-b865-c9efb8ae94f6",
			"chapter-chain-function-f26bde04-5aa3-4706-835f-785f7a431699"
		],
		"conditions": [
			"page-chapters-bbc0da17-194b-473a-b865-c9efb8ae94f6",
			"page-unlocked-bbc0da17-194b-473a-b865-c9efb8ae94f6",
			"adv-95408e97-50a5-4eb1-6d65-c75cf42e349b"
		]
	},
	{
		"id": "981468a4-d38f-4fd3-4b4c-dbb03637ef32",
		"content": "<p>Special thanks to St. Peter's Church for hosting the story world of Shelley's Heart, and thank you for exploring it! </p>\n",
		"name": "Thank You",
		"pageTransition": "next",
		"hint": {
			"locations": [],
			"direction": ""
		},
		"functions": [
			"page-read-981468a4-d38f-4fd3-4b4c-dbb03637ef32",
			"chapter-chain-function-f26bde04-5aa3-4706-835f-785f7a431699"
		],
		"conditions": [
			"page-chapters-981468a4-d38f-4fd3-4b4c-dbb03637ef32",
			"page-unlocked-981468a4-d38f-4fd3-4b4c-dbb03637ef32",
			"adv-ed1b177a-05fd-4cfb-149a-50d3a483c77e"
		]
	},
	{
		"id": "3bfc772a-2257-4244-3e75-51c181bee1a9",
		"content": "<p>Special thanks to St. Peter's Church for hosting the story world of Shelley's Heart, and thank you for exploring it!</p>\n",
		"name": "Thank You",
		"pageTransition": "next",
		"hint": {
			"locations": [],
			"direction": ""
		},
		"functions": [
			"page-read-3bfc772a-2257-4244-3e75-51c181bee1a9",
			"chapter-chain-function-f26bde04-5aa3-4706-835f-785f7a431699"
		],
		"conditions": [
			"page-chapters-3bfc772a-2257-4244-3e75-51c181bee1a9",
			"page-unlocked-3bfc772a-2257-4244-3e75-51c181bee1a9",
			"adv-bed1c996-e8d0-48d9-ccb1-c8293f4f7331"
		]
	},
	{
		"id": "dafd6c3f-9bed-4879-d90b-20001528504b",
		"content": "<p>Special thanks to St. Peter's Church for hosting the story world of Shelley's Heart, and thank you for exploring it!</p>\n",
		"name": "Thank You",
		"pageTransition": "next",
		"hint": {
			"locations": [],
			"direction": ""
		},
		"functions": [
			"page-read-dafd6c3f-9bed-4879-d90b-20001528504b",
			"chapter-chain-function-f26bde04-5aa3-4706-835f-785f7a431699"
		],
		"conditions": [
			"page-chapters-dafd6c3f-9bed-4879-d90b-20001528504b",
			"page-unlocked-dafd6c3f-9bed-4879-d90b-20001528504b",
			"adv-4d7b4ab2-c272-4daf-2540-5094b77a6474"
		]
	},
	{
		"id": "47480a57-3aee-4176-c171-7a02b2572a57",
		"content": "<p>Thank you for your time, we hope you enjoyed Shelley's Heart.</p>\n",
		"name": "Exit Story",
		"pageTransition": "end",
		"hint": {
			"locations": [],
			"direction": ""
		},
		"functions": [
			"page-read-47480a57-3aee-4176-c171-7a02b2572a57"
		],
		"conditions": [
			"page-not-read-47480a57-3aee-4176-c171-7a02b2572a57",
			"page-unlocked-47480a57-3aee-4176-c171-7a02b2572a57"
		]
	}
    ]

    
# Normalizes the main data set, which seemed to fix the above bug
pageData = json_normalize(pageData)

# Adds in the hint locations to the page Data so I can link the actual
# locations to it
pageData['hint.locations'] = pageData['hint.locations'].apply(lambda x:remove_brackets(x))
# Using the hint locations as a key, I can map the lat/lon coordinates
# to each page
pageData['Latitude'] = pageData['hint.locations'].map(locationData.set_index('id')['lat'])
pageData['Longitude'] = pageData['hint.locations'].map(locationData.set_index('id')['lon'])

# Function to calculate distane between 2 lat/lon coordinates
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


