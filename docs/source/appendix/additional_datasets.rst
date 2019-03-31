.. _additional_datasets:

==============================
Additional Datasets considered
==============================

CDC ILINet
=============

As analysis continued, we found that the FluNet was at times difficult to model due to the gradual increase in reported positive cases of influenza over time. In particular, after the 2009 influenza pandemic, far more influenza samples were detected as governments around the world took the threat of another influenza outbreak increasingly seriously. To alleviate this issue, alternative sources of data were investigated.

We found the Centers for Disease Control and Prevention (CDC), a government agency of the United States of America, monitors the spread of influenza-like illnesses (ILI) [#ili]_ via ILINet [#ilinet]_, and makes the data freely available online. Unlike the FluNet data, did not have a constantly increasing background. However, this data was only available for the US and so was deemed unsuitable for our usecase.

Physicians
=============

A factor that we believed may affect the spread of influenza was the number of physicians per unit population, which was provided in the :code:`health_indicators` dataset. While the data was clean when provided, there were numerous periods with missing data, resulting in the need for interpolation.

With the assumption that the measurements were made in the January of every year, monthly data was created using quadratic spline interpolation. This interpolation method was chosen for a number of reasons; we wanted to ensure that the interpolation equalled the actual measurements at the points the measurements were made, that the interpolation did not overfit the data, and that the interpolation was smooth, as the data would often go up and down. Quadratic spline interpolation satisfies all of this due to it being a smooth interpolation method with very few parameters.

There were also cases when there were only two measurements in total, in which case quadratic spline interpolation was not sensible so linear interpolation was used instead. Finally, in the case there was only one datapoint for a country, that value was set for the January of that year, and all other values were recorded as not available.

While this data was promising, we found that although it was a good variable to consider globally, for the region we investigated, Europe, the number of physicians was not a good explanatory variable as each nation had a slightly different healthcare system making each physician more or less effective.

Healthcare Expenditure
========================

While it is well-known that life expectancy correlates with total healthcare expenditure [#healthcareexpenditure]_, we also wanted to investigate its effects on controlling influenza. This was found by combining the domestic government healthcare expenditure per capita and domestic private healthcare expenditure per capita adjusted for purchasing power parity in current international dollars. This data was not interpolated as these budgets are usually set on an annual basis, and so the value for any time in each year was taken to be the value measured for that year.

We discarded this dataset for the same reason we discarded the dataset on physicians.

Smoking prevalence
========================

Although not commonly recognised as a risk factor for influenza, there have been small-scale studies that have indicated that it increases both the *risk* for contracting influenza and *severity* of such infections [#cigarettes]_. The data was extracted from the :code:`health_indicators` dataset. As smoking rates were linearly decreasing with time around the world, linear interpolation was found to be a good fit and  was used between the given measurements to find the smoking rate at any given time.

This dataset was discarded as the data was relatively consistent within Europe and there were a large number of missing values.

Number of hours worked
========================

So-called presenteeism, when ill workers come into work due to societal pressure and spread disease, can contribute to the spread of disease, with a study estimating that presenteeism costing the U.S. economy a staggering $150 billion a year [#presenteeism]_. We wanted to factor in presenteeism culture in different countries into our models; presumably, the higher the degree of presenteeism, the faster the spread of influenza. However, without expensive primary research, it is near impossible to estimate the degree of presenteeism and even then, it is not possible to extrapolate this data to the past.

Instead, we looked at the number of hours worked as a proxy for this. If there is a high degree of presenteeism, this should manifest in the number of hours that people work. This data was found for OECD countries in the form of number of hours worked per year [#workinghours]_. The value was processed so that the number of hours worked was constant through the calendar year as the measurements given were in the form of hours worked per year; it didn't make sense to divide the data any further as in reality there is seasonality to the number of hours worked per month.

We attempted to model influenza spread with a classical time-series model with this dataset as an explanatory variable as this appeared to be a promising approach after feature selection with ElasticNet. However, after much effort, we concluded that this model would not achieve our high standards and decided to cancel the project. More details on this are also included in the appendix.

Google Trends
================

There have been a number of attempts to use Google search data to model influenza prevalence, the most famous being Google Flu Trends [#googletrends]_. We decided to scrape all available data from Google Trends at a weekly resolution going back to 2004 to add as an input to our models. Google only allows querying 5 years at a time for weekly resolution data and normalises the data within that time range such that the most number of queries in the requested time period is 100, so we had to apply a scaling factor to normalise the data, which was calculated by getting a year overlap between queries and looking at the corresponding values. Furthermore, the Google Trends API accepts geographical codes in two-letter codes as opposed to the three-letter codes provided, so a short script was written to transform between the two.

We used the query terms of 'fever' and 'cough' as indications that people have the flu. The obvious terms 'influenza' and 'flu' were omitted as they scaled more with interest in the disease from media coverage than with the actual number of people infected. A problem with this dataset was that as the number of people using Google has been steadily increasing, the search count has been constantly increasing with time as well. This, along with the fact that the peaks in interest were virtually perfectly *aligned* with the influenza outbreaks as opposed to *leading* them meant that this dataset was not useful for predicting the future, and so this dataset was also discarded.

.. [#ili] A patient is defined to have an influenza-like illness when they have a fever of 37.8 °C or greater and a cough and/or sore throat in the absence of a known cause other than influenza. (https://gis.cdc.gov/grasp/fluview/FluViewPhase2QuickReferenceGuide.pdf)
.. [#ilinet] ILINet collects information on patient visits to healthcare providers for influenza-like illnesses, with data available online `here <https://gis.cdc.gov/grasp/fluview/fluportaldashboard.html>`_
.. [#healthcareexpenditure] https://ourworldindata.org/grapher/life-expectancy-vs-health-expenditure
.. [#cigarettes] A study of an outbreak of A(H1N1) influenza in an Israeli military unit with 336 healthy young men found that the smokers were ~1.4x more likely to contract influenza, and ~1.6x as likely to lose work days. (https://www.nejm.org/doi/full/10.1056/NEJM198210213071702)
.. [#presenteeism] https://www.forbes.com/sites/karenhigginbottom/2018/04/20/the-price-of-presenteeism-2/#4742f0f37f9c
.. [#workinghours] https://stats.oecd.org/index.aspx?DataSetCode=ANHRS
.. [#googletrends] http://static.googleusercontent.com/media/research.google.com/en/us/archive/papers/detecting-influenza-epidemics.pdf , https://www.mitpressjournals.org/doi/full/10.1162/NECO_a_00756#.Vu5zr0eAY4A
