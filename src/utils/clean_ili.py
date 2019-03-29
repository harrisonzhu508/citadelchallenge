import datetime
import csv
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

d = '1997-W53'
date = datetime.datetime.strptime(d + '-7', '%G-W%V-%u')
print(date)


class VariableNames:
    country_code = 'country_code'
    year = 'year'
    year_origin = 'YEAR'
    week_number_origin = 'WEEK'
    week_number = 'week'
    weighted_ili_origin = '% WEIGHTED ILI'
    percentage_ili = '% ILI affected patients'


new_data = []
new_data_graphing = []
weeks = []

with open('../../data/ILINet.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if int(row[VariableNames.year_origin]) >= 2000:
            weeks.append(int(row[VariableNames.week_number_origin]))
            new_data.append({VariableNames.country_code: 'USA',
                             VariableNames.week_number: row[VariableNames.week_number_origin],
                             VariableNames.percentage_ili: row[VariableNames.weighted_ili_origin],
                             VariableNames.year: row[VariableNames.year_origin]
                             })
            new_data_graphing.append(float(row[VariableNames.weighted_ili_origin]))
# print(new_data)
# print(weeks)
plt.plot(new_data_graphing)
plt.show()
out_file_name = '../../data/processed/ili.csv'
with open(out_file_name, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=[VariableNames.country_code,
                                           VariableNames.year,
                                           VariableNames.week_number,
                                           VariableNames.percentage_ili])
    writer.writeheader()
    writer.writerows(new_data)
