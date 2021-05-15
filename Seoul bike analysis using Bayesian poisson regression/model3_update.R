model3 <- function(B,tau,seed,x,y,sigma_start,A,alpha_start){
  
  ################regression###################
  func1 <- glm(y ~Temperature+Humidity+Wind_speed+ Visibility+Dew_point_temperature+Solar_Radiation+Rainfall+Snowfall+Autumn+Spring+Summer+holiday+functioningday,data=df,family = poisson(link='log')) #
  bhat <- coef(func1)
  vbeta <- vcov(func1)
  
  ################parameters####################
  beta		<- matrix(0, nrow = B, ncol = ncol(x))
  ar			<- vector('numeric', length = B)
  sigma2   <- vector('numeric', length = B)
  alpha <- vector('numeric', length = B)
  
  beta[1,]	<- bhat 
  sigma2[1] <- sigma_start
  alpha[1] <- alpha_start
  
  tdens	<- function(b, X, Y,sigma2){
    likelihood <-sum(Y*(X%*%b) - exp(X%*%b))
    prior <- (-1/(2*sigma2)*(t(b)%*%b))
    post <- likelihood + prior
    return(post)
  }
  
  tau	<- tau # need to tune this
  B= B
  ################M-H steps####################
  set.seed(seed)
  for(t in 2:B){
    
    #sample beta
    bstar	<- rmvnorm(1, beta[t-1,], tau*vbeta)
    r		<- exp(tdens(t(bstar), x, y,sigma2[t-1])-tdens(beta[t-1,], x, y,sigma2[t-1]))
    #print(r)
    U		<- runif(1)
    if(U < min(1,r)){
      beta[t,]	<- bstar
      ar[t]		  <- 1
    } else{
      beta[t,]	<- beta[t-1,]
      ar[t]		  <- 0
    }
    
    #sample sigma2 for beta
    sigma2[t] <- rinvgamma(1,1,0.5*(t(beta[t,])%*%beta[t,])+1/alpha[t-1])
    
    alpha[t] <- rinvgamma(1,1,1/A^2+1/sigma2[t]^2)
  }
  out <- NULL
  out$ar <- ar
  out$beta <-beta
  out$sigma2 <-sigma2
  out$alpha <-alpha
  return(out)
}

