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
    physician_rate = 'Physicians (per 1,000 people)'
    physician_rate_destination = 'Physicians (per 1,000 people), linearly interpolated'


def append_data_for_country(data_list, country_code, years_data, prevalence_data):
    print(country_code, years_data, prevalence_data)
    if not prevalence_data:
        print(country_code, 'has no physician data')
        for year in range(2000, 2016):
            for i in range(1, 13):
                data_list.append({VariableNames.country_code: country_code,
                                 VariableNames.year: year,
                                 VariableNames.month: i,
                                 VariableNames.physician_rate_destination: 'N/A'})
    else:
        if len(years_data) >= 3:
            interpolated = interp1d(years_data, prevalence_data, kind='quadratic')
        elif len(years_data) == 1:
            print(country_code, 'has only one datapoint')
            for year in range(2000, 2016):
                for i in range(1, 13):
                    if year == years_data[0] and i == 1:
                        data_list.append({VariableNames.country_code: country_code,
                                     VariableNames.year: year,
                                     VariableNames.month: i,
                                     VariableNames.physician_rate_destination: prevalence_data[0]})
                    else:
                        data_list.append({VariableNames.country_code: country_code,
                                         VariableNames.year: year,
                                         VariableNames.month: i,
                                         VariableNames.physician_rate_destination: 'N/A'})
            return
        else:
            interpolated = interp1d(years_data, prevalence_data, kind='linear')
        if int(min(years_data)) > 2000:
            for year in range(2000, int(min(years_data))):
                for i in range(1, 13):
                    data_list.append({VariableNames.country_code: country_code,
                                     VariableNames.year: year,
                                     VariableNames.month: i,
                                     VariableNames.physician_rate_destination: 'N/A'})
        for year in range(int(min(years_data)), int(max(years_data))):
            for i in range(1, 13):
                time = year + (float(i) - 1) / 12
                interpolated_value = float(interpolated(time))
                data_list.append({VariableNames.country_code: country_code,
                                 VariableNames.year: year,
                                 VariableNames.month: i,
                                 VariableNames.physician_rate_destination: interpolated_value})
        if max(years_data) < 2017:
            for year in range(int(max(years_data)), 2017):
                for i in range(1, 13):
                    data_list.append({VariableNames.country_code: country_code,
                                     VariableNames.year: year,
                                     VariableNames.month: i,
                                     VariableNames.physician_rate_destination: 'N/A'})


new_data = []
current_country = None

with open('data/health_indicators.csv') as f:
    reader = csv.DictReader(f)
    years_data = []
    physician_data = []
    for row in reader:
        if int(row[VariableNames.year]) >= 2000:
            if row[VariableNames.country_code] != current_country:
                if current_country is not None:
                    append_data_for_country(new_data,
                                            current_country,
                                            years_data,
                                            physician_data)
                current_country = row[VariableNames.country_code]
                years_data = []
                physician_data = []
            if row[VariableNames.physician_rate]:
                years_data.append(float(row[VariableNames.year]))
                physician_data.append(float(row[VariableNames.physician_rate]))

# print(new_data)

out_file_name = 'data/processed/physician_data.csv'
with open(out_file_name, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=[VariableNames.country_code,
                                           VariableNames.year,
                                           VariableNames.month,
                                           VariableNames.physician_rate_destination])
    writer.writeheader()
    writer.writerows(new_data)
