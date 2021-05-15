model1 <- function(B,tau,seed,x,y){
  
  ################regression###################
  func1 <- glm(y ~Temperature+Humidity+Wind_speed+ Visibility+Dew_point_temperature+Solar_Radiation+Rainfall+Snowfall+Autumn+Spring+Summer+holiday+functioningday,data=df,family = poisson(link='log')) #
  bhat <- coef(func1)
  vbeta <- vcov(func1)
  
  ################parameters####################
  beta		<- matrix(0, nrow = B, ncol = ncol(x))
  ar			<- vector('numeric', length = B)
  
  beta[1,]	<- bhat
  
  tdens	<- function(b, X, Y){
    sum(Y*(X%*%b) - exp(X%*%b))
  }
  
  tau	<- tau # need to tune this
  B= B
  ################M-H steps####################
  set.seed(seed)
  for(t in 2:B){
    
    bstar	<- rmvnorm(1, beta[t-1,], tau*vbeta)
    r		<- exp(tdens(t(bstar), x, y)-tdens(beta[t-1,], x, y))
    U		<- runif(1)
    if(U < min(1,r)){
      beta[t,]	<- bstar
      ar[t]		  <- 1
    } else{
      beta[t,]	<- beta[t-1,]
      ar[t]		  <- 0
    }
  }
  out <- NULL
  out$ar <- ar
  out$beta <-beta
  return(out)
}