import csv
from sklearn import linear_model
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt


class VariableNames:
    country_code = 'country_code'
    capital_lat = 'CapitalLatitude'
    capital_long = 'CapitalLongitude'
    region_name = 'who_region'
    tmmn = 'tmmn'
    tmmx = 'tmmx'
    pr = 'pr'
    def_ = 'def'
    aet = 'aet'
    srad = 'srad'
    vap = 'vap'
    ndvi = 'NDVI'
    hours_worked = 'Hours_worked_per_year'
    expenditure_ppp = 'expenditure_PPP'
    num_physician = 'num_physician'
    smoking = 'smoking'
    year = 'year'
    month = 'month'
    num_positive = 'num_influenza_positive'


regions_interested = ["European Region of WHO"]
# regions_interested = ["Region of the Americas of WHO"]
# regions_interested = ["Western Pacific Region of WHO"]
variables_interested = [VariableNames.capital_lat,
                        VariableNames.capital_long,
                        VariableNames.tmmn,
                        VariableNames.tmmx,
                        VariableNames.pr,
                        VariableNames.def_,
                        VariableNames.aet,
                        VariableNames.srad,
                        VariableNames.vap,
                        VariableNames.ndvi,
                        VariableNames.hours_worked,
                        VariableNames.expenditure_ppp,
                        VariableNames.num_physician,
                        VariableNames.smoking,
                        VariableNames.year,
                        VariableNames.month,
                        ]

xs = []
ys = []
xs_test = []
ys_test = []
na_variables = dict()

with open('../../data/processed/influenza.csv') as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)
    for row in reader:
        if int(row[VariableNames.year]) >= 2000 and row[VariableNames.region_name] in regions_interested:
            x = []
            na_found = False
            for variable_name in variables_interested:
                if row[variable_name] == 'N/A' or row[variable_name] == 'NA':
                    if variable_name in na_variables.keys():
                        na_variables[variable_name] = na_variables[variable_name] + 1
                    else:
                        na_variables[variable_name] = 1
                    na_found = True
                    break
                else:
                    x.append(float(row[variable_name]))
            if not na_found:
                if int(row[VariableNames.year]) >= 2012:
                    xs_test.append(x)
                    ys_test.append(float(row[VariableNames.num_positive]))
                else:
                    xs.append(x)
                    ys.append(float(row[VariableNames.num_positive]))

print(len(ys))
print(len(ys_test))
print(na_variables)
reg = linear_model.Lasso(alpha=0.1)
reg.fit(xs, ys)
for (variable_name, coefficient) in zip(variables_interested, reg.coef_):
    print(variable_name, coefficient)
predictions = reg.predict(xs_test)
print('Root Mean squared error: ', np.sqrt(mean_squared_error(predictions, ys_test)))
print('R2 score: ', r2_score(predictions, ys_test))
