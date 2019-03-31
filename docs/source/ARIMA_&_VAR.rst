=================
Univariate ARIMA & VAR trials
=================


Motivation & Introduction
============

A usual method to approach a time series  :math:`(X_{t})_{t=1}^{T}` is to observe its Autoregressive Integrated Moving Average (ARIMA) structure. By ARIMA(p,d,q), we refer to

.. math:: \Delta^d (X_{t}) = a+\sum_{j=1}^p \theta_j \Delta^d (X_{t-j}) +\sum_{j=1}^q  \psi_j \varepsilon_{t-j} + \varepsilon_t
with :math:`\varepsilon_t \sim iidN(0,\sigma^2)` as a usual distributional assumption.




We start by looking at univariate case, which :math:`X_{t}\in\mathbb{R}`.


Univariate examples
============

USA
-----------

We pick a country which has small empty reports over 2000-2018 and sizable numbers so that spikes compared to usual observations can be seen clearly. USA seems to be a good choice, with time plot as follows:

.. image:: ./img/USA.png

Indeed, compared to the globe, despite some other countries like Australia have yearly spike time being different from American, America data still captures the global trend as well as spikes.



Now, write the sequence as :math:`(USA_{t})_{t=1}^{T}`, and let us firstly check the stationarity: we run a Dickey-Fluller test on the sequence, and obtained a p-value of 0.022; a Dicky-Fuller on :math:`\Delta USA_t` to be having a p-value of 0.013; and on :math:`\Delta \Delta USA_t` gets a p-value of 0.009. Hence, upon the choice of significance level, we can have the following conclusion:

- If we choose the significance level to be the classical 5% or anything above 2.3%, then we conclude :math:`USA_t \sim I(0)`, i.e. we can investigate :math:`USA_{t}` directly.

- If we choose the significance level to be a rigorous 1% for instance, then we conclude  :math:`USA_t \sim I(2)`, i.e. we can only investigate :math:`\Delta \Delta USA_{t}` directly.

For both circumstances, we can now carry on by reading the sample estimation on the ACF (Auto Correlation Function) and PACF (Partial Auto Correlation Function) to determine how many lags to use, i.e. we are now investigating :math:`USA_t \sim ARIMA(p, d, q)` where :math:`d \in \{0, 2\}`.


ARIMA(p,0,q)
~~~~~~~~
When d=0, i.e. using USAt we observed 1-2 significant lags in PACF and 1-9 in ACF, thus all 18 possible comibnations of ARIMA are ran, and based on Akaike Information Criterion (AIC) and the Bayesian Information Criterion (BIC), we selected the following two models for fitting:


- ARIMA(5,0,2), which has the lowest BIC and the second lowest AIC;

- ARIMA(7,0,2), which has the lowest AIC and the forth lowest BIC.

It turns out that the difference between these two models aren't huge --- the difference is within -350 to 300 interval throughout, and the plot is clearly similar as shown below:

.. image:: ./img/ARIMA502.png

.. image:: ./img/ARIMA702.png


ARIMA(p,2,q)
~~~~~~~~
Likewise, by observing the ACF and PACF, we found 1-4 significant lags in both ACF and PACF, thus run all 16 possible combinations of ARIMA, and select the following top two:

- ARIMA(1,2,4), which has the lowest BIC and the third lowest AIC;

- ARIMA(3,2,3), which has the second lowest BIC and the second lowest AIC.


The prediction, as shown below, are actually similar amongst the two. However, as one can see, perform poorly when facing spikes.

.. image:: ./img/ARIMA124.jpg

.. image:: ./img/ARIMA323.jpg


Comparing across
~~~~~~~~
In terms of information criterion, the two ARIMA(p,2,q) models have slightly lower information criteria for both AIC and BIC amongst the four. The difference amongst is tight though, within 2% of each other.

In terms of Mean Sum of Squared Errors (MSE), however, ARIMA(p,2,q) models perform much worse than the other --- 40-50 times larger than ARIMA(p,0,q)'s, which could be understood as ARIMA(p,2,q) models fail to predict precise large movements at the spike time.



Germany (DEU)
-----------
As an interest of this report in general, we also look at DEU's data. 

DEU's data is not as good as the American one --- it has more empty slots than the USA data, which makes less complete time series to run ARIMA fittings.

We start by the Dickey Fuller stationarity test, which gives a p-value of 0 up to the 5\ :sup:`th` significant level. Therefore we fit ARIMA(p,0,q) model for :math:`DEU_t`. 

By getting 1-5 significant lags via sample ACF and 1-2 significant lags via sample PACF, we get 10 possible combinations, and similar to the USA case, the top two are:

- ARIMA(5,0,2), which has the lowest BIC and the lowest AIC;
- ARIMA(3,0,2), which has the second lowest BIC and the third lowest AIC.

As shown below, peaks are nicely captured.

.. image:: ./img/DEUARIMA.png





VAR example: DEU and its neighbourhoods
=================

The concept of Vector Autoregression (VAR) is simply an ARIMA (p,0,0) model with :math:`X_{t}\in\mathbb{R}^n` where :math:`n\geq 2`, i.e. the variable is now a proper vector, rather than a scalar.

It comes to a natural question that which variables should one pick. As analysed above, and as per concerned by this report, DEU should be an obvious country to investigate. DEU's surrounding countries, which has various features, could also be included, as the transmission of influenza could thus be understood in such a broader-contingent way.

As a matter of geographical fact, (note: see `datasets section <datasets.html>`_ and the below map for further details. To use the dragging cursor, click on the play icon and select the second icon) Germany boarders with Denmark (DNK), Netherlands (NLD), Belgium (BEL), Luxembourg (LUX), France (FRA), Switzerland (CHE), Austria (AUT), Czech Republic (CZE), and Poland (POL). 

.. raw:: html

	<iframe src="_static/spatial_outbreak.html" height="530px" width="100%"></iframe>
`Figure link <https://public.tableau.com/profile/harrison4446#!/vizhome/outbreak_influenza/Spatialoutbreak/>`_. 


Now, by observing each individual countries, we found that NLD, DNK, POL, and CHE have no significant data before 2009, LUX has no data before 2003, AUT has no data before 2011, and FRA has no data before 2013. Hence, to run the VAR smoothly, we drop FRA and AUT, and only consider years after 2008. Additionally, CZE has numerous empty observations throughout, which would make the VAR restricted due to shrunk sample size. Hence CZE is dropped, too.

Hence, we now consider the remaining 8 countries together, and stuck them into our vector.

Due to data availability, the maximum p that would sustain the regression would be 8. Hence run all  :math:`p \in \{0,1,...,8\}` and find the one with the least Schwarz Bayesian Information Criterion (SBIC). We get  :math:`p =2` being optimal.

In order to compare whether VAR does good to our model fitting, we consider a univariate AR(p) model for DEU and see if by considering wider dataset, whether the VAR fitting could be of good. We run all possible p until 52, and by BIC, found :math:`p =3` to be optimal. The two models' fitting results as follows: 


.. image:: ./img/DEUcomparison.jpg


MSE suggests the baseline AR(3) model to be 20% better than the more advanced VAR(2) model, which is counter-intuitive. This fact can also be seen by the above graph, where VAR predictions seem to be jumping too largely at the event of outbreaks.
