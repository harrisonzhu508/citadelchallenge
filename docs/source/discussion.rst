.. _discussion:

==============
Discussion
==============

Thinking back to our initial question, *'How can we better allocate resources to contain influenza?'*, we made the models described in the :ref:`previous section <models>` so that we could predict the information we need to best allocate resources; the *time*, the *location*, and the *severity* of influenza outbreaks. As discussed in the :ref:`previous section <models>`, we know how to obtain accurate predictions for all of these factors, on numerous timescales. We believe that by deploying these models to policy makers, the clarity they provide could result in meaningful improvements being made to the prevention of influenza epidemics.

The long-term knowledge provided by the :ref:`Bayesian model <bayesian>` combined with its quantification of credible intervals allows us to budget accordingly on a yearly basis with confidence that 95% of the time, the preparations will be adequate to manage any outbreaks. We could even budget for each quarter based on the proportion of the population during that period.

Furthermore, if the observations deviate significantly from the predictions, this would give a strong indication that the influenza outbreak is approaching the level of an epidemic. A local authority should act swiftly on this data, instating more drastic measures such as social distancing strategies for those at risk, preventing the situation evolving into an actual epidemic.

The short-term knowledge provided by the :ref:`Gaussian Processes <gp>` can also inform immediate action. If deployed to policy makers, they can find the regions where an outbreak is predicted and instate some of the following measures to contain the spread of influenza to a bare minimum:

- If the outbreak is predicted far enough in advance, a swift deployment of vaccines to a region may limit the spread of influenza there.

- Public Service Announcements warning of a heightened risk of influenza in the coming week, encouraging the population to take preventative measures such as disinfecting hands, or ventilating living areas and to go to the doctors should they experience flu-like symptoms. This could be implemented in a similar manner to severe weather warnings.

- The transportation of antiviral drugs to the region in advance. As antiviral medication must be administered early (within 48 hours of first symptoms) [#antivirals]_, this measure would be especially effective in conjunction with the Public Service Announcements.

- It is well known that influenza outbreaks can occur in hospitals, which is of particular concern due to the number of at-risk individuals at these locations [#crossinfection]_. By informing healthcare professionals ahead of time, they could take extra caution, e.g. ensuring facemasks are worn by all staff and patients, or disinfecting surfaces more regularly, to prevent outbreaks.

These are just some of the ways influenza could be better contained given the data that our models provide, and we believe that in the hands of healthcare professionals who have decades of knowledge on how to contain influenza outbreaks, even more powerful and effective measures could be undertaken.

.. [#antivirals] https://www.tandfonline.com/doi/full/10.1586/14787210.4.5.795
.. [#crossinfection] https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(02)00221-9/fulltext
