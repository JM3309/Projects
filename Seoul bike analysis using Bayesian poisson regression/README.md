# Seoul bike analysis project

In this analysis project, we focus on the bike sharing demand in Seoul, Korea and try to explore the relationship between hourly rented bikes demand and some influencing factors. 
We wish to build a Poisson regression model on all observed data and use Bayesian methods to find the posterior distribution of the coefficients. We will try to discover how differnt priors on β will affect the posterior distribution. We suggest three priors, a flat prior, a normal prior with Inverse-Gamma variance, and a normal prior with Half-Cauchy vairance. 

## Model
* Model1: Flat prior on β
* Model2: a normal prior with Inverse-Gamma variance on β
* Model3: a normal prior with Half-Cauchy vairance on β

For the simplicity and convergence, we should choose mean zero normal prior with Inverse-Gamma variance (Model2)

## [Paper](_)

## Data source:
https://archive.ics.uci.edu/ml/datasets/Seoul+Bike+Sharing+Demand
