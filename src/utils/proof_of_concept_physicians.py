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

original_data = []
original_years_data = []

def append_data_for_country(data_list, country_code, years_data, prevalence_data):
    if not prevalence_data:
        print(country_code, 'has no smoking data')
    else:
        print(years_data, prevalence_data)
        interpolated = interp1d(years_data, prevalence_data, kind='quadratic')
        for year in range(2000, int(max(years_data))):
            print(year)

            for i in range(1, 13):
                time = year + (float(i) - 1) / 12
                print(time)
                interpolated_value = float(interpolated(time))
                data_list.append(interpolated_value)
            #     data_list.append({VariableNames.country_code: country_code,
            #                      VariableNames.year: year,
            #                      VariableNames.month: i,
            #                      VariableNames.smoking_prevalence_destination: interpolated_value})


new_data = []
current_country = None

with open('data/health_indicators.csv') as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)
    years_data = []
    prevalence_data = []
    for row in reader:
        if row[VariableNames.country_code] != current_country:
            if current_country is not None and current_country == 'USA':
                original_data = prevalence_data
                original_years_data = years_data
                append_data_for_country(new_data,
                                        current_country,
                                        years_data,
                                        prevalence_data)
            current_country = row[VariableNames.country_code]
            years_data = []
            prevalence_data = []
        if row[VariableNames.physician_rate]:
            years_data.append(float(row[VariableNames.year]))
            prevalence_data.append(float(row[VariableNames.physician_rate]))

print(new_data)
plt.plot(np.linspace(2000, max(original_years_data), (max(original_years_data) - 2000) * 12), (new_data))
print(original_years_data, original_data)
plt.scatter(original_years_data, original_data)
plt.show()

# out_file_name = 'data/processed/hours_worked.csv'
# with open(out_file_name, 'w') as f:
#     writer = csv.DictWriter(f, fieldnames=[VariableNames.country_code,
#                                            VariableNames.year,
#                                            VariableNames.month,
#                                            VariableNames.hours_worked])
#     writer.writeheader()
#     writer.writerows(new_data)
