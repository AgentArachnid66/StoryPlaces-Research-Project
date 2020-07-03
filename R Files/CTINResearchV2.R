# Gets the libraries required for the script
require(ggmap)
require(sf)
require(sp)
require(rgdal)
require(tidyverse)


# Google Cloud API Key
key <- "AIzaSyD5B3reqaxwM3PXkuYnWY_vtwNZmzETgZQ"
register_google(key = key )
# Retrieves a copy of the google map using the mean latitude and longitude as 
# the centre of focus. 
ShelleysHeart_basemap <- get_map(location=c(-1.8750486246575349,50.72039837397259), zoom=17, maptype = 'roadmap', source = 'google')

p <- ggmap(ShelleysHeart_basemap)
# Reads the dataframe made in Python into a dataframe that R can use
rawpageData <- read.csv("C:/Users/brown/.spyder-py3/PageData.csv")
# Omits the rows without any data in any columns
pageData <- na.omit(rawpageData)
# Copies the dataframe into a separate object
elements <- pageData
coordinates(elements) <- c("Longitude", "Latitude")
# Reads the dataframe into a SF object
pageData_sf <- st_as_sf(elements , coords = c("Longitude", "Latitude"))

exitPoints <- read.csv("C:/Users/brown/.spyder-py3/ExitPointBranchs.csv")
exitPoints <- na.omit(exitPoints)
filteredExit <- exitPoints %>% 
  select(Latitude, Longitude, Frequency)
# Plots the exit points
exitPointsplots <- p + geom_point(data=exitPoints, aes(x=Longitude, y=Latitude), size=3) 
# Plots the frequency of exit on top of the position. Experiment to be
# used to plot page index later
exitPointsplots <- exitPointsplots + geom_text(data=exitPoints, aes(x=Longitude, y=Latitude, label=exitPoints$Frequency), colour="blue")
plot(exitPointsplots)

st_crs(pageData_sf) <- 4326 # we can use EPSG as numeric here
st_crs(pageData_sf)

st_write(pageData_sf, "pageData_sf", driver = "ESRI Shapefile")
# Registers the key so I can get the map

p + geom_point(data=pageData, aes(x=Longitude, y=Latitude) ,size=1)


# Filters out the unimportant data from the dataset
Filtered <- pageData %>% 
  select(Tag, OriginalIndex,Latitude, Longitude)
# Filters the dataset by the major story branch
byron <- Filtered %>% 
  filter(Tag == "Byron")
percy <- Filtered %>% 
  filter(Tag=="Percy")
mary <- Filtered %>% 
  filter(Tag=="Mary")
john <- Filtered %>% 
  filter(Tag=="John")
unTagged <- rawpageData %>%
  select(Tag, OriginalIndex,Latitude, Longitude) %>% 
  filter(Tag=="No Story")
# So I can easily change the size of the points
pointSize <- 2

# Plots the Byron Map
byron_BaseMap <- get_map(location=c(mean(byron$Longitude),mean(byron$Latitude)), zoom=18, maptype = 'roadmap', source = 'google')
byron_ggmap <- ggmap(byron_BaseMap)
byronPoints <- geom_point(data=byron, aes(x=Longitude, y=Latitude), colour = "blue", size=pointSize)
byronMap <- byron_ggmap + byronPoints
plot(byronMap)

# Plots the Percy Map
percy_BaseMap <- get_map(location=c(mean(percy$Longitude),mean(percy$Latitude)), zoom=18, maptype = 'roadmap', source = 'google')
percy_ggmap <- ggmap(percy_BaseMap)
percyPoints <- geom_point(data=percy, aes(x=Longitude, y=Latitude), colour="red", size=pointSize)
percyMap <- percy_ggmap + percyPoints
plot(percyMap)

# Plots the Mary Map
mary_BaseMap <- get_map(location=c(mean(mary$Longitude),mean(mary$Latitude)), zoom=18, maptype = 'roadmap', source = 'google')
mary_ggmap <- ggmap(mary_BaseMap)
maryPoints <- geom_point(data=mary, aes(x=Longitude, y=Latitude),colour = "orange" ,size=pointSize)
maryMap <- mary_ggmap + maryPoints
plot(maryMap)

# Plots the John Map
john_BaseMap <- get_map(location=c(mean(john$Longitude),mean(john$Latitude)), zoom=18, maptype = 'roadmap', source = 'google')
john_ggmap <- ggmap(john_BaseMap)
johnPoints <- geom_point(data=john, aes(x=Longitude, y=Latitude) ,size=pointSize)
johnMap <- john_ggmap + johnPoints
plot(johnMap)

# Compiles all of the points and map into one object
overall <- p + byronPoints
overall <- overall + percyPoints
overall <- overall + maryPoints
overall <- overall+ johnPoints

# Exports the plot as a png
png(file = "pagePoints.png", res=50)
plot(overall)
ggsave(
  "pagePoints.png",
  plot(overall),
  dpi = 1200
)


