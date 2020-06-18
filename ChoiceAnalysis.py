# -*- coding: utf-8 -*-

import CTINDeepReaderClassification as ctin

#%%

# To analyse branches and choices, I first must have a way to process them.
#
# The first way that comes to mind is a matrix that holds each page and their 
# connections, but this would result in a lot of wasted space and memory.
# The alternative is an adjanceny list, which is what I'll use and store
# the distance between nodes using a dictionary format for each page

pathList = ["893861b0-fa80-483e-ed94-e405e91ee0b6"["5a428f8b-173c-4d48-ce72-b1d137234d5d", 
                                                   "1ed5a659-7032-41cf-03e9-82effaf98552", 
                                                   "f17e55aa-28d2-4596-3a3b-f4160fec8c37", 
                                                   "8bf230cc-42fa-4cd2-3eb9-d16480cd7094"], 
            ""]