
Initial Exploratory Data Analysis
==============


.. image:: ../img/dist.outbreak.who.png


.. image:: ../img/seasonEU.png


.. image:: ../img/Outbreak.eu.png


Models
===============

To obtain these pieces of information, we created two models, one to predict in the short term when and where influenza will strike, and another long-term model which predicts the severity of the influenza season.

The short-term model uses, to the best of our knowledge, a newly proposed Gaussian process mixture model with an XGBoost mean function, taking into account of geographical and spatiotemporal factors to identify, with high precision, when and where an outbreak will occur. During evaluation, we found that it performed well on predicting outbreaks in 2018, with an AUC of 0.762 and a false negative rate lying in a credible interval of (10.2%,13.1%). The surveillance system was also able to capture how influenza spreads spatiotemporally, as explained in the `Models section <models.html.html>`_.

We also have a Bayesian model that accurately predicts the severity of the next year's influenza season given the data from the current year. We find this model to also perform exceptionally well with PERFORMANCE DATA TO BE ADDED BY BENJAMIN.

Applications
==============


Based off this, we can make the following policy suggestions:



.. [#fludeaths] https://www.cdc.gov/media/releases/2017/p1213-flu-death-estimate.html
.. [#tbdeaths] https://www.who.int/tb/publications/global_report/en/
.. [#ustbdeaths] https://www.cdc.gov/tb/publications/factsheets/statistics/tbtrends.htm
.. [#usfludeaths] https://www.cdc.gov/flu/about/burden/2017-2018.htm
.. [#2009pandemic] https://www.who.int/mediacentre/news/statements/2009/h1n1_pandemic_phase6_20090611/en/
.. [#nhsbudget] https://www.theguardian.com/society/2018/may/22/hospitals-struggling-to-afford-new-equipment-after-nhs-budget-cuts
