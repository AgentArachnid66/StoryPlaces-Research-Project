require(ggmap)
require("sf")
require("sp")
require("rgdal")
key <- "AIzaSyD5B3reqaxwM3PXkuYnWY_vtwNZmzETgZQ"

elements <- read.csv("C:/Users/brown/.spyder-py3/PageData.csv")
elements <- na.omit(elements)
coordinates(elements) <- c("Longitude", "Latitude")
pageData_sf <- st_as_sf(elements , coords = c("Longitude", "Latitude"))
st_crs(pageData_sf) <- 4326 # we can use EPSG as numeric here
st_crs(pageData_sf)

st_write(pageData_sf, "pageData_sf", driver = "ESRI Shapefile")
register_google(key = key )

ShelleysHeart_basemap <- get_map(location=c(-1.875315,50.720544), zoom=19, maptype = 'roadmap', source = 'google')

p <- ggmap(ShelleysHeart_basemap)
p + geom_point(data=pageData, aes(x=Longitude, y=Latitude), size=3)

