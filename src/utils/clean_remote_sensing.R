#modify this script to clean the remote sensing data

`%--%` <- function(x,y)
# https://stackoverflow.com/questions/46085274/is-there-a-string-formatting-operator-in-r-similar-to-pythons
{
  do.call(sprintf, c(list(x), y))
}

# 
library(dplyr)
library(sqldf)

path <- "../../data/processed/noaa"

country_code <- read.csv("../../data/country_codes.csv")
influenza <- read.csv("../../data/influenza_activity.csv")
influenza <- influenza[,c(1,2,3,4,5,20)]
colnames(influenza)

weekly_remote <- read.csv("../../data/processed/noaa/joined_remote.csv")

plc_holder <- merge(influenza, weekly_remote, by.x = c("country_code", "year", "week")
                    , by.y = c("country_code", "year", "week"))
head(influenza)
head(plc_holder)

save_data <- select(plc_holder, c("Country", "CapitalName","country_code", "who_region", "flu_region", 
                                  "ContinentName","year", "week", "CapitalLatitude", "CapitalLongitude",
                                  "Geopotential_height_surface", "Temperature_height_above_ground",
                                  "Potential_Evaporation_Rate_surface_6_Hour_Average", 
                                  "Specific_humidity_height_above_ground", "Pressure_surface", 
                                  "total_num_influenza_positive_viruses"))

colnames(save_data)
colnames(save_data)[c(11,12,13,14,15,16)] <- c("surface_height", "temperature", "evaporation",
                                               "humidity", "Pressure_surface", "num_influenza")
write.csv(save_data, "../../data/processed/weekly_influenza.csv")