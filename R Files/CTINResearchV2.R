# Gets the libraries required for the script
require(ggmap)
require(sf)
require(sp)
require(rgdal)
require(tidyverse)
require(ggplot2)
require(geosphere)



# Google Cloud API Key - Need to put in your personal API key. Get it from Google Cloud
# Account
key <- ""
register_google(key = key )
# Retrieves a copy of the google map using the mean latitude and longitude as 
# the centre of focus. 
ShelleysHeart_basemap <- get_map(location=c(-1.8750486246575349,50.72039837397259), zoom=18, maptype = 'roadmap', source = 'google')
# Saves the basemap to a variable that is quicker to type
p <- ggmap(ShelleysHeart_basemap)


satelliteSH <- get_map(location = c(-1.8750486246575349,50.72039837397259), zoom=18, maptype="satellite", source='google')
satelliteSH <- ggmap(satelliteSH)
png(file="ShelleysHeart_Satellite.png", res = 50)
ggsave(
  "ShelleysHeart_Satellite.png",
  plot(satelliteSH),
  dpi = 1200
)


# Reads the dataframe made in Python into a dataframe that R can use
rawpageData <- read.csv("PageData.csv")
# Omits the rows without any data in any columns
pageData <- na.omit(rawpageData)
# Copies the dataframe into a separate object
elements <- pageData
coordinates(elements) <- c("Longitude", "Latitude")
# Reads the dataframe into a SF object
pageData_sf <- st_as_sf(elements , coords = c("Longitude", "Latitude"))

exitPoints <- read.csv("ExitPointBranchs.csv")
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

#st_write(pageData_sf, "pageData_sf", driver = "ESRI Shapefile")
# Registers the key so I can get the map


# First read in the routes dataframe generated in python from the location data
routeCoords <- read.csv("Routes.csv")
# Initializes the list
routes <- c()
png(file = "routes.png", res=50)
ggsave(
  "routes.png",
  plot(p + geom_segment(data=routeCoords, aes(x = RootLon, y = RootLat, xend = DestinationLon, yend = DestinationLat),
            arrow = arrow(length = unit(0.1, "cm"))) + geom_point(data=pageData, aes(x=Longitude, y=Latitude) ,size=1)),
  dpi=1200
  )



# Filters out the unimportant data from the dataset
Filtered <- pageData %>% 
  select(X, Tag, OriginalIndex,Latitude, Longitude)
filterRoutes <- routeCoords %>% 
  select(RootLat, RootLon, DestinationLat, DestinationLon, Index)

# Filters the dataset by the major story branch
byron <- Filtered %>% 
  filter(Tag == "Byron")
byronRoutes <- filterRoutes %>% 
  filter(Index=="Byron")

percy <- Filtered %>% 
  filter(Tag=="Percy")
percyRoutes <- filterRoutes %>% 
  filter(Index=="Percy")

mary <- Filtered %>% 
  filter(Tag=="Mary")
maryRoutes <- filterRoutes %>% 
  filter(Index=="Mary")

john <- Filtered %>% 
  filter(Tag=="John")
johnRoutes <- filterRoutes %>% 
  filter(Index=="John")

unTagged <- rawpageData %>%
  select(Tag, OriginalIndex,Latitude, Longitude) %>% 
  filter(Tag=="No Story")
# So I can easily change the size of the points
pointSize <- 10


# Plots the Byron Map
byron_BaseMap <- get_map(location=c(mean(byron$Longitude),mean(byron$Latitude)), zoom=18, maptype = 'roadmap', source = 'google')
byron_ggmap <- ggmap(byron_BaseMap)
byronPoints <- geom_point(data=byron, aes(x=Longitude, y=Latitude), colour = "blue", size=pointSize)
byronMap <- byron_ggmap + byronPoints + geom_text(data=byron, aes(x=Longitude, y=Latitude, label=byron$X, colour="white"))
png(file = "byronMap.png", res =50)
ggsave(
  "byronMap.png",
  plot(byronMap),
  dpi = 1200
)
png(file = "byronRoutes.png", res =50)
ggsave(
  "byronRoutes.png",
  plot(byronMap + geom_segment(data=byronRoutes, aes(x = RootLon, y = RootLat, xend = DestinationLon, yend = DestinationLat),
                  arrow = arrow(length = unit(0.1, "cm")))),
  dpi = 1200
)



# Plots the Percy Map
percy_BaseMap <- get_map(location=c(mean(percy$Longitude),mean(percy$Latitude)), zoom=18, maptype = 'roadmap', source = 'google')
percy_ggmap <- ggmap(percy_BaseMap)
percyPoints <- geom_point(data=percy, aes(x=Longitude, y=Latitude), colour="red", size=pointSize)
percyMap <- percy_ggmap + percyPoints + geom_text(data=percy, aes(x=Longitude, y=Latitude, label=percy$X, colour="white"))
png(file = "percyMap.png", res =50)
ggsave(
  "percyMap.png",
  plot(percyMap),
  dpi = 1200
)
png(file = "percyRoutes.png", res=50)
ggsave(
  "percyRoutes.png",
  plot(percyMap + geom_segment(data=percyRoutes, aes(x = RootLon, y = RootLat, xend = DestinationLon, yend = DestinationLat),
                               arrow = arrow(length = unit(0.1, "cm")))
  ),
  dpi = 1200
)


# Plots the Mary Map
mary_BaseMap <- get_map(location=c(mean(mary$Longitude),mean(mary$Latitude)), zoom=18, maptype = 'roadmap', source = 'google')
mary_ggmap <- ggmap(mary_BaseMap)
maryPoints <- geom_point(data=mary, aes(x=Longitude, y=Latitude),colour = "orange" ,size=pointSize)
maryMap <- mary_ggmap + maryPoints + geom_text(data=mary, aes(x=Longitude, y=Latitude, label=mary$X))
png(file = "maryMap.png", res =50)
ggsave(
  "maryMap.png",
  plot(maryMap),
  dpi = 1200
)
png(file = "maryRoutes.png", res = 50)
ggsave(
  "maryRoutes.png",
  plot(maryMap + geom_segment(data=maryRoutes, aes(x = RootLon, y = RootLat, xend = DestinationLon, yend = DestinationLat),
                               arrow = arrow(length = unit(0.1, "cm")))
  ),
  dpi = 1200
)

# Plots the John Map
john_BaseMap <- get_map(location=c(mean(john$Longitude),mean(john$Latitude)), zoom=18, maptype = 'roadmap', source = 'google')
john_ggmap <- ggmap(john_BaseMap)
johnPoints <- geom_point(data=john, aes(x=Longitude, y=Latitude),colour="green" ,size=pointSize)
johnMap <- john_ggmap + johnPoints + geom_text(data=john, aes(x=Longitude, y=Latitude, label=john$X))
png(file = "johnMap.png", res =50)
ggsave(
  "johnMap.png",
  plot(johnMap),
  dpi = 1200
)
png(file = "johnRoutes.png", res=50)
ggsave(
  "johnRoutes.png",
  plot(johnMap + geom_segment(data=johnRoutes, aes(x = RootLon, y = RootLat, xend = DestinationLon, yend = DestinationLat),
                               arrow = arrow(length = unit(0.1, "cm")))
  ),
  dpi = 1200
)


# Compiles all of the points and map into one object
overall <- p + byronPoints
overall <- overall + percyPoints
overall <- overall + maryPoints
overall <- overall+ johnPoints
overall <- overall + geom_text(data=pageData, aes(x=Longitude, y=Latitude, label=pageData$X))

# Exports the plot as a png
png(file = "pagePoints.png", res=50)
plot(overall)
ggsave(
  "pagePoints.png",
  plot(overall),
  dpi = 1200
)

branches <- read.csv("BranchesWOptionsLocation.csv")
byronBranches <- branches %>% 
  filter(Tag=="Byron")

percyBranches <- branches %>% 
  filter(Tag=="Percy")

maryBranches <- branches %>% 
  filter(Tag=="Mary")

johnBranches <- branches %>% 
  filter(Tag=="John")

png(file="ByronBranches.png", res = 50)
ggsave(
  "ByronBranches.png",
plot(byron_ggmap + geom_segment(data=byronBranches, aes(x = RootLon, y = RootLat, xend = DesLon, yend = DesLat),
                arrow = arrow(length = unit(0.1, "cm"))) +
                geom_point(data=byronBranches, aes(x=RootLon, y=RootLat),colour = "blue" ,size=pointSize) +
                geom_point(data=byronBranches, aes(x=DesLon, y=DesLat),colour = "blue" ,size=pointSize)+
                geom_text(data=byronBranches, aes(x=RootLon, y=RootLat, label=RootIndex, colour="white")) +
                geom_text(data=byronBranches, aes(x=DesLon, y=DesLat, label=DesIndex, colour="white"))),
dpi = 1200
)


png(file="PercyBranches.png", res = 50)
ggsave(
  "PercyBranches.png",
  plot(percy_ggmap + geom_segment(data=percyBranches, aes(x = RootLon, y = RootLat, xend = DesLon, yend = DesLat),
                arrow = arrow(length = unit(0.1, "cm"))) +
                geom_point(data=percyBranches, aes(x=RootLon, y=RootLat),colour = "red" ,size=pointSize) +
                geom_point(data=percyBranches, aes(x=DesLon, y=DesLat),colour = "red" ,size=pointSize)+
                geom_text(data=percyBranches, aes(x=RootLon, y=RootLat, label=RootIndex, colour="white")) +
                geom_text(data=percyBranches, aes(x=DesLon, y=DesLat, label=DesIndex, colour="white"))),
  dpi = 1200

)

png(file="MaryBranches.png", res = 50)
ggsave(
  "MaryBranches.png",
  plot(mary_ggmap + geom_segment(data=maryBranches, aes(x = RootLon, y = RootLat, xend = DesLon, yend = DesLat),
                arrow = arrow(length = unit(0.1, "cm"))) +
                geom_point(data=maryBranches, aes(x=RootLon, y=RootLat),colour = "orange" ,size=pointSize) +
                geom_point(data=maryBranches, aes(x=DesLon, y=DesLat),colour = "orange" ,size=pointSize)+
                geom_text(data=maryBranches, aes(x=RootLon, y=RootLat, label=RootIndex)) +
                geom_text(data=maryBranches, aes(x=DesLon, y=DesLat, label=DesIndex))),
  dpi = 1200
)

png(file="JohnBranches.png", res = 50)
ggsave(
  "JohnBranches.png",
  plot(john_ggmap + geom_segment(data=johnBranches, aes(x = RootLon, y = RootLat, xend = DesLon, yend = DesLat),
                arrow = arrow(length = unit(0.1, "cm"))) +
                geom_point(data=johnBranches, aes(x=RootLon, y=RootLat),colour = "green" ,size=pointSize) +
                geom_point(data=johnBranches, aes(x=DesLon, y=DesLat),colour = "green" ,size=pointSize)+
                geom_text(data=johnBranches, aes(x=RootLon, y=RootLat, label=RootIndex)) +
                geom_text(data=johnBranches, aes(x=DesLon, y=DesLat, label=DesIndex))),
  dpi = 1200
  
)