`%--%` <- function(x,y)
# https://stackoverflow.com/questions/46085274/is-there-a-string-formatting-operator-in-r-similar-to-pythons
{
  do.call(sprintf, c(list(x), y))
}

# 
library(dplyr)
library(sqldf)
library(randomForest)
library(tseries)

# load data

complete_countries <- c("Belgium", "Germany", "Italy", "Luxembourg", 
                      "Netherlands", "Portugal", "Slovenia",
                      "Spain","United Kingdom")
original <- read.csv("../data/processed/weekly_influenza_original.csv")

head(influenza)
head(inf_original)
head(plc_holder)
head(original)

influenza <- original[original$Country %in% complete_countries,]
unique(influenza$Country)

par(mfrow = c(1,3))
for (country in complete_countries[1:3]) 
{
  print(country)
  hist(influenza[influenza$Country == country,]$num_influenza)
}
par(mfrow = c(1,3))
for (country in complete_countries[4:6]) 
{
  print(country)
  hist(influenza[influenza$Country == country,]$num_influenza)
}
par(mfrow = c(1,3))
for (country in complete_countries[7:9]) 
{
  print(country)
  hist(influenza[influenza$Country == country,]$num_influenza)
}

influenza$rate <- 0
for (country in complete_countries)
{
  #rescale countries based on proportions
  num_obs <- length(influenza[influenza$Country == country,]$country_code)
  influenza[influenza$Country == country,]$rate[2:num_obs] <- diff(influenza[influenza$Country == country,]$num_influenza+1)/(influenza[influenza$Country == country,]$num_influenza[1:(num_obs-1)]+1)
  plot(influenza[influenza$Country == country,]$rate)
}



#influenza$outbreak <- as.numeric((influenza$num_influenza > 50))
influenza$rate


influenza <- select(influenza, c("country_code","year", "week","CapitalLatitude",
                                 "CapitalLongitude", "surface_height",
                                 "temperature", "evaporation", "humidity",
                                 "humidity", "Pressure_surface", "num_influenza",
                                 "outbreak"))

#train test split
train <- influenza[influenza$year <= 2017 & influenza$year >= 2010,]
test <- influenza[influenza$year <= 2018 & influenza$year >= 2018,]

head(train)

write.csv(train, "../data/processed/modelling_data/weekly_SWEurope_train.csv", row.names = FALSE)
write.csv(test, "../data/processed/modelling_data/weekly_SWEurope_test.csv", row.names = FALSE)

train_x <- train[,-ncol(train)]
train_y <- train[,ncol(train)]
test_x <- test[,-ncol(test)]
test_y <- test[,ncol(test)]

head(train)
head(train_y)

par(mfrow = c(1,2))
plot(train$num_influenza)
plot(train$temperature, type = "l")

pred_gp <- read.csv("../exploration/pred_full.csv")
pred_gp <- data.frame(t(as.matrix(pred_gp)))

plot(pred_gp$X1, type = "l")
lines(pred_gp$X1 + 2*pred_gp$X2, type="l", col = "blue")
lines(pred_gp$X1 - 2*pred_gp$X2, type="l", col = "red")

max_countries <- c()
for (country in complete_countries)
{
  #rescale countries based on proportions
  max_countries <- c(max_countries, max(influenza[influenza$Country == country,]$num_influenza))
}

df_prediction_gp <- cbind(test, pred_gp[-77,])
df_prediction_gp$upper <- pred_gp$X1[-77] + 2*sqrt(pred_gp$X2[-77])
df_prediction_gp$lower <- pred_gp$X1[-77] - 2*sqrt(pred_gp$X2[-77])
c<-1
df_prediction_gp$pred_class <- 0
df_prediction_gp$pred_class_upper <- 0
df_prediction_gp$pred_class_lower <- 0

for (country in c("BEL", "DEU", "ITA", "LUX", "NET", "POR", "SVN", "ESP", "GBR"))
{
  #rescale countries based on proportions
  max_country <- max_countries[1]
  df_prediction_gp[df_prediction_gp$country_code == country,]$pred_class <- as.numeric(df_prediction_gp[df_prediction_gp$country_code
                                                                                                        == country,]$X1>max_country*0.05)
  df_prediction_gp[df_prediction_gp$country_code == country,]$pred_class_upper <- as.numeric(df_prediction_gp[df_prediction_gp$country_code
                                                                                                        == country,]$upper>max_country*0.05)
  df_prediction_gp[df_prediction_gp$country_code == country,]$pred_class_lower <- as.numeric(df_prediction_gp[df_prediction_gp$country_code
                                                                                                        == country,]$lower>max_country*0.05)
  c <- c+1
}
table(df_prediction_gp$pred_class , test_y)
table(df_prediction_gp$pred_class_lower , test_y)
table(df_prediction_gp$pred_class_upper , test_y)

plot(df_prediction_gp[df_prediction_gp$country_code=="GBR",], main = "Probability of Outbreak for the UK", 
     ylab = "Probability of Outbreak")

plot(roc(test_y, df_prediction_gp$pred_class), print.auc=TRUE, col = 'red', lwd = 3,
     main = "ROC-AUC Plot of XGBoost_GP Model")

write.csv(df_prediction_gp, "predictions_gp_tableau.csv",row.names = FALSE)

sort(df_prediction_gp[df_prediction_gp$country_code=="SVN",]$week)

sum(df_prediction_gp$pred_class == test_y) / length(test_y)


#xgboost
# XGboost requires a special data structure
library(xgboost)
library(Matrix)
d_train <- sparse.model.matrix(train_y~ year + week + temperature + CapitalLatitude
                               + CapitalLongitude + surface_height
                               + evaporation + humidity + Pressure_surface, data=train_x)
d_test <- sparse.model.matrix(test_y~ year + week + temperature + CapitalLatitude
                              + CapitalLongitude + surface_height
                              + evaporation + humidity + Pressure_surface, data=test_x)
# Build XGboost classifier
model_xgboost <- xgboost(data = d_train, label = train_y, max.depth = 7, eta = 0.1, nthread = 4, nrounds = 2000, objective = "reg:logistic",
                         reg_lambda=1)
# Importance plots
importance_xgboost <- xgb.importance(feature_names = colnames(d_train), model = model_xgboost)
head(importance_xgboost)
xgb.plot.importance(importance_matrix = importance_xgboost)

pred_test <- predict(model_xgboost, d_test)


plot(test_y[test_x$country_code=="GBR"], main = "Probability of Outbreak for the UK", 
                    ylab = "Probability of Outbreak")
lines(pred_test[test_x$country_code=="GBR"])

sum(as.numeric(pred_test >= 0.5) == test_y) / length(test_y)

library(pROC)
table(as.numeric(pred_test >= 0.5) , test_y)

plot(roc(test_y, as.numeric(pred_test>=0.5)), print.auc=TRUE, col = 'red', lwd = 3,
     main = "ROC-AUC Plot of XGBoost Model")

write.csv(cbind(test_x,pred_test),"./RFpredictions.csv", row.names = FALSE)

# random forest
model_rf <- randomForest(train_y ~ temperature + week + year,data=train_x)
varImpPlot(model_rf)

pred_test <- predict(model_rf, test_x)

sum(as.numeric(pred_test >= 0.5) == test_y)

library(pROC)
table(as.numeric(pred_test >= 0.5) , test_y)

plot(roc(test_y, as.numeric(pred_test>=0.5)), print.auc=TRUE, col = 'red', lwd = 3)

roc_obj <- roc(test_y, as.numeric(pred_test>=0.5))
auc(roc_obj)

plot(pred_test, type = "l")
points(test_y, cex=0.2)



