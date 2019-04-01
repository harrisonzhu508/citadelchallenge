=================
Executive Summary
=================

Introduction
==============

It is estimated that every year, more than 291,000 people die from seasonal flu-related illnesses [#fludeaths]_. While there are diseases that cause more deaths, we know how to virtually completely prevent them. For example, tuberclosis claimed 1.6 million deaths in 2017 [#tbdeaths]_, but only around 500 of those deaths were in the United States [#ustbdeaths]_. Diseases like tuberclosis, cholera, or measles have been effectively 'solved' in developed countries. All that we need to do is to 'port' these solutions to the developing world. It may cost money, it may take time, but we know what works.

Influenza is different. Approximately 80,000 people died in the United States in 2017 alone [#usfludeaths]_, and as recently as 2009, the World Health Organisation declared an influenza pandemic [#2009pandemic]_. Especially with  influenza's extremely fast rate of mutation, it is unlikely that we will be able to find a fundamental solution to influenza any time in the near future, making it vital that we find ways to contain the spread of influenza.

As can be seen from the constant budget crises facing the British National Health Services [#nhsbudget]_, our society seems to have priorities other than human life. It is therefore of paramount importance that we allocate the limited resources available to most effectively contain influenza and minimise its impact. We will be focussing on the developed world to ensure that the hypotheses we explore and the policies we propose go beyond the state-of-the-art.

To answer our question of how to better allocate resources to contain influenza, we must first think about what information we need to make these decisions. We believe that to make optimal decisions we must be able to predict, ahead of time, when, and with what severity a region will be impacted by influenza. Once we have that information, we can simply apply procedures that would usually be applied after we find an influenza outbreak, but apply it earlier, to contain the disease before it can spread.

Models
===============

To obtain these pieces of information we created two models, one to predict in the short term when and where influenza will strike, and another long-term model which predicts the severity of the influenza season.

The short-term model uses, to the best of our knowledge, a newly proposed Gaussian process mixture model with an XGBoost mean function, taking into account geographical and spatiotemporal factors to identify, with high precision, when and where an outbreak will occur. During evaluation we found that it performed well on predicting outbreaks in 2018, with an AUC of 0.762 and a false negative rate lying in a credible interval of (10.2%, 13.1%). The surveillance system was also able to capture how influenza spreads spatiotemporally, as explained in the `Models section <models.html.html>`_.

We also developed a Bayesian model that accurately predicts the severity of next year's influenza season given the data from the current year. We found this model to also perform well, with demonstration on the European 2018 cycle, with all of the values falling within our credible interval.

Applications
==============

The long-term knowledge provided by the Bayesian model combined with its quantification of credible intervals allows us to budget accordingly on a yearly basis with confidence that 95% of the time, the preparations will be adequate to manage any outbreaks. We could even budget for each quarter based on the proportion of the population during that period.

Furthermore, if the observations deviate significantly from the predictions, this would give a strong indication that the influenza outbreak is approaching the level of an epidemic. A local authority should act swiftly on this data, instating more drastic measures such as social distancing strategies for those at risk, preventing the situation evolving into an actual epidemic.

The short-term knowledge provided by the Gaussian Processes can also inform immediate action. If deployed to policy makers, they can find the regions where an outbreak is predicted and instate some of the following measures to contain the spread of influenza to a bare minimum:

- If the outbreak is predicted far enough in advance, a swift deployment of vaccines to a region may limit the spread of influenza there.

- Public Service Announcements warning of a heightened risk of influenza in the coming week, encouraging the population to take preventative measures such as disinfecting hands, or ventilating living areas and to go to the doctors should they experience flu-like symptoms. This could be implemented in a similar manner to severe weather warnings.

- The transportation of antiviral drugs to the region in advance. As antiviral medication must be administered early (within 48 hours of first symptoms) [#antivirals]_, this measure would be especially effective in conjunction with the Public Service Announcements.

- It is well known that influenza outbreaks can occur in hospitals, which is of particular concern due to the number of at-risk individuals at these locations [#crossinfection]_. By informing healthcare professionals ahead of time, they could take extra caution, e.g. ensuring facemasks are worn by all staff and patients or disinfecting surfaces more regularly, to prevent outbreaks.

These are just some of the ways influenza could be better contained given the data that our models provide, and we believe that in the hands of healthcare professionals who have decades of knowledge on how to contain influenza outbreaks, even more powerful and effective measures could be undertaken.

Conclusions
===============

Based off our research, we believe that the answer to the question

*'How can we better allocate resources to contain influenza?'*

is as follows:

*We can better allocate resources to contain influenza by creating accurate predictive models which allow budgets to be made and preventative measures to be taken that will effectively contain any outbreaks before they can become epidemics.*


.. [#fludeaths] https://www.cdc.gov/media/releases/2017/p1213-flu-death-estimate.html
.. [#tbdeaths] https://www.who.int/tb/publications/global_report/en/
.. [#ustbdeaths] https://www.cdc.gov/tb/publications/factsheets/statistics/tbtrends.htm
.. [#usfludeaths] https://www.cdc.gov/flu/about/burden/2017-2018.htm
.. [#2009pandemic] https://www.who.int/mediacentre/news/statements/2009/h1n1_pandemic_phase6_20090611/en/
.. [#nhsbudget] https://www.theguardian.com/society/2018/may/22/hospitals-struggling-to-afford-new-equipment-after-nhs-budget-cuts
.. [#antivirals] https://www.tandfonline.com/doi/full/10.1586/14787210.4.5.795
.. [#crossinfection] https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(02)00221-9/fulltext
