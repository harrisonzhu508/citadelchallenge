# -*- coding: utf-8 -*-
import pickle
import csv
from pytrends.request import TrendReq
import os


class VariableNames:
    country_code = 'country_code'
    country_name = 'country_name'
    two_letter_code = 'two_letter_code'
    three_letter_code = 'three_letter_code'
    year_origin = 'Time'
    year = 'year'
    month = 'month'
    hours_worked_origin = 'Value'
    hours_worked = 'Hours worked per year'
    employment_status = 'EMPSTAT'


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


# kw_list = ['fever', 'cough', 'flu']
kw_list = ['fever', 'cough']
converter_file_name = '../../data/country_codes_correspondence.csv'

nc = NameConverter(converter_file_name)
country_code = 'USA'
two_letter_code = nc.convert(country_code)
directory = '../../data/dataframes/' + two_letter_code + '/test/'
if not os.path.exists(directory):
    print('Does not exist')
    os.makedirs(directory)

years = [2004, 2008, 2012, 2016]

for year in years:

    pytrend = TrendReq()
    df = pytrend.get_historical_interest(kw_list,
                                         start_year=year,
                                         geo=two_letter_code)
    print(df)
    dataframe_path = '../../data/dataframes/' + two_letter_code + '/' + str(year) + '.pkl'
    open(dataframe_path, 'a').close()
    df.to_pickle(dataframe_path)
