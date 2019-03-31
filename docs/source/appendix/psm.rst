=================
Presenteeism
=================

Motivation & Introduction
======

The current models we have do not take into account social factors, and we believed we may be able to create an effective model by incorporating this data. We hypothesised that we may be able to explain which regions are more severely affected by influenza by looking at variables that we haven't investigated yet that may increase the 'risk factor' of a nation to staying in a state of high influenza infection rates.

We first collect a number of variables, both social and physical, as described in :ref:`the datasets section <datasets>` and :ref:`the additional datasets section <additional_datasets>`. We then construct a simple elastic net model [#elasticnet]_ , i.e. we minimise the objective function

.. math::

    \min_{w} { \frac{1}{2n_{samples}} ||X w - y||_2 ^ 2 + \alpha \rho ||w||_1 + \frac{\alpha(1-\rho)}{2} ||w||_2 ^ 2}

to perform variable selection. This model has a set of coefficients that represent the way that each variable correlates with the output. To ensure that we could properly see which variables were most significant, we normalise all the input features to be between 0 and 1. We train the model on developed countries to control for underdeveloped countries having other unaccounted factors that will skew our results. We observe the following coefficients as a result of running this process::

    Minimum temperature :  -35.75207412089624
    Maximum temperature :  -27.572710323493112
    Precipitation :  -1.1936198807223342
    Climate water deficit :  0.9117976671368961
    Actual evapotranspiration :  -25.67468313304453
    Downward surface shortwave radiation :  -15.056164498685526
    Vapour pressure :  -8.59360337613683
    Hours worked per year :  48.18539588156608
    Total healthcare expenditure per capita, adjusted by PPP :  21.214423216995893
    Number of physicians per capita :  -36.074258171081844

As we know and expect, the higher the temperature, the fewer the positive instances of influenza [#temperatureflu]_. What is surprising is the high positive coefficient for the hours worked per year. While some degree of correlation was expected, the extremely large coefficient, significantly larger than any other known factor, motivated us to create a model using this as a explanatory factor.

We believe that a potential explanation for this is the effect of presenteeism culture. So-called presenteeism, when ill workers come into work due to societal pressure and spread disease, can contribute to the spread of disease, with a study estimating that presenteeism costing the U.S. economy a staggering $150 billion a year [#presenteeism]_, and we can reasonably assume that the number of hours worked per year correlates with presenteeism culture.

Methodology
=====

We obtain the working hour of dependent work data from OECD dataset during 2000-2017, and as is aimed by the report, the focus is restricted to the Europe region outlined by WHO. Amongst the 24 countries who reported, a yearly average is calculated, above which gets allocated to the group PRES (Presenteeism), and the rest to the group ABS (Absenteeism). There are 10 countries which stays in ABS throughout 2000-2017, 10 countries in PRES throughout, and the remaining 4 has switched for at least once. Those 4 are ruled out of the dataset for simplicity. Full breakdown can be seen in the below map.

.. image:: ../img/pmap2.png





Construction
~~~~~~

Descriptive Statistics
~~~~

Time Series
~~~~~~

.. [#elasticnet] https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.124.4696
.. [#temperatureflu] https://jvi.asm.org/content/88/14/7692s
.. [#presenteeism] https://www.forbes.com/sites/karenhigginbottom/2018/04/20/the-price-of-presenteeism-2/#4742f0f37f9c
