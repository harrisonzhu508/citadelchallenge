####################################
## EDA for influenza_activity.csv ##
####################################
library(data.table)
influenza_activity <- fread("influenza_activity.csv", header = T)

# Outbreak type 
barplot(table(as.factor(influenza_activity$influenza_like_illness_activity)), main = "Class of influenza outbreaks", ylim = c(0,35000))

# Where do local and regional outbreaks occur?
loc <- subset(influenza_activity, influenza_activity$influenza_like_illness_activity == "Local Outbreak")
barplot(table(as.factor(loc$flu_region)), las = 2, cex.names=0.8, ylim = c(0,600), main = "Locations of local influenza outbreaks")
reg <- subset(influenza_activity, influenza_activity$influenza_like_illness_activity == "Regional Outbreak")
barplot(table(as.factor(reg$flu_region)), las = 2, cex.names=0.8, ylim = c(0,500), main = "Locations of regional influenza outbreaks")
dev.off()

# Outbreaks in WHO
# Stacked Bar Plot with Colors and Legend
outbreaks <- subset(influenza_activity, influenza_activity$influenza_like_illness_activity %in% c("Widespread Outbreak", "Regional Outbreak", "Local Outbreak"))
outbreaks[outbreaks$who_region == "European Region of WHO"]$who_region <- "European" 
outbreaks[outbreaks$who_region == "African Region of WHO"]$who_region <- "African" 
outbreaks[outbreaks$who_region == "Region of the Americas of WHO"]$who_region <- "American" 
outbreaks[outbreaks$who_region == "Western Pacific Region of WHO"]$who_region <- "Western Pacific" 
outbreaks[outbreaks$who_region == "Eastern Mediterranean Region of WHO"]$who_region <- "Eastern Mediterranean" 
outbreaks[outbreaks$who_region == "South-East Asia Region of WHO"]$who_region <- "South-East Asian" 
counts <- table(outbreaks$influenza_like_illness_activity,outbreaks$who_region)
barplot(counts[,], main="Distribution of outbreak type by region",
        ylim=c(0,4000),
        col=c("royalblue","forestgreen","red"),
        legend = rownames(counts),
        args.legend = list(x="topleft"),
        las = 2)

# In Europe?
europe <- subset(outbreaks, outbreaks$who_region == "European")
eu.counts <- table(europe$influenza_like_illness_activity,europe$country_code)
barplot(eu.counts[,], main="Distribution of outbreak type by European region",
        xlab="Country Code", 
        cex.lab = 1.1,
        ylim=c(0,280),
        col=c("royalblue","forestgreen","red"),
        legend = rownames(counts),
        args.legend = list(x="topleft"),
        las = 2)

# What time of year are these occuring?
yr18 <- subset(influenza_activity, year == 2018)
heat <- matrix(NA,18,52)
row <- unique(yr18$flu_region)
for(i in 1:18){
  for(j in 1:52){
    heat[i,j] <- sum(subset(yr18, yr18$flu_region == row[i] & yr18$week == j)$num_detected_total_influenza_a)
  }
}
# Rescale
scaled.heat <- matrix(NA,18,52)
for(i in 1:18){ scaled.heat[i,] <- heat[i,]/max(heat[i,]) }
# Order 
unique(yr18$flu_region)
ord <- c(1,6,12,14,17,2,8,15,3,11,16,18,4,9,5,10,7) 
scaled.heat <- scaled.heat[ord,]
# Plot
library(reshape2)
scaled.heat[ord,1:15]
melted.heat <- melt(as.matrix(scaled.heat))  
# Var1 is flu_region, Var2 is normalised count
library(ggplot2)
ggplot(data = (melted.heat), aes(x=Var1, y=Var2, fill=value)) + 
  geom_tile()+
  theme_minimal()+
  scale_fill_gradient2(low = "yellow", high = "red", mid = "orange", 
                       midpoint = 0.5, limit = c(0,1), space = "Lab", 
                       name="Normalised influenza count")

# Heatmap for europe 2018
eu <- subset(yr18, yr18$who_region == "European Region of WHO")
heat <- matrix(NA,50,52)
row <- unique(eu$country_code)
names <- noquote(row)
for(i in 1:50){
  for(j in 1:52){
    heat[i,j] <- sum(subset(eu, eu$country_code == row[i] & eu$week == j)$num_detected_total_influenza_a)
  }
}
# Rescale
scaled.heat <- matrix(NA,50,52)
for(i in 1:50){
  scaled.heat[i,] <- heat[i,]/max(heat[i,])
}

library(reshape2)
melted.heat <- melt((as.matrix(scaled.heat)))  # Var1 is flu_region, Var2 is normalised count
# Impute missing values 
for(i in 1:2600){
  if(is.na(melted.heat$value[i])){melted.heat$value[i] <- mean(melted.heat$value[i-1],melted.heat$value[i+1])}
}

# Plot 
tran <- t(scaled.heat)
tran <- tran[,-c(45,47,7)]
names <- row[-c(45,47,7)]
melted.heat <- melt((as.matrix(tran)))  # Var1 is flu_region, Var2 is normalised count
# Plot 
ggplot(data = (melted.heat), aes(x=Var1, y=Var2, fill=value)) + 
  geom_tile()+
  theme_minimal()+
  labs(y = "Country Code")+
  labs(x = "Weeks of 2018")+
  labs(title = "Seasonality of influenza in the European Region of WHO")+
  theme(plot.title = element_text(size=15))+
  theme(plot.title = element_text(hjust = 0.5))+
  theme(plot.title = element_text(margin = margin(b = 20)))+
  theme(axis.text.y = element_text(angle = 0, hjust = 1.5, size=10),
        axis.text.x = element_text(angle = 0, hjust = 1.5, size=10),
        axis.title.y = element_text(size = 14))+
  scale_y_discrete(limits=names)+
  scale_fill_gradient2(low = "yellow", high = "red", mid = "orange", 
                       midpoint = 0.5, limit = c(0,1), space = "Lab", 
                       name="Normalised influenza count")