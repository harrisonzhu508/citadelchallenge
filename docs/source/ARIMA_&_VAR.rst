=================
Univariate ARIMA & VAR trials
=================



Motivation & Introduction
============

A usual method to approach a time series  :math:`(X_{t})_{t=1}^{T}` is to observe its ARIMA structure. By ARIMA(p,d,q), we refer to

.. math:: \Delta^d (X_{t}) = a+\sum_{j=1}^p \theta_j \Delta^d (X_{t-j}) +\sum_{j=1}^q  \psi_j \varepsilon_{t-j} + \varepsilon_t
with :math:`\varepsilon_t \sim iidN(0,\sigma^2)` as a usual distributional assumption.




We start by looking at univariate case, which `X_{t}\in\mathbb{R}`.



Univariate examples
============

USA
-----------

We pick a country which has small empty reports over 2000-2018 and large numbers so that spikes c.f. usual observations can be seen clearly. USA seems to be a good choice, with time plot as follows:

.. image:: ./img/USA.png





Germany (DEU)
-----------




VAR example: DEU and its neighbourhoods
============



