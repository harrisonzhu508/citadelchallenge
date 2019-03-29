library(dplyr)
library(sqldf)

country_codes <- read.csv("../data/country_codes.csv")
remote <- read.csv("../data/processed/remote_sensing.csv")
influenza <- read.csv("../data/processed/influenza_activity.csv")
plc_holder <- merge(influenza, remote, by.x = c("country_code", "year", "month"), by.y = c("country_code", "year", "month"))

plc_holder <- select(plc_holder,c("Country", "CapitalName", "country_code", "who_region", 
                    "flu_region", "latitude", "longitude", "CapitalLatitude", 
                    "CapitalLongitude", "year", "month", "tmmn", "tmmx", 
                    "pr", "def", "aet", "srad", "vap", "num_influenza_positive"))

write.csv(plc_holder, "../data/processed/influenza.csv", row.names = FALSE)
