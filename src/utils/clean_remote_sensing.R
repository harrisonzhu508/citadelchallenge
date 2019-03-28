#modify this script to clean the remote sensing data

`%--%` <- function(x,y)
# https://stackoverflow.com/questions/46085274/is-there-a-string-formatting-operator-in-r-similar-to-pythons
{
  do.call(sprintf, c(list(x), y))
}

# 
library(dplyr)
library(sqldf)

rm01 <- read.csv("../data/remote_sensing/2000_01.csv")
path <- "../data/remote_sensing/"

files <- list.files(path = path, pattern = ".csv", 
                    all.files = FALSE, full.names = FALSE,
                    recursive = FALSE, ignore.case = FALSE,
                    include.dirs = FALSE, no.. = FALSE)

for (file in files) 
# insert code to process dataframe
{ 
  print("Processing %s" %--% file)
  data <- read.csv("../data/processed/remote_sensing/%s" %--% file)
  data$tmmn <- data$tmmn * 0.1
  data$tmmx <- data$tmmx * 0.1
  
  write.csv(data, "../data/processed/remote_sensing/%s" %--% file)
}

