.. _datasets:

=================
Datasets
=================

While most of the data we required was provided, and already in a fairly structured form, we had to take care to process data to account for missing data, at times interpolating between data points. This section will outline the procedures undertaken to obtain/clean the data for each dataset used. Missing data in general was marked as :code:`N/A` and the time steps where such data occurred were disregarded during modelling.

Influenza Data
=================

WHO FluNet
-----------

As the project was focussed on the spread of influenza, the logical choice was to use the WHO FluNet database, provided in the :code:`influenza_activity` dataset. As the different types of influenza have similar levels of symptoms, we decided that the field of most interest was the number of total detected influenza viruses as opposed to the data for each subtype of influenza. This also had the advantage of giving us more data to work with; many countries recorded total influenza activity while not necessarily recording data for each type of influenza.

The dataset was relatively clean and didn't require further cleaning, and any dates with missing values were ignored. To create predictive models, a large number of other datasets were also created and joined with this dataset using the :code:`country_code` as the primary key.

The dataset was used as-is but a version was also made where the data was collected such that it was at a monthly timescale as opposed to a weekly one, due to many of the other variables having a monthly or yearly timescale.

As analysis continued, we found that this data was at times difficult to model due to its gradual increase over time. In particular, after the 2009 influenza pandemic, far more influenza samples were detected as governments around the world took the threat of another influenza outbreak increasingly seriously. To alleviate this issue, alternative sources of data were investigated.

CDC ILINet
------------

We found the Centers for Disease Control and Prevention (CDC), a government agency of the United States of America, monitored the spread of influenza-like illnesses (ILI) [#ili]_ via ILINet [#ilinet]_, and this data was freely available online. As the data is restricted exclusively to the US, it was not suitable for some of our usecases, but unlike the FluNet data, did not have a constantly increasing background.

Physicians
============

A factor that we believed was likely to affect the spread of influenza was the number of physicians per unit population, which was provided in the :code:`health_indicators` dataset. While the data was clean when provided, there were numerous periods with missing data, resulting in the need for interpolation.

With the assumption that the measurements were made in the January of every year, monthly data was created using quadratic spline interpolation. This interpolation method was chosen for a number of reasons; we wanted to ensure that the interpolation equalled the actual measurements at the points the measurements were made, that the interpolation did not overfit the data, and that the interpolation was smooth, as the data would often go up and down. Quadratic spline interpolation satisfies all of this due to it being a smooth interpolation method with very few parameters.

There were also cases when there were only two measurements in total, in which case quadratic spline interpolation was not sensible so linear interpolation was used instead. Finally, in the case there was only one datapoint for a country, that value was set for the January of that year, and all other values were recorded as not available.

Healthcare Expenditure
========================

While it is well-known that life expectancy correlates with total healthcare expenditure [#healthcareexpenditure]_, we also wanted to investigate its effects on controlling influenza. This was found by combining the domestic government healthcare expenditure per capita and domestic private healthcare expenditure per capita adjusted for purchasing power parity in current international dollars. This data was not interpolated as these budgets are usually set on an annual basis, and so the value for any time in each year was taken to be the value measured for that year.

Smoking prevalence
===================

Although not commonly recognised as a risk factor for influenza, there have been small-scale studies that have indicated that it increases both the *risk* for contracting influenza and *severity* of such infections [#cigarettes]_. The data was extracted from the :code:`health_indicators` dataset. As smoking rates were linearly decreasing with time around the world, as can be seen in the case of the United States

INSERT FIGURE HERE,

 linear interpolation was used between the given measurements to find the smoking rate at any given time.

Number of hours worked
========================

So-called presenteeism, when ill workers come into work due to societal pressure and spread disease, can contribute to the spread of disease, with a study estimating that presenteeism costing the U.S. economy a staggering $150 billion a year [#presenteeism]_. We wanted to factor in presenteeism culture in different countries into our models; presumably, the higher the degree of presenteeism, the faster the spread of influenza. However, without expensive primary research, it is near impossible to estimate the degree of presenteeism and even then, it is not possible to extrapolate this data to the past.

Instead, we looked at the number of hours worked as a proxy for this. If there is a high degree of presenteeism, this should manifest in the number of hours that people work. This data was found for OECD countries in the form of number of hours worked per year [#workinghours]_. The value was processed so that the number of hours worked was constant through the calendar year as the measurements given were in the form of hours worked per year; it didn't make sense to divide the data any further as in reality there is seasonality to the number of hours worked per month.

Spatiotemporal Data
================

Influenza viruses can survive much longer at low humidity and low temperatures, partially contributing to the seasonality of flu outbreaks [#flutemp]_. 

We obtained the coordinates of the capitals of each country and performed an SQL left join of ``influenza`` on
the coordinates. We picked the coordinates of the capitals because these would usually indicate the regions with
most of the population.

To use the dragging cursor, click on the play icon and select the second icon.

We can make the following observations.

- Influenza outbreaks seems to appear in clusters of regions. Especially for Europe and Central + South America.
One of our goals could be to identity how the spread occurs over space and time.
- There are more outbreak reports in Europe and fewer in South America. This may be due to better surveying and medical
infrastructure in Europe. Another subject of study for us would be to use the existing data for 
South America to interpolate what could happen in countries where there is little or no observation, 
using a spatiotemporal model.

.. raw:: html

	<iframe src="_static/spatial_outbreak.html" height="530px" width="100%"></iframe>
`Figure link <https://public.tableau.com/profile/harrison4446#!/vizhome/outbreak_influenza/Spatialoutbreak/>`_. Our previous visualisation and studies view that there is a yearly seasonality. Many recent studies have been 
on studying the relationship of spatiotemporal spread of influenza and diseases over a particular regional clusters. 
For example, Bhatt et al., 2017 looked at mapping disease over space-time using a GP in sub-Saharan Africa, 
Chen et al, 2019 looked at seasonal influenza spread in Shenzhen, China and Senanayake et al., 2016 on weekly flu
occurrence in the USA. 

Motivated by Bhatt et al., 2017, we use live satellite imagery (NOOA, MODIS, TERRACLIMATE) 
to obtain aggregated remote sensing data of temperature, precipitation, 
humidity etc... to augment our existing feature space. The data can be found from 
Google Earth Engine API (Gorelick et al., 2017) newly-developed by Google. An extraction pipeline is illustrated below.

.. image:: ./img/ee_pipeline.png

Using Lasso regularised regression, we select the following features for our Gaussian process model

- Capital city latitude 
- Capital city longitude 
- Weekly temperature 
- Evapotranspiration, derived using a one-dimensional soil water balance model 
- Surface pressure
- Surface Height
- Year 
- Month

In particular, we found that spatial, temporal and the number of physicians to be highly 
significant features to the occurrence of influenza.

Google Trends
================

There have been a number of attempts to use Google search data to predict influenza prevalence, the most famous being Google Flu Trends [#googletrends]_. We decided to scrape all available data from Google Trends at a weekly resolution going back to 2004 to add as an input to our models. Google only allows querying 5 years at a time for weekly resolution data and normalises the data within that time range such that the most number of queries in the requested time period is 100, so we had to apply a scaling factor to normalise the data, which was calculated by getting a year overlap between queries and looking at the corresponding values. Furthermore, the Google Trends API accepts geographical codes in two-letter codes as opposed to the three-letter codes provided, so a short script was written to transform between the two.

We used the query terms of 'fever' and 'cough' as indications that people have the flu. The obvious terms 'influenza' and 'flu' were omitted as they scaled more with interest in the disease from media coverage than with the actual number of people infected. A problem with this dataset was that as the number of people using Google has been steadily increasing, the search count has been constantly increasing with time as well, as can be seen in the graph below (TO BE ADDED). To get around this, WHAT CAN WE DO?

.. [#ili] A patient is defined to have an influenza-like illness when they have a fever of 37.8 °C or greater and a cough and/or sore throat in the absence of a known cause other than influenza. (https://gis.cdc.gov/grasp/fluview/FluViewPhase2QuickReferenceGuide.pdf)
.. [#ilinet] ILINet collects information on patient visits to healthcare providers for influenza-like illnesses, with data available online `here <https://gis.cdc.gov/grasp/fluview/fluportaldashboard.html>`_
.. [#healthcareexpenditure] https://ourworldindata.org/grapher/life-expectancy-vs-health-expenditure
.. [#cigarettes] A study of an outbreak of A(H1N1) influenza in an Israeli military unit with 336 healthy young men found that the smokers were ~1.4x more likely to contract influenza, and ~1.6x as likely to lose work days. (https://www.nejm.org/doi/full/10.1056/NEJM198210213071702)
.. [#presenteeism] https://www.forbes.com/sites/karenhigginbottom/2018/04/20/the-price-of-presenteeism-2/#4742f0f37f9c
.. [#workinghours] https://stats.oecd.org/index.aspx?DataSetCode=ANHRS
.. [#flutemp] http://sitn.hms.harvard.edu/flash/2014/the-reason-for-the-season-why-flu-strikes-in-winter/
.. [#googletrends] http://static.googleusercontent.com/media/research.google.com/en/us/archive/papers/detecting-influenza-epidemics.pdf , https://www.mitpressjournals.org/doi/full/10.1162/NECO_a_00756#.Vu5zr0eAY4A
