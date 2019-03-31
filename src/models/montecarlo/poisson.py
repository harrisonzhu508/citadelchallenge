import gc
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use('seaborn-darkgrid')
import gc
gc.collect()
import pymc3 as pm


train = pd.read_csv("../../../data/processed/modelling_data/weekly_SWEurope_train.csv")
train = train.dropna()
test = pd.read_csv("../../../data/processed/modelling_data/weekly_SWEurope_test.csv")
test = test.dropna()

fml = 'num_influenza ~ year + week + year:(temperature + CapitalLatititude\
                      + CapitalLongitude)'
with pm.Model() as model:

  pm.glm.GLM.from_formula('num_influenza ~ year + week'\
                          , train, family=pm.glm.families.Poisson())
  poisson_regression_model = pm.sample(2000, chains=1, tune=1000)

pm.traceplot(trace)
