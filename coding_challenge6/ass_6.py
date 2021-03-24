import arcpy
import os
outputDirectory = "D:/Luba/pythonArcGIS/mod6/rasters"


listMonths = ["02", "04", "05", "07", "10", "11"]

for month in listMonths:
    arcpy.env.workspace = "D:/Luba/pythonArcGIS/mod6/rasters/2015_" + month
    listRasters = arcpy.ListRasters("LC*", "TIF")
#    I am getting an error in here: for file in listRasters: TypeError: 'NoneType' object is not iterable
    for file in listRasters:
        if "_4.tif" in file:
            band_4 = file
        elif "_5.tif" in file:
            band_5 = file

    NDVI  = (band_5 - band_4) / (band_5 + band_4)
    NDVI + month.save("D:/Luba/pythonArcGIS/mod6/rasters")


