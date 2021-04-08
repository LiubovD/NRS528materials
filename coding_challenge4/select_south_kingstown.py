import arcpy
from arcpy import env

#setting directory
env.workspace = r"D:\Luba\pythonArcGIS\mod4\data"

#making a selection in towns layer, selecting south kingstown
in_features = "towns.shp"
out_feature_class = "select_south_kingstown.shp"
where_clause = "NAME = 'SOUTH KINGSTOWN'"

arcpy.Select_analysis(in_features, out_feature_class, where_clause)
