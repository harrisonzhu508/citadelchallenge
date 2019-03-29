Spatiotemporal Modelling
========================

Introduction
------------

Suppose :math:`\{X_i,y_i\}_{i=1}^N` as our features and response (number of positive influenza cases). We
will assume the following underlying relationship:

.. math::

   y_i = f(x_i) + \epsilon_i,

where :math:`x_i\in\mathbb{R}^p` is the feature, :math:`\epsilon_i\sim N(0,\sigma^2)` 
and :math:`f`
is the underlying function. Since :math:`x_i` contains spatial and temporal features, 
the standard regression methods
of generalised additive models (GAMs) (Davison, 2003), gradient boosting and regression
trees (Bishop, 2006) are not adapted to this problem, and does not help us 
understand the underlying causality/correlation. In addition, pure time series
models such as Long-short term memory (LSTM) recurrent neural networks (Hochreiter et al., 1997),
SARIMA and ARMA-GARCH models (Davison, 2003) also do not take in account of the spatial
variation. On the other hand, stochastic processes such as Gaussian processes (GP) (Rasmussen et al., 2006)
or solutions to stochastic partial differential equations (SPDE) (Hairer, 2009) are
well-adapted to what we would like to accomplish.

SPDEs are the most natural approach to modelling spatiotemporal
phenomenon, by adding a driven white noise to a partial differential
equation (PDE) to obtain

.. math::

   Lu = f + \xi\circ dW,

where :math:`L` is a differential operator, :math:`f` is a function and :math:`\xi\circ dW`
is a driven white noise. However, there is limited software to provide
solutions to these SPDEs. ``R-INLA`` (Lindgren et al., 2015) is a library that uses the Bayesian
method integrated nested Laplace approximation (INLA) to construct weak
solutions to linear fractional SPDEs, but this places too much
restriction of the underlying SPDE and would result in blackbox
modelling. 

A Spatiotemporal Model
----------------------

In this study, we will thus use GPs as a spatiotemporal framework to
study spatiotemporal variations. We let :math:`f` have a Gaussian process prior, giving

.. math::

   f\sim GP(\mu(\cdot), k(\cdot,\cdot)),

where :math:`\mu(\cdot)` and :math:`k(\cdot,\cdot)` are chosen mean and covariance functions. 
We also call :math:`k(\cdot,\cdot)` a kernel by convention. The choice of the mean is usually zero mean,
constant mean, polynomial or splines. This helps us capture the trend of :math:`y_i`. However, perhaps 
what would be more important is capturing the covariance between different features. Finally, it is 
worth mentioning that GP regression is a form of non-parametric (infinite dimensional) regression.
Suppose we have observed some data :math:`X,y` with :math:`N` observation and we are given a 
test set :math:`X_*` with :math:`K` observations,  where we would like to predict :math:`y_*`. 
Then using the  Sherman-Morrison-Woodbury identity on the joint posterior of the GP, 
we obtain the posterior distribution of :math:`f_*` (Rasmussen et al, 2006)

.. math::

    f_*| X,y,f\sim N_K(K_*(K + \sigma^2I_N)^{-1}[f + \mu(X)], K_{**} - K_*(K + \sigma^2I_N)^{-1}K_*),

where the notations are :math:`f, f_*` denote the value of the function for the training and test set,
for the GP function, :math:`K, K_*,K_{**}` are the covariance matrices of the training, training-test and
test sets.
