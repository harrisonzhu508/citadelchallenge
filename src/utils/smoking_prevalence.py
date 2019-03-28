import csv
from scipy.interpolate import interp1d
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


class VariableNames:
    country_code = 'country_code'
    year = 'year'
    month = 'month'
    smoking_prevalence = 'Smoking prevalence, total (ages 15+)'
    smoking_prevalence_destination = 'Smoking prevalence, total (ages 15+, linearly interpolated)'


def append_data_for_country(data_list, country_code, years_data, prevalence_data):
    if not prevalence_data:
        print(country_code, 'has no smoking data')
        for year in range(2000, 2016):
            for i in range(1, 13):
                data_list.append({VariableNames.country_code: country_code,
                                 VariableNames.year: year,
                                 VariableNames.month: i,
                                 VariableNames.smoking_prevalence_destination: 'N/A'})
    else:
        interpolated = interp1d(years_data, prevalence_data)
        for year in range(2000, int(max(years_data))):
            for i in range(1, 13):
                time = year + (float(i) - 1) / 12
                interpolated_value = float(interpolated(time))
                data_list.append({VariableNames.country_code: country_code,
                                 VariableNames.year: year,
                                 VariableNames.month: i,
                                 VariableNames.smoking_prevalence_destination: interpolated_value})
        if max(years_data) < 2017:
            for year in range(int(max(years_data)), 2017):
                for i in range(1, 13):
                    data_list.append({VariableNames.country_code: country_code,
                                     VariableNames.year: year,
                                     VariableNames.month: i,
                                     VariableNames.smoking_prevalence_destination: 'N/A'})


new_data = []
current_country = None

with open('data/health_indicators.csv') as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)
    years_data = []
    prevalence_data = []
    for row in reader:
        if int(row[VariableNames.year]) >= 2000:
            if row[VariableNames.country_code] != current_country:
                if current_country is not None:
                    append_data_for_country(new_data,
                                            current_country,
                                            years_data,
                                            prevalence_data)
                current_country = row[VariableNames.country_code]
                years_data = []
                prevalence_data = []
            if row[VariableNames.smoking_prevalence]:
                years_data.append(float(row[VariableNames.year]))
                prevalence_data.append(float(row[VariableNames.smoking_prevalence]))

# print(new_data)

out_file_name = 'data/processed/smoking_prevalence.csv'
with open(out_file_name, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=[VariableNames.country_code,
                                           VariableNames.year,
                                           VariableNames.month,
                                           VariableNames.smoking_prevalence_destination])
    writer.writeheader()
    writer.writerows(new_data)
