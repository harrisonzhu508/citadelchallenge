import csv
from sklearn import linear_model
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib as mpl
import pprint
mpl.use('TkAgg')
import matplotlib.pyplot as plt
pp = pprint.PrettyPrinter(indent=4)

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
    hours_worked = 'Hours_worked_per_year'
    expenditure_ppp = 'expenditure_PPP'
    num_physician = 'num_physician'
    year = 'year'
    month = 'month'
    num_positive = 'num_influenza_positive'


regions_interested = ["European Region of WHO", "Region of the Americas of WHO", "Western Pacific Region of WHO"]
# regions_interested = ['Western Pacific Region of WHO']
variables_interested = [
                        # VariableNames.capital_lat,
                        # VariableNames.capital_long,
                        VariableNames.tmmn,
                        VariableNames.tmmx,
                        VariableNames.pr,
                        VariableNames.def_,
                        VariableNames.aet,
                        VariableNames.srad,
                        VariableNames.vap,
                        VariableNames.hours_worked,
                        VariableNames.expenditure_ppp,
                        VariableNames.num_physician,
                        ]

# Scale so everything between 0 and 1, using either the limits, e.g. for long lat,
# and the maximum numbers for others
# shows the min and max numbers so can be scaled between.
variables_scales = {
                    VariableNames.capital_lat: (0, 90.),
                    VariableNames.capital_long: (0, 180.),
                    VariableNames.tmmn: (-29.54, 21.47),
                    VariableNames.tmmx: (-21.33, 33.82),
                    VariableNames.pr: (0.59, 546.75),
                    VariableNames.def_: (0, 1806),
                    VariableNames.aet: (0, 1389.73),
                    VariableNames.srad: (23.13, 3189.91),
                    VariableNames.vap: (94.67, 2864.35),
                    VariableNames.hours_worked: (1289.2, 2359.0),
                    VariableNames.expenditure_ppp: (0.0, 428.2),
                    VariableNames.num_physician: (0.9, 6.25),
                    }

human_readable_names = {
    VariableNames.tmmn: 'Minimum temperature',
    VariableNames.tmmx: 'Maximum temperature',
    VariableNames.pr: 'Precipitation',
    VariableNames.def_: 'Climate water deficit',
    VariableNames.aet: 'Actual evapotranspiration',
    VariableNames.srad: 'Downward surface shortwave radiation',
    VariableNames.vap: 'Vapour pressure',
    VariableNames.hours_worked: 'Hours worked per year',
    VariableNames.expenditure_ppp: 'Total healthcare expenditure per capita, adjusted for PPP',
    VariableNames.num_physician: 'Number of physicians per capita'
}

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
                    to_append = float(row[variable_name])
                    if variable_name in variables_scales.keys():
                        scale = variables_scales[variable_name]
                        to_append = (to_append - scale[0]) / (scale[1] - scale[0])
                    x.append(to_append)
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
reg = linear_model.ElasticNet(max_iter=100000)
reg.fit(xs, ys)
print_dictionary = {}
for (variable_name, coefficient) in zip(variables_interested, reg.coef_):
    print(human_readable_names[variable_name], ': ', coefficient)

# pp.pprint(print_dictionary)
