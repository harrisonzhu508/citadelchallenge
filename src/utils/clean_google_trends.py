# -*- coding: utf-8 -*-
import pickle
import csv
import pandas
import os
import numpy as np
import pprint
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

pp = pprint.PrettyPrinter(indent=4)


class VariableNames:
    country_code = 'country_code'
    country_name = 'country_name'
    two_letter_code = 'two_letter_code'
    three_letter_code = 'three_letter_code'
    year = 'year'
    month = 'month'
    day = 'day'
    search_frequency = 'frequency'
    search_query = 'search_query'


class NameConverter:
    def __init__(self, converter_file_name):
        self.dictionary = self.extract_dictionary(converter_file_name)

    def extract_dictionary(self, file_name):
        dict = {}
        with open(file_name, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            print(reader.fieldnames)
            for row in reader:
                if row[VariableNames.two_letter_code] and row[VariableNames.three_letter_code]:
                    dict[row[VariableNames.two_letter_code]] = row[VariableNames.three_letter_code]
                    dict[row[VariableNames.three_letter_code]] = row[VariableNames.two_letter_code]
        return dict

    def convert(self, code):
        if code in self.dictionary.keys():
            return self.dictionary[code]
        else:
            print(code, " not found")


converter_file_name = '../../data/country_codes_correspondence.csv'
nc = NameConverter(converter_file_name)
country_code = 'USA'
two_letter_code = nc.convert(country_code)
directory = '../../data/dataframes/' + two_letter_code + '/test/'
if not os.path.exists(directory):
    print('Does not exist')
    os.makedirs(directory)

all_data = []
scales = {}
years = [2004, 2008, 2012, 2016]
last_date = None

_fever_data = []
_times = []

for index, year in enumerate(years):
    if index != 0:
        dataframe_path = '../../data/dataframes/' + two_letter_code + '/' + str(year) + '.pkl'
        year_dataframe = pickle.load(open(dataframe_path, 'rb'))
        dataframe_path = '../../data/dataframes/' + two_letter_code + '/' + str(years[index - 1]) + '.pkl'
        prev_dataframe = pickle.load(open(dataframe_path, 'rb'))
        for key in year_dataframe.keys():
            if key != 'isPartial':
                # scale = year_dataframe[key][0].key
                # Approximate the scale by taking 50 readings, in very close agreement.year
                # Difference is due to quantisation errors.
                ratios = []
                for i in range(0, 50):
                    current_value = year_dataframe[key][i]
                    current_date = year_dataframe[key].index[i]
                    prev_corresponding_value = prev_dataframe[key][current_date]
                    ratio = prev_corresponding_value / current_value
                    ratios.append(ratio)

                ratios = np.array(ratios)
                average_ratio = np.average(ratios)

                scales[key] = scales[key] * average_ratio
                for date, value in year_dataframe[key].items():
                    if date > last_date:
                        all_data.append({VariableNames.year: date.year,
                                     VariableNames.month: date.month,
                                     VariableNames.day: date.day,
                                     VariableNames.search_query: key,
                                     VariableNames.country_code: country_code,
                                     VariableNames.search_frequency: float(value) * scales[key]})
                        if key == 'cough':
                            _times.append(date.value // 10 ** 9)
                            _fever_data.append(float(value) * scales[key])
        last_date = year_dataframe.index[-1]
    if index == 0:
        dataframe_path = '../../data/dataframes/' + two_letter_code + '/' + str(year) + '.pkl'
        year_dataframe = pickle.load(open(dataframe_path, 'rb'))
        print(year_dataframe)
        for key in year_dataframe.keys():
            if key != 'isPartial':
                scales[key] = 1.0
                for date, value in year_dataframe[key].items():
                    all_data.append({VariableNames.year: date.year,
                                 VariableNames.month: date.month,
                                 VariableNames.day: date.day,
                                 VariableNames.search_query: key,
                                 VariableNames.country_code: country_code,
                                 VariableNames.search_frequency: value})
                    if key == 'cough':
                        _times.append(date.value // 10 ** 9)
                        _fever_data.append(float(value) * scales[key])
        last_date = year_dataframe.index[-1]
        print(last_date)

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

window = 1
avged = moving_average(_fever_data, window)
# pp.pprint(all_data)
differentiated = np.diff(avged)
# differentiated = np.tanh(differentiated - 4)
plt.plot(_times[window:], differentiated)
plt.plot(_times[window - 1:], avged / 5)
plt.show()
