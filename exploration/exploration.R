library(sqldf)
country_codes <- read.csv("./data/country_codes.csv")
developing_countries <- read.csv("./data/processed/developing_countries", header = FALSE)

dev_mortality <- merge(merged_mortality, developing_countries, by.x = "country_name", by.y = "V1")

head(dev_mortality)

write.csv(dev_mortality, "data/processed/dev_mortality.csv")

unique(merged_mortality$cause_code)
