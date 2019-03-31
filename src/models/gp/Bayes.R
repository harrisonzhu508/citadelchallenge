
############
# AR model #
############


# Notes: 

# We model the deaths (or with easy adjustment the infections) 
# of influenza in non-epedemic states. We hope to use this to then 
# detect epedemics when observed values exceed our posterior samples 
# by a certain threshold 

# Questions: is there a floor in the influenza cycle?

# Note : particularly interested in the distribution of the maximu,
# so look at HPD of posterior max HPDinterval(as.mcmc(weekmax))


# Function that produces n samples of Y1,...,Y104 in a matrix 
xsample <- function(n){
  # Input: number of desired observations
  # Output: An n by 104 matrix 
  dat <- matrix(0,n,104)
  for (i in 1:n){
    # Priors
    a <- runif(1,100,150)
    b1 <- runif(1,0,20)
    b2 <- runif(1,0,20)
    rho <- runif(1,0.6,0.9)
    l <- runif(1,0.7,1)
    th <- runif(1,0,0.2)
    # Produce samples
    t <- c(1:104)
    m <- a + th*t + b1*sin((pi/26)*t - l*pi) + b2*cos((pi/26)*t - l*pi)
    X <- m + c(arima.sim(list(ar=rho),26,sd=2),arima.sim(list(ar=rho),52,sd=2),arima.sim(list(ar=rho),26,sd=2))
    # Append samples 
    dat[i,] <- X
  }
  return(dat)
}

# Function that produces n samples of Y and phi in a matrix 
thetasample <- function(n){
  # Input: number of desired observations
  # Output: An n by 104+6 matrix of parameters
  dat <- matrix(0,n,110)
  for (i in 1:n){
    # Priors
    a <- runif(1,100,150)
    b1 <- runif(1,0,20)
    b2 <- runif(1,0,20)
    rho <- runif(1,0.6,0.9)
    l <- runif(1,0.7,1)
    th <- runif(1,0,0.2)
    # Produce samples
    t <- c(1:104)
    m <- a + th*t + b1*sin((pi/26)*t - l*pi) + b2*cos((pi/26)*t - l*pi)
    X <- m + c(arima.sim(list(ar=rho),52,sd=2),arima.sim(list(ar=rho),52,sd=2))
    # Append samples 
    dat[i,] <- c(X,a,b1,b2,rho,l,th)
  }
  return(dat)
}

# Prior Elicitation: Graphs to consider likeness to relaity 
library(coda)
par(mfrow=c(1,1))
par(cex.lab=1.2)
sam <- xsample(10000)
upper <- c(NA,104)
lower <- c(NA,104)
for(i in 1:104){
  lower[i] <- HPDinterval(as.mcmc(sam[,i]))[1,1] # Lower 
  upper[i] <- HPDinterval(as.mcmc(sam[,i]))[1,2] # Upper
}
avg <- apply(sam[,1:104],2,mean)     
plot(avg, type="l", col = "grey35", xlim = c(0,104), ylim = c(70,180), xlab = "Week", ylab = "Number infected")
par(new=T)
plot(upper, type="l", col = "red", xlim = c(0,104), ylim = c(70,180), xlab ="", ylab ="")
par(new=T)
plot(lower, type="l", col = "red", xlim = c(0,104), ylim = c(70,180), xlab ="", ylab ="")
legend(0, 20, legend=c("Mean Process", "95% Credible Interval"),
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
plot(density(weekavg), xlab= "Number Infected", ylab = "Density", ylim = c(0,0.03), xlim = c(50,200), main = "Approximate distribution of Avg, Max and Min infected", col ="darkblue")
par(new=T)
plot(density(weekmin), xlab= "", ylab = "", ylim = c(0,0.03), xlim = c(50,200), col = "red", main = "")
par(new=T)
plot(density(weekmax), xlab= "", ylab = "", ylim = c(0,0.03), xlim = c(50,200), col = "grey35", main = "")
legend(50, 0.03, legend=c("Weekly Average", "Weekly Minimum", "Weekly Maximum"),
       col=c("darkblue","red","grey35"), lty=1, cex=0.9)

# Average count across whole sample and HPD
c(mean(dayavg), mean(daymin), mean(daymax))
#[1] 130.3822 107.7969 151.6472
HPDinterval(as.mcmc(dayavg))


# PRIOR ELICITATION   
# Graphs of realisations for different parameters 
# Consider how changing the priors gives us more or less realistic ideas of the real world 
for (i in 1:100){
  a <- runif(1,100,150)
  b1 <- runif(1,0,20)
  b2 <- runif(1,0,20)
  rho <- runif(1,0.6,0.9)
  l <- runif(1,0.7,1)
  th <- runif(1,0,0.2)
  t <- c(1:104)
  m <- a + th*t + b1*sin((pi/26)*t - l*pi) + b2*cos((pi/26)*t - l*pi)
  X <- m + c(arima.sim(list(ar=rho),52,sd=2),arima.sim(list(ar=rho),52,sd=2))
  plot(X, ylim = c(50,200), col = "red")
  ####
  a <- runif(1,100,150)
  b1 <- runif(1,0,20)
  b2 <- runif(1,0,20)
  rho <- runif(1,0.6,0.9)
  l <- runif(1,0.7,1)
  th <- runif(1,0,0.2)
  t <- c(1:104)
  m <- a + th*t + b1*sin((pi/26)*t - l*pi) + b2*cos((pi/26)*t - l*pi)
  X <- m + c(arima.sim(list(ar=rho),52,sd=2),arima.sim(list(ar=rho),52,sd=2))
  par(new=TRUE)
  plot(X, ylim = c(50,200), col = "black")
  ####
  a <- runif(1,100,150)
  b1 <- runif(1,0,20)
  b2 <- runif(1,0,20)
  rho <- runif(1,0.6,0.9)
  l <- runif(1,0.7,1)
  th <- runif(1,0,0.2)
  t <- c(1:104)
  m <- a + th*t + b1*sin((pi/26)*t - l*pi) + b2*cos((pi/26)*t - l*pi)
  X <- m + c(arima.sim(list(ar=rho),52,sd=2),arima.sim(list(ar=rho),52,sd=2))
  par(new=TRUE)
  plot(X, ylim = c(50,200), col = "blue")#, type = "l")
  par(new=TRUE)
}