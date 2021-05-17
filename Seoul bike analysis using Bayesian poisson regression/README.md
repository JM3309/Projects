# Seoul bike analysis project

This repo contains the final project for Math 640(Bayesian Statistics) at Georgetown University.

In this analysis project, we focus on the bike sharing demand in Seoul, Korea and try to explore the relationship between hourly rented bikes demand and some influencing factors. We wish to build a Poisson regression model on all observed data and use Bayesian methods to find the posterior distribution of the coefficients. We will try to discover how differnt priors on β will affect the posterior distribution. We suggest three priors, a flat prior, a normal prior with Inverse-Gamma variance, and a normal prior with Half-Cauchy vairance. 

## Model
* [Model1](https://github.com/JM3309/Projects/blob/master/Seoul%20bike%20analysis%20using%20Bayesian%20poisson%20regression/model1_update.R): Flat prior on β
* [Model2](https://github.com/JM3309/Projects/blob/master/Seoul%20bike%20analysis%20using%20Bayesian%20poisson%20regression/model2_update.R): a normal prior with Inverse-Gamma variance on β
* [Model3](https://github.com/JM3309/Projects/blob/master/Seoul%20bike%20analysis%20using%20Bayesian%20poisson%20regression/model3_update.R): a normal prior with Half-Cauchy vairance on β

For the simplicity and convergence, we should choose mean zero normal prior with Inverse-Gamma variance (Model2)

## [Paper](_)

## [Data source](https://github.com/JM3309/Projects/blob/master/Seoul%20bike%20analysis%20using%20Bayesian%20poisson%20regression/SeoulBikeData.csv):
[Seoul Bike Sharing Demand Data Set](https://archive.ics.uci.edu/ml/datasets/Seoul+Bike+Sharing+Demand)
