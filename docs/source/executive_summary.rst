=================
Efficient resource allocation during influenza cycles
=================

Introduction
==============

It is estimated that every year, more than 291,000 people die from seasonal flu-related illnesses [#fludeaths]_. While there are diseases that cause more deaths, we know how to virtually completely prevent them. For example, tuberclosis claimed 1.6 million deaths in 2017 [#tbdeaths]_, but only around 500 of those deaths were in the United States [#ustbdeaths]_. Diseases like tuberclosis, cholera, or measles have been effectively 'solved' in developed countries. All that we need to do is to 'port' these solutions to the developing world. It may cost money, it may take time, but we know what works.

Influenza is different. Approximately 80,000 people died in the United States in 2017 alone [#usfludeaths]_, and as recently as 2009, the World Health Organisation declared an influenza pandemic [#2009pandemic]_. Especially with  influenza's extremely fast rate of mutation, it is unlikely that we will be able to find a fundamental solution to influenza any time in the near future, making it vital that we find ways to contain the spread of influenza.

As can be seen from the constant budget crises facing the British National Health Services [#nhsbudget]_, our society seems to have priorities other than human life. It is therefore of paramount importance that we allocate the limited resources available to most effectively contain influenza and minimise its impact. We will be focussing on the developed world to ensure that the hypotheses we explore and the policies we propose go beyond the state-of-the-art.

To answer our question of how to better allocate resources to contain influenza, we must first think about what information we need to make these decisions. We believe that to make the best decisions, what we need to be able to do is predict, ahead of time, when, and with what severity a region will be impacted by influenza. Once we know that, we can simply apply procedures that would usually be applied after we find an influenza outbreak, but apply it earlier, to contain the disease before it can spread.

Models
===============

To obtain these pieces of information, we created two models, one to predict in the short term when and where influenza will strike, and another long-term model which predicts the severity of the influenza season.

The short-term model uses, to the best of our knowledge, a newly proposed Gaussian process mixture model with an XGBoost mean function, taking into account of geographical and spatiotemporal factors to identify, with high precision, when and where an outbreak will occur. During evaluation, we found that it performed well on predicting outbreaks in 2018, with an AUC of 0.762 and a false negative rate lying in a credible interval of (10.2%,13.1%). The surveillance system was also able to capture how influenza spreads spatiotemporally, as explained in the `Models section <models.html.html>`_.

We also have a Bayesian model that accurately predicts the severity of the next year's influenza season given the data from the current year. We find this model to also perform exceptionally well with PERFORMANCE DATA TO BE ADDED BY BENJAMIN.

Applications
==============


Based off our analysis, we can make the following policy suggestions:



.. [#fludeaths] https://www.cdc.gov/media/releases/2017/p1213-flu-death-estimate.html
.. [#tbdeaths] https://www.who.int/tb/publications/global_report/en/
.. [#ustbdeaths] https://www.cdc.gov/tb/publications/factsheets/statistics/tbtrends.htm
.. [#usfludeaths] https://www.cdc.gov/flu/about/burden/2017-2018.htm
.. [#2009pandemic] https://www.who.int/mediacentre/news/statements/2009/h1n1_pandemic_phase6_20090611/en/
.. [#nhsbudget] https://www.theguardian.com/society/2018/may/22/hospitals-struggling-to-afford-new-equipment-after-nhs-budget-cuts
