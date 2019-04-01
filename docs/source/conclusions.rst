==============
Conclusions
==============

Through our research, we were able to produce two models that respectively excelled at different parts of predicting influenza outbreaks. We have a :ref:`novel Gaussian Process-based model <gp>` that predicting *when* and *where* an influenza outbreak will occur in the short term, and a :ref:`Bayesian model <bayes>` that meaningfully improves on the state-of-the art predictions for *how serious* an influenza outbreak will be.

The Gaussian Process-based model predicts outbreaks with good accuracy, achieving an AUC of 0.762 and a false negative rate lying in a credible interval of (10.2%, 13.1%), despite the wildly unbalanced dataset.

The Bayesian model correctly predicted the 2018 flu season's magnitude, with the actual values lying comfortably within the predicted 95% credible interval.

As described in the :ref:`Discussion section <discussion>`, policy makers could take advantage of the accurate predictive information provided by these models to take appropriate measures to prevent and contain influenza outbreaks. Some of these potential measures include allocating quarterly budgets based on the long-term predictions of Bayesian models, early declaration of epidemics if the infection values lie above the 95% credible interval from the Bayesian models, and heightening preventative measures/stockpiling resources should an outbreak be predicted by the Gaussian Process-based model.

Based off our research, we believe that the answer to the question

*'How can we better allocate resources to contain influenza?'*

is as follows:

*We can better allocate resources to contain influenza by creating accurate predictive models which allow budgets to be made and preventative measures to be taken that will effectively contain any outbreaks before they can become epidemics.*
