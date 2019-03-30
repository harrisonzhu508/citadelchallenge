#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 22:28:46 2019
Datasource: https://developers.google.com/earth-engine/datasets/catalog/IDAHO_EPSCOR_TERRACLIMATE

TERRACLIMATE AND MODIS

	- MODIS/006/MOD13Q1
	- NOAA/CFSV2/FOR6H

@author: harrisonzhu
"""

import ee
from ee import batch
from datetime import datetime

ee.Initialize()

noaa = ee.ImageCollection("NOAA/CFSV2/FOR6H")
ndvi = ee.ImageCollection("MODIS/006/MOD13Q1")

def process(week, start_date, end_date, database, features_list):
	"""extract and process climatic data for year

	Input:

		start_date: start date. YEAR-MONTH-DAY, zero-padded
		end_date: end date. YEAR-MONTH-DAY, zero-padded
		database:
		features

        Output:
	"""

	if database == "noaa":
		data = noaa
	elif database == "ndvi":
		data = ndvi
	else:
		raise Exception("ImageCollection not defined. Check whether input is modis, gridmet or noah")


	print("Gathering data from " + database)
	print("start date: {}, end date {}".format(start_date, end_date))
	# convert dates to ee data types
	month = end_date[5:7]
	year = end_date[:4]
	# select feature
	data_reduced = data.select(features_list).filterDate(ee.Date(start_date), ee.Date(end_date)).mean()

	# load regions: countries from a public fusion table, removing non-conus states
	# by using a custom filter
	countries = ee.FeatureCollection('ft:1tdSwUL7MVpOauSgRzqVTOwdfy17KDbw-1d9omPw')

	# get mean values by country polygon
	features = data_reduced.reduceRegions(\
	collection = countries,\
	reducer = ee.Reducer.mean(),\
	scale = 4000
	)

	# add a new column for year to each feature in the features
	features = features.map(
		lambda feature: feature.set("date",year + "-" + month + "-" + "{}".format(week))
	)

	# Export ---------------------------------------------------------------------
	out = batch.Export.table.toDrive(
	collection = features,\
	description = '{}_{}'.format(year, week),\
	folder = "noaa",\
	fileFormat = 'CSV',
	selectors = "date, Country, {}".format(", ".join(features_list)))


	# send batch to process as csv in server
	batch.Task.start(out)
	print("Process sent to cloud")

	return

def main():
	#["pr", "rmax", "rmin", "erc", "eto", "etr"]
	datatype = "noaa"
	features_list = ["Geopotential_height_surface",\
				"Temperature_height_above_ground",\
                "Potential_Evaporation_Rate_surface_6_Hour_Average",\
                "Specific_humidity_height_above_ground",\
                "Pressure_surface"]
	#features_list = ["NDVI"]
	for year in range(2000, 2019):
		for week in range(1, 52):
			start_date = "{}-W{}".format(year, week)
			end_date = "{}-W{}".format(year, week+1)

			start_date = datetime.strptime(start_date + '-1', "%Y-W%W-%w")
			end_date = datetime.strptime(end_date + '-1', "%Y-W%W-%w")
			start_date = start_date.strftime("%Y-%m-%d")
			end_date = end_date.strftime("%Y-%m-%d")
			process(week, start_date, end_date, datatype, features_list)
if __name__ == "__main__":
	main()
