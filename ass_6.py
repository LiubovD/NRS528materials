import arcpy
import os
outputDirectory = "D:/Luba/pythonArcGIS/mod6/rasters"


listMonths = ["02", "04", "05", "07", "10", "11"]

for month in listMonths:
    arcpy.env.workspace = "D:/Luba/pythonArcGIS/mod6/rasters/2015_" + month
    listRasters = arcpy.ListRasters("LC*", "TIF")
#    print("For month: " + month + ", there are: " + str(len(listRasters)- 1) + "bands to process.")
    for file in listRasters:
        if "_4.tif" in file:
            band_4 = file
        elif "_5.tif" in file:
            band_5 = file

    NDVI  = (band_5 - band_4) / (band_5 + band_4)
    NDVI + month.save("D:/Luba/pythonArcGIS/mod6/rasters")


