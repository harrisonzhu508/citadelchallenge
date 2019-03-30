`%--%` <- function(x,y)
# https://stackoverflow.com/questions/46085274/is-there-a-string-formatting-operator-in-r-similar-to-pythons
{
  do.call(sprintf, c(list(x), y))
}

# 
library(dplyr)
library(sqldf)
library(randomForest)

# load data
d <- read.csv("../data/health_indicators.csv")
colnames(d)


influenza <- read.csv("../data/processed/influenza.csv")

#train test split
train <- influenza[influenza$year <= 2014,]
train <- train[complete.cases(train),]
test <- influenza[influenza$year <= 2017 & influenza$year >= 2015,]
test <- test[complete.cases(test),]

write.csv(train, "../data/processed/modelling_data/influenza_train.csv", row.names = FALSE)
write.csv(test, "../data/processed/modelling_data/influenza_test.csv", row.names = FALSE)

train <- train[train$ContinentName == "South America",]
test <- test[test$ContinentName == "South America",]

train_x <- train[,-ncol(train)]
train_y <- train[,ncol(train)]
test_x <- test[,-ncol(test)]
test_y <- test[,ncol(test)]



# random forest
model_rf <- randomForest(train_y ~ CapitalLatitude + CapitalLongitude + year + month + 
                           tmmn + tmmx + NDVI,data=train_x)
varImpPlot(model_rf)

pred_test <- predict(model_rf, train_x)

sqrt(mean((pred_test - test_y)^2))

plot(pred_test, train_y, cex=0.3)
abline(a = 0, b = 1)



head(train)
head(test)
colnames(train_x)
max(train_y)
max(test_y)