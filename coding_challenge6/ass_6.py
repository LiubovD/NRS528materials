# in this task we are calculating NDVI values per each month

import arcpy
import os
from arcpy.sa import *

outputDirectory = "D:/Luba/pythonArcGIS/mod6/rasters"

arcpy.env.overwriteOutput = True

# we create a list of months and printing them
listMonths = ["02", "04", "05", "07", "10", "11"]
print(listMonths)

# for every month in the list we set as directory a folder of this month
# and within this folder we pick red and NIR bands
for month in listMonths:
    arcpy.env.workspace = "D:/Luba/pythonArcGIS/mod6/rasters/2015" + month
    listRasters = arcpy.ListRasters("LC*", "TIF")
#    print("For month: " + month + ", there are: " + str(len(listRasters)- 1) + "bands to process.")
    for file in listRasters:
        if "4.tif" in file:
            band_4 = file
        elif "5.tif" in file:
            band_5 = file



    # based on red and NIR rasters we create raster containing NDVI values
    output_raster = (Raster(band_5) - Raster(band_4)) / (Raster(band_5) + Raster(band_4))
    output_raster.save(outputDirectory + "\\"+ str(month) + "_NDVI.tif")
    print(month + "_NDVI.tif")\
    
# i tried to make it check whether results printing works but it does prints 'failed' even though file with such name exists!"
    if arcpy.Exists(month + "_NDVI.tif"):
        print("Created NDVI raster successfully for" + month)
    else:
        print("failed")

