======================================================
How long will the epidemic last?
======================================================

Introduction
==============

Our other two models tell us when and where the epidemics will strike, and how hard. The final factor we need to better allocate resources is to know how long such an episode will last. We hypothesise that we may be able to explain which regions have long-lasting influenza seasons by looking at variables that we haven't investigated yet that may increase the 'risk factor' of a nation to staying in a state of high influenza infection rates.

We first collect a number of variables, both social and physical, as described in :ref:`the datasets section <datasets>`. We then construct a simple elastic net model [#elasticnet]_ , i.e. we minimise the objective function

.. math::

    \min_{w} { \frac{1}{2n_{samples}} ||X w - y||_2 ^ 2 + \alpha \rho ||w||_1 + \frac{\alpha(1-\rho)}{2} ||w||_2 ^ 2}

to perform variable selection. This model will have a set of coefficients that represent the way that each variable correlates with the output. To ensure that we could properly see which variables were most significant, we normalise all the input features to be between 0 and 1. We train the model on developed countries to control for underdeveloped countries having other unaccounted factors that will skew our results. We observe the following coefficients as a result of running this process::

    Minimum temperature :  -35.75207412089624
    Maximum temperature :  -27.572710323493112
    Precipitation :  -1.1936198807223342
    Climate water deficit :  0.9117976671368961
    Actual evapotranspiration :  -25.67468313304453
    Downward surface shortwave radiation :  -15.056164498685526
    Vapour pressure :  -8.59360337613683
    Hours worked per year :  48.18539588156608
    Total healthcare expenditure per capita, adjusted for PPP :  21.214423216995893
    Number of physicians per capita :  -36.074258171081844

As we know and expect, the higher the temperature, the fewer the positive instances of influenza [#temperatureflu]_. What is surprising is the high positive coefficient for the hours worked per year. While we would expect for there to be some type of

Theory
=========

Results
============

Performance
-------------

Application to 2018
--------------------

Limitations
===============

.. [#elasticnet] https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.124.4696
.. [#temperatureflu] https://jvi.asm.org/content/88/14/7692s
