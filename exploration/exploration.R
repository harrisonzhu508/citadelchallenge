`%--%` <- function(x,y)
# https://stackoverflow.com/questions/46085274/is-there-a-string-formatting-operator-in-r-similar-to-pythons
{
  do.call(sprintf, c(list(x), y))
}

# 
library(dplyr)
library(sqldf)



# work
remote <- read.csv("../data/processed/remote_sensing.csv")
influenza <- read.csv("../data/influenza_activity.csv")

merge(influenza, remote, by.x = )

head(remote)
head(influenza)
colnames(influenza)

