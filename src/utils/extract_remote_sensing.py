#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 22:28:46 2019

@author: harrisonzhu
"""

import ee
from ee import batch
from datetime import datetime

ee.Initialize()

gridmet = ee.ImageCollection("IDAHO_EPSCOR/GRIDMET")

def process(start_date, end_date, database, feature):
	"""extract and process climatic data for year

	Input:

		start_date: start date. YEAR-MONTH-DAY, zero-padded
		end_date: end date. YEAR-MONTH-DAY, zero-padded
		database: 
		feature:

	Output:


	"""

	elif database == "gridmet":
		data = gridmet
	else:
		raise Exception("ImageCollection not defined. Check whether input is modis, gridmet or noah")

	print("Gathering data from " + database)
	print("start date: {}, end date {}".format(start_date, end_date))
	print("feature: {}".format(feature))
	# convert dates to ee data types
	month = end_date[5:7]
	year = end_date[:4]
	
	# select feature
	data_reduced = data.select(feature).filterDate(ee.Date(start_date), ee.Date(end_date)).mean()

	# load regions: countries from a public fusion table, removing non-conus states
	# by using a custom filter
	countries = ee.FeatureCollection('ft:1tdSwUL7MVpOauSgRzqVTOwdfy17KDbw-1d9omPw')

	# get mean values by county polygon
	features = data_reduced.reduceRegions(\
	collection = countries,\
	reducer = ee.Reducer.mean(),\
	scale = 4000
	)

	# add a new column for year to each feature in the features
	features = features.map(
		lambda feature: feature.set("month",year + "-" + month)
	)
	
	# Export ---------------------------------------------------------------------
	out = batch.Export.table.toDrive(
	collection = features,\
	description = '{}_{}_{}'.format(feature, year, month),\
	folder = feature,\
	fileFormat = 'CSV',
	selectors = "mean, month, name, STATEFP "
	)
	
	# send batch to process as csv in server
	batch.Task.start(out)
	print("Process sent to cloud")

	return

def main():
	#["pr", "rmax", "rmin", "erc", "eto", "etr"]
	datatype = "modis"
	features = ["NDVI"]
	
	for feature in features:
		for year in range(1969, 2019):
			for month in range(1, 13):

				start_date = datetime(year=year, month=month, day=1)
				end_date = datetime(year=year, month=month, day=28)
				start_date = start_date.strftime("%Y-%m-%d")
				end_date = end_date.strftime("%Y-%m-%d")
				process(start_date, end_date, datatype, feature)

if __name__ == "__main__":
	main()	