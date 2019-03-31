================
Univariate ARIMA & VAR trials
=================

Motivation & Introduction
============

A usual method to approach a time series  :math:`(X_{t})_{t=1}^{T}` is to observe its ARIMA structure. By ARIMA(p,d,q), we usually refer to

.. math:: \Delta^d (X_{t}) = a+\sum_{j=1}^p  \Delta^d \theta_j(X_{t-j}) +\sum_{j=1}^q  \psi_j \varepsilon_{t-j} + \varepsilon_t
with :math:`\varepsilon_t \sim iidN(0,\sigma^2)` as a usual assumption.

