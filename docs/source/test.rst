=================
Bayesian Approach
=================

Introduction
============

A major infectious disease surveillance body, the Centre for Disease
Control in the Untied States, currently deploy an adaptation of
Serfling’s method (cite here) for influenza modelling. The method uses
cyclic regression to model the weekly proportion of deaths from
pneumonia and influenza. Since then adaptations have incorporated
indicators such as counts of patient visits for influenza like illness
(ILI). However, regardless of modern modifications the methodology has a
particular flaw in its assumption that observations are independent and
identically distributed.

In this section we attempt to shift the methodology towards the Bayesian
framework in order to provide better epidemic thresholds that are
adjusted for seasonal effects. In doing so, we build prior and
observation models for the number of individuals infected by influenza
within a specific region. After building the models we simulate from the
prior to test its likeness to reality and ensure the prior model is
sufficiently grounded in reality to produce justified posterior
inference. Once we are satisfied with the model we deploy Approximate
Bayesian Computation (ABC) to generate approximate posterior samples and
proceed to make pobabilistic statements to inform policy makers.

Prior Elicitation
=================

We begin by outlining the prior and observation models in this setting.
Whilst the systematic use of parameterised distributions is not always
justifiable, when building the prior we arbitrarily restrict ourselves
to a parameterised density where we can make subjective evaluations of
the parameters in line with our knowledge of the world.

Prior Model
-----------

We build a model for the number of individuals infected by influenza in
a given week for a two year period. The parameters are
:math:`\Theta = (X_{1:104},\mu, \theta, \alpha, \rho, \ell)`, with
notation defined as
:math:`(X_{1:104}) \vcentcolon= (X_{1},...,X_{104})`. From which, we
model the weekly flu process :math:`(X_{i})_{i=1}^{104}` over a 2 year
period (for example 2018 to 2019) as a weekly mean with an
autoregressive process. By considering the seasonality of infection
count we use a single AR process for each winter, since these winters
vary in strands of influenza active, health care spending, temperature
and so on. Hence we have, :math:`X_{t}|X_{t-1},\phi = m_{t}+y_{t}` with
:math:`y_{t} \stackrel{}{\sim} AR(\rho,50)` and
:math:`\phi = (\mu, \theta, \rho, \ell, \alpha)`. The mean in week
:math:`t` is given by

.. math:: m_{t} = \mu + \theta t + \alpha sin^8\Big(\frac{\pi}{52}t - \ell\pi\Big)

That is to say the weekly mean is a baseline infection count
:math:`\mu`, :math:`\theta t` to describe secular trend, and a suitably
scaled and lagged sine function to capture seasonality.

The prior :math:`\pi(\Theta)` is composed of the following:
