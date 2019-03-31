weirdsample <- function(n){
  # Input: number of desired observations
  # Output: An n by 104 matrix 
  dat <- matrix(0,n,104)
  for (i in 1:n){
    # Priors
    a <- runif(1,0,1000)
    b1 <- runif(1,3000,25000)
    rho <- runif(1,0.6,0.9)
    l <- runif(1,0.55,0.75)
    th <- runif(1,0,0.2)
    # Produce samples
    t <- c(1:104)
    m <- a + th*t + b1*sin((pi/52)*t - l*pi)^8 
    X <- m + c(arima.sim(list(ar=rho),26,sd=50),arima.sim(list(ar=rho),52,sd=50),arima.sim(list(ar=rho),26,sd=50))
    # Append samples 
    dat[i,] <- X
  }
  return(dat)
}

# Function that produces n samples of Y and phi in a matrix 
thetasample <- function(n){
  # Input: number of desired observations
  # Output: An n by 104+6 matrix of parameters
  dat <- matrix(0,n,109)
  for (i in 1:n){
    a <- runif(1,0,1000)
    b1 <- runif(1,3000,25000)
    rho <- runif(1,0.6,0.9)
    l <- runif(1,0.55,0.75)
    th <- runif(1,0,0.2)
    t <- c(1:104)
    m <- a + th*t + b1*sin((pi/52)*t - l*pi)^8
    X <- m + c(arima.sim(list(ar=rho),26,sd=50),arima.sim(list(ar=rho),52,sd=50),arima.sim(list(ar=rho),26,sd=50))
    # Append samples 
    dat[i,] <- c(X,a,b1,rho,l,th)
  }
  return(dat)
}

# Prior Elicitation: Graphs to consider likeness to relaity 
library(coda)
par(cex.lab=1.2)
sam <- weirdsample(10000)
upper <- c(NA,104)
lower <- c(NA,104)
for(i in 1:104){
  lower[i] <- HPDinterval(as.mcmc(sam[,i]))[1,1] # Lower 
  upper[i] <- HPDinterval(as.mcmc(sam[,i]))[1,2] # Upper
}
avg <- apply(sam[,1:104],2,mean)     
plot(avg, type="l", col = "grey35", xlim = c(0,104), ylim = c(0,27500), xlab = "Week", ylab = "Number infected", main = "Synthetic data from the prior")
plot(upper, type="l", col = "red", xlim = c(0,104), ylim = c(0,27500), xlab ="", ylab ="")
plot(lower, type="l", col = "red", xlim = c(0,104), ylim = c(0,27500), xlab ="", ylab ="")
legend(65, 27500, legend=c("Mean Process", "95% Credible Interval"),
       col=c("grey35", "red"), lty=1, cex=0.9)

# Now plot avg, min, max dist 
weekavg <- c(NA, 10000)
weekmin <- c(NA, 10000)
weekmax <- c(NA, 10000)
for(i in 1:10000){ 
  weekavg[i] <- mean(sam[i,1:104])
  weekmin[i] <- min(sam[i,1:104])
  weekmax[i] <- max(sam[i,1:104])
}
plot(density(weekavg), xlab= "Number Infected", ylab = "Density", ylim = c(0,0.0002), xlim = c(0,28000), main = "Approximate distributions of average and maximum infected", col ="red")
plot(density(weekmax), xlab= "", ylab = "", ylim = c(0,0.0002), xlim = c(0,28000), col = "grey35", main = "")
legend(17000, 0.0002, legend=c("Weekly Average", "Weekly Maximum"),
       col=c("red","grey35"), lty=1, cex=1)
# Prior stats 
mean(weekmax)
HPDinterval(as.mcmc(weekmax))

# Average count across whole sample and HPD
c(mean(weekavg), mean(weekmin), mean(weekmax))
HPDinterval(as.mcmc(weekavg))

# ABC
ABC <- function(n,eps,x){
  # Note: x must be a vector of observations
  raw <- thetasample(n)
  index <- c()
  for (i in 1:n){
    if(max(abs(raw[i,1:52]-x))<eps){ index <- c(index,i) }
  } # index is a vector of the realisations of X that satisfy our condition
  xcond <- raw[index,]
  return(xcond)
}

# Output rejected samples
ABCrej <- function(n,eps,x){
  raw <- thetasample(n)
  index <- c(1)
  for (i in 1:n){
    if(max(abs(raw[i,1:52]-x))<eps){ index <- c(index,i) }
  } 
  xcond <- raw[-index,]
  return(xcond)
} 

# Get the real data 
yr18 <- subset(influenza_activity, year == 2018)
eu <- subset(yr18, yr18$who_region == "European Region of WHO")
eu.con <- eu[,c(5,20)]
dat <- matrix(0,52,2)
for(i in 1:52){ dat[i,] <- c(i,sum(subset(eu.con,eu.con$week == i)$total_num_influenza_positive_viruses)) }
eu18 <- dat[,2]
# Perform ABC on real 
abc <- ABC(100000,3000,eu18)
rej <- ABCrej(100000,3000,eu18)
# Plot for report 
plot(eu18, ylim = c(0,27500), col = "black", xlab = "", ylab = "")
for(i in sample(1:min(nrow(rej),nrow(abc)),50)){
  lines(rej[i,1:52], ylim = c(0,27500), col = "red")
}
for(i in sample(1:min(nrow(rej),nrow(abc)),50)){
  lines(abc[i,1:52], ylim = c(0,27500), col = "green")
  lines(rej[i,1:52], ylim = c(0,27500), col = "red")
}
plot(eu18, ylim = c(0,27500), col = "black", pch=19, ylab = "Number Infected", xlab = "Weeks of 2018", main = "Acceptances of ABC by EU data")
legend(35, 25000, legend=c("Accepted", "Rejected","EU 2018"),
       col=c("green","red","black"), lty = c(1, 1, NA), pch = c(NA, NA, 19), cex=1)

# Compare 2017 to 2018
yr17 <- subset(influenza_activity, year == 2017)
eu <- subset(yr17, yr17$who_region == "European Region of WHO")
eu.con <- eu[,c(5,20)]
dat <- matrix(0,52,2)
for(i in 1:52){
  dat[i,] <- c(i,sum(subset(eu.con,eu.con$week == i)$total_num_influenza_positive_viruses))
}
eu17 <- dat[,2] 
# Plot 2018 on top of the prediction for 2018
abc <- ABC(100000,5000,eu17)
nrow(abc)
upper <- c(NA,52)
lower <- c(NA,52)
for(i in 53:104){
  lower[i] <- HPDinterval(as.mcmc(abc[,i]))[1,1] # Lower 
  upper[i] <- HPDinterval(as.mcmc(abc[,i]))[1,2] # Upper
}
avg <- apply(abc[,53:104],2,mean)     
plot(avg, type="l", col = "grey35", xlim = c(0,52), ylim = c(0,21000), xlab = "Weeks of 2018", ylab = "Number infected", main = "2018 European Forecast")
par(new=T)
plot(upper[53:104], type="l", col = "red", xlim = c(0,52), ylim = c(0,21000), xlab ="", ylab ="")
par(new=T)
plot(lower[53:104], type="l", col = "red", xlim = c(0,52), ylim = c(0,21000), xlab ="", ylab ="")
par(new=T)
plot(eu18, col = "black", xlim = c(0,52), ylim = c(0,21000), xlab ="", ylab ="", pch = 19)
legend(30, 21000, legend=c("Posterior mean", "95% Credible Interval", "Observed 2018 process"),
       col=c("grey35", "red", "black"), lty = c(1, 1, NA), pch = c(NA, NA, 19), cex=1)

# Probabilistic statements about the posterior 
weekmax <- c(NA, nrow(abc))
for(i in 1:nrow(abc)){ 
  weekmax[i] <- max(abc[i,53:104])
}
# Posterior
mean(weekmax)
HPDinterval(as.mcmc(weekmax))

# Look at how the distribution of the parameters shift 
hist(abc[,105])
hist(abc[,106])
hist(abc[,107])
hist(abc[,108])
hist(abc[,109])
#a,b1,rho,l,th

#################
# BF estimation #
#################

postMM <- function(theta){
  # Input: parameter vector 
  # Output: log of the value of the density of f(eu data|theta) 
  sum <- 0 
  for(i in 1:52){
    sum <- sum + log(dnorm(eu18[i],theta[i],1))
  }
  return(sum)
}
ksample <- function(n,k){
  # Input: number of desired observations
  # Output: An n by 104 matrix 
  dat <- matrix(0,n,104)
  for (i in 1:n){
    # Priors
    a <- runif(1,0,1000)
    b1 <- runif(1,3000,25000)
    rho <- runif(1,0.6,0.9)
    l <- runif(1,0.55,0.75)
    th <- runif(1,0,0.2)
    # Produce samples
    t <- c(1:104)
    m <- a + th*t + b1*sin((pi/52)*t - l*pi)^k 
    X <- m + c(arima.sim(list(ar=rho),26,sd=50),arima.sim(list(ar=rho),52,sd=50),arima.sim(list(ar=rho),26,sd=50))
    # Append samples 
    dat[i,] <- X
  }
  return(dat)
}

# Naive Estimation
B <- 10000 # Number of samples to draw and average 
p <- rep(0,6)
ind <- c(8,10,12,16,20,30)
for (k in 1:6){
  for (i in 1:B){
    p[k] <- p[k] + (postMM(ksample(1,ind[k])))}
}
par(new=F)
plot(exp(p/B))


# Plot the prediction 
upper <- c(NA,52)
lower <- c(NA,52)
for(i in 53:104){
  lower[i] <- HPDinterval(as.mcmc(abc[,i]))[1,1] # Lower 
  upper[i] <- HPDinterval(as.mcmc(abc[,i]))[1,2] # Upper
}
m <- apply(abc[,53:104],2,mean)     
plot(m, type="l", col = "grey35", xlim = c(0,52), ylim = c(0,21000), xlab = "Week", ylab = "Number infected", main = "Posterior prediciton for Europe 2019")
par(new=T)
plot(upper[53:104], type="l", col = "red", xlim = c(0,52), ylim = c(0,21000), xlab ="", ylab ="")
par(new=T)
plot(lower[53:104], type="l", col = "red", xlim = c(0,52), ylim = c(0,21000), xlab ="", ylab ="")
legend(25, 20000, legend=c("Posterior Mean", "HPD Interval"),
       col=c("grey35", "red"), lty=1, cex=0.9)
