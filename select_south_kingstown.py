import arcpy
from arcpy import env

env.workspace = "C:/Users/lubad/PycharmProjects/pythonProject1/Data"

in_features = "towns.shp"
out_feature_class = "C:/Users/lubad/PycharmProjects/pythonProject1/Data/select_south_kingstown.shp"
where_clause = "NAME = 'SOUTH KINGSTOWN'"

arcpy.Select_analysis(in_features, out_feature_class, where_clause)