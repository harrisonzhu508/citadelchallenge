=================
Bayesian Approach
=================

Motivation
============

A major infectious disease surveillance body, the Centre for Disease
Control in the US, currently deploy an adaptation [#first]_ for influenza modelling. The method uses
cyclic regression to model the weekly proportion of deaths from
pneumonia and influenza. Since then adaptations have incorporated
indicators such as counts of patient visits for influenza like illness
(ILI) [#second]_, [#third]_. However, regardless of modern modifications the methodology is limited by its unfounded assumption that observations are independent and
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
proceed to make probabilistic statements to inform policy makers.

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
a given week for a two year period. Whilst the model is agnostic to
geographical location, we focus on specifying the prior distribution in
line with European influenza cycles. The parameters are
:math:`\Theta = (X_{1:104},\mu, \theta, \alpha, \rho, \ell)`, with
notation defined as
:math:`(X_{1:104}) := (X_{1},...,X_{104})`. From which, we
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
:math:`\mu`, with :math:`\theta t` to describe secular trend, and a
suitably scaled and lagged sine function to capture seasonality.

The prior :math:`\pi(\Theta)` is composed of the following:

.. math::

   \begin{aligned}
   & X_{1}|\phi \stackrel{}{\sim} \mathcal{N}\Big(m_{1} ,\frac{50^2}{1-\rho^2}\Big) & & \mu \stackrel{}{\sim} \mathcal{U}(0,1000) \\
   & X_{27}|\phi \stackrel{}{\sim} \mathcal{N}\Big(m_{1} ,\frac{50^2}{1-\rho^2}\Big) & & \theta \stackrel{}{\sim} \mathcal{U}(0,0.5)  \\
   & X_{79}|\phi \stackrel{}{\sim} \mathcal{N}\Big(m_{1} ,\frac{50^2}{1-\rho^2}\Big) & & \rho \stackrel{}{\sim} \mathcal{U}(0.6,0.9) \\
   & X_{t}|X_{t-1}, \phi \stackrel{}{\sim} \mathcal{N}\Big(m_{t} + \rho(X_{t-1}-m_{t-1}), 50^2\Big) & & \ell \stackrel{}{\sim} \mathcal{U}(0.7,1) \\
   &      && \alpha \stackrel{}{\sim} \mathcal{U}(3000,25000)\end{aligned}

for :math:`t \in \{2,...,26,28,...,78,80,...,104\}`.

Given this prior model we have the following decomposition:

.. math::

   \begin{aligned}
    \pi(\Theta)  &=  \pi(X_{1:104}|\phi)\pi(\phi) \\
    &= \pi(X_{104}|X_{1:103},\phi)\pi(X_{1:103}|\phi)\pi(\phi) \\
    &= \pi(X_{104}|X_{103},\phi)\pi(X_{1:103}|\phi)\pi(\alpha)\pi(\rho)\pi(\ell)\pi(\theta)\pi(\mu)\\
    &= \bigg[\prod_{i=2}^{26}\pi(X_{i}|X_{i-1},\phi)\bigg]\pi(X_{1}|\phi)\bigg[\prod_{i=28}^{78}\pi(X_{i}|X_{i-1},\phi)\bigg]\pi(X_{27}|\phi)\\
    &\times \bigg[\prod_{i=80}^{104}\pi(X_{i}|X_{i-1},\phi)\bigg]\pi(X_{79}|\phi)
   \pi(\alpha)\pi(\rho)\pi(\ell)\pi(\theta)\pi(\mu)\end{aligned}

Observation Model
-----------------

We model a two year period above in order to make predictions for the
second year, given observations of the first. We observe the first year
of recorded counts of influenza infection with noise due to poor data
collection and miss-classification of illness. That is,

.. math::	

	 Y_{1:52} = X_{1:52} + (\epsilon_{i})_{i=1}^{52}

where :math:`\epsilon_{i} \stackrel{iid}{\sim} \mathcal{N}(0,1)`. Thus
we have

.. math:: \pi(X_{1:52}|\Theta) = \prod_{i=1}^{52}\mathcal{N}(Y_{i},1).

Simulating our prior model
--------------------------

Our prior model is a reductive representation of a complex random
phenomena, hence it is vital to evaluate the model for likeness to the
real world to ensure our posterior inference is justified.

We first consider 100,000 samples from the prior model in Figure XXX.
This graph demonstrates likeness to real observed data for Europe over
the past 5 years. Additionally, the credible
intervals plotted show a sufficiently large range of realisations. The
mean weekly flu count is 3934 (CI: 1313,6629) which further provide
reasonable fit to reality, for example, in 2018 the European weekly
average was 4611 patients.

.. image:: ./img/synthetic.png

It is important to scrutinise the prior for informativeness with respect
to quantities we are particularly interested in. In Figure XXX the
approximate distribution of average and maximum counts for 100,000
samples are given. Both are satisfactory, since they fall roughly
uniform across wide intervals. The weekly average of 4611 in 2018 falls
in the range of high density for the average, and the European 2018
maximum of 19,074 patients infected also sits in the high density region
of the approximate maximum. Both distributions reflect reality well and
do not over-inform.

.. image:: ./img/max.avg.png

A Quick Remark
~~~~~~~~~~~~~~

When choosing a prior it is important to consider alternatives. In this
project a range of distributions for each of the parameters
:math:`(\alpha, \rho, \ell, \mu, \theta)` were considered in order to
represent different states of knowledge. We verified that the results of
our analysis were not sensitive to this range of priors. For example in
our choice of :math:`\mu`, which provides a base-level for the weekly
mean :math:`m_{t}`, we considered variants of uniform, normal and
triangle distributions, for example
:math:`\mathcal{N}(10000,3),\mathcal{U}(3000,25000)` and
:math:`\text{Tri}(3000,25000,10000)`. We observed reasonable similarity
between the distributions and ultimately decided to work with the
uniform since it best represented our prior beliefs.

Model Choice
============

We are interested in understanding whether or not our current model,
:math:`\mathcal{M}_{1}`, is adequate. In doing so, we compare its
performance with alternative models whose difference with our current
model is the power of sine. That is, for alternative models
:math:`\mathcal{M}_{2}, \mathcal{M}_{3}, \mathcal{M}_{4}, \mathcal{M}_{5}`
and :math:`\mathcal{M}_{6}` we alter the weekly mean number of influenza
positive virus as:

.. math::

   \begin{aligned}
    \mathcal{M}_{2} &:  m_{t} = \mu + \theta t + \alpha sin^{10}\Big(\frac{\pi}{52}t - \ell\pi\Big) \\
    \mathcal{M}_{3} &:  m_{t} = \mu + \theta t + \alpha sin^{12}\Big(\frac{\pi}{52}t - \ell\pi\Big) \\ 
    \mathcal{M}_{4} &:  m_{t} = \mu + \theta t + \alpha sin^{16}\Big(\frac{\pi}{52}t - \ell\pi\Big) \\
    \mathcal{M}_{5} &:  m_{t} = \mu + \theta t + \alpha sin^{20}\Big(\frac{\pi}{52}t - \ell\pi\Big) \\ 
    \mathcal{M}_{6} &:  m_{t} = \mu + \theta t + \alpha sin^{30}\Big(\frac{\pi}{52}t - \ell\pi\Big)  \end{aligned}

Here a finite number of model comparisons is made. If one wants to
consider an infinite number of models a more delicate construction of
the unconditional probabilities :math:`(p_{i} : i \in \mathbf{N})` is
required (for example adhering to notions of coherence). Assuming an
equal prior weighting, we progress to consider Bayes factors.

Bayes factors depend on estimates of the marginal likelihood for the
observation in question, that is, the first year falling in line with
recorded data. We make use of the following consistent estimator:

.. image:: ./img/naive.png

When implemented using :math:`n=100,000` the approximation produced
unstable results despite efforts to reduce computational underflow. To
assess the evidence for accepting :math:`\mathcal{M}_{k}`,
:math:`k\neq 1`, over :math:`\mathcal{M}_{1}` we compute the Bayes
factor for the best performing of
:math:`\mathcal{M}_{2},...\mathcal{M}_{6}` against
:math:`\mathcal{M}_{1}`. In 10 runs we realised a range of
:math:`(0.004,12.656)` with the Naive approximation. However, the
particular :math:`\mathcal{M}_{k}` with the best performance was
consistently :math:`\mathcal{M}_{1}`. For this reason we proceed with
:math:`\mathcal{M}_{1}`.

Posterior sampling
==================

Now content with the prior model we proceed to generate approximate
samples of the posterior distribution given observed European data.
Whilst it would be possible to generate true posterior samples, for
example by using Metropolis Hastings and assessing the quality of fit
with ACFs, trace plots and checking that marginal distributions agree,
we rather deploy ABC to generate approximate uncorrelated samples.

Approximate Bayesian Computation
--------------------------------

With the aim to make probabilistic statements about 2019 we deploy
approximate Bayesian computation to target the posterior. In doing so,
we generate samples from :math:`\pi(\Theta|Y_{1:52})` where
:math:`Y_{1:52}` are given by the influenza\_activity.csv.

Below we observe the first year of some synthetic data, with samples
accepted by ABC in green. These samples provide a satisfactory fit to
the observed process.

.. image:: ./img/ABC.png

Results
=======

Using the posterior distribution we can inform policy makers about the
probability of particular magnitude outbreaks, allowing
for improved emergency planning and resource allocation. The methodology
further provides an opportunity to look at the posterior for different regions of a country. Medical professionals can then
strategically allocate their resources within their country to areas with higher probability of outbreak. 

To demonstrate its usefullness we consdier 2018 model predictions given 2017 cycle observations. Below we find that the observation for 2018 fell within our reasonablly tight HPD interval. Given that the European Centre for Disease Prevention and Control recognised 2018 as reasonably large season we are encoraged by the fact the observations still fell within our bounds [#forth]_. Note we observe the peak of the season above the mean prediction. 

.. image:: ./img/forecast2018.png

Returning to 2018 observations for 2019 predictions, we observe an expected maximum number of viruses
testing positive for influenza at 14,487 with a 95% credible interval of
(3882,24675) in the prior. This expected maximum shifts to 19,413 in the posterior
with a 95% credible interval at (14507,20085). Below we also produce the expected flu cycle for 2019 with 95% HPD intervals. This can provide an alternative epidemic threshold to that currently used by the Centre for Disease Control.

.. image:: ./img/eu2019.png

Shortcomings
=======

Whilst we achieved success in developing a model that reframed and extended the existing approach, there are a few shortcomings to be mentioned. Firstly, it is generally difficult to assess whether arbitrary features of the prior do not predominate our posterior analysis. The question of robustness has been tackled in the literature and further work could extend this by considering the prior belonging to a class of distributions as proposed by Berger’s classification [#five]_. Attempts could then be made to derive bounds on posterior quantities and hence produce analysis less sensitive to the choice of prior. 

Beyond criticism of the arbitrariness and importance of the prior, we consider the use of ABC. The applications of ABC are often based on improved versions of the basic rejection scheme [#six]_, and have already yielded valuable insights into questions concerning the rate of spread of pathogens [#seven]_, [#eight]_. Past applications have typically focused on parameter estimation rather than posterior prediction. In our case, ABC provides the benefit of independant samples. However, true posterior samples could be found by the implimentation of Hamiltonian Monte Carlo [#nine]_. 

Finally, the Naive approximation of Bayes factors in this setting proved unstable. Future work could focus on deploying more stable estimators for the marginal likelihood, such as a Harmonic approximation.


.. [#first] Robert E. Serfling. (1963). Methods for Current Statistical Analysis of Excess Pneumonia-Influenza Deaths. Public Health Reports (1896-1970), 78(6), 494-506. doi:10.2307/4591848
.. [#second] L. Simenson, K. Fukuda, L. B. Schonberg, and N. J. Cox. The impact of influenza epidemics on hospitalizations. The Journal of Infectious Diseases, 181:831–837, 2000.
.. [#third] F. C. Tsui, M. M. Wagner, V. Dato, and C. C. H. Chang. Value ICD-9-Coded chief complaints for detection of epidemics. In Proceedings of the Annual AMIA Fall Symposium, 2001.
.. [#forth] https://ecdc.europa.eu/en/seasonal-influenza/season-2017-18
.. [#five] (Berger’s (1990a))
.. [#six] Beaumont, M.A. et al. (2002) Approximate Bayesian Computation in population genetics. Genetics 162, 2025–2035
.. [#seven] Tanaka, M. et al. (2006) Estimating tuberculosis transmission parameters from genotype data using approximate Bayesian computation. Genetics 173, 1511–1520
.. [#eight] Shriner, D. et al. (2006) Evolution of intrahost HIV-1 genetic diversity during chronic infection. Evolution 60, 1165–1176
.. [#nine] https://arxiv.org/abs/1701.02434
















