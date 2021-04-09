#finding best areas for bird watching

import arcpy
import csv
import pandas as pd

arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"D:\Luba\pythonArcGIS\midterm project"

#opening a tables with information of bird frequency per sq km
#reading columns TTLC which contains amount of species which are commonly occuring in this cell
#finding maximum value of TTLC
#We are picking a cell with a maximum TTLC (amount of species which are commonly occuring in this cell)
df = pd.read_csv('bird_frequency_ri/birds.csv')
max_count_com_sp = df['TTLC'].max()
print("Maximum amount of species which are commonly occuring in a cell is " + max_count_com_sp)


conservation_land = 'conservation_lands/conservation_land.shp'
birds_freq = 'bird_frequency_ri/birds.shp'
rivers = 'rivers_and_lakes/Rivers.shp'
lakes = 'rivers_and_lakes/Lakes.shp'

#selecting area with higest amount of common species
birds_pop_area = "Birds_Area.shp"
arcpy.analysis.Select(in_features = birds_freq, out_feature_class = birds_pop_area, where_clause = '"TTLC" = ' + str(max_count_com_sp))
print("Selecting area with highest amount of species which are commonly occuring in this cell...")

#finding natural reserve areas which belongs to the area of higest amount of common species
# because it is easier to observe birds in nature preserve and because preserve has presumably higer bird count
reserve_w_birds = "Reserve_Birds_often.shp"
arcpy.analysis.Clip(in_features=conservation_land, clip_features=birds_pop_area, out_feature_class=reserve_w_birds, cluster_tolerance="")
print("Locating conservation lands within this cell...")

#creating buffer of 300 ft along rivers because it would be the area of high bird concentration and easier observation
Rivers_Buffer = "Rivers_Buffer.shp"
arcpy.analysis.Buffer(in_features=rivers, out_feature_class=Rivers_Buffer, buffer_distance_or_field="300 Feet", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field=[], method="PLANAR")


#creating buffer of 300 ft along lakes because it would be the area of high bird concentration and easier observation
Lakes_Buffer = "Lakes_Buffer.shp"
arcpy.analysis.Buffer(in_features=lakes, out_feature_class=Lakes_Buffer, buffer_distance_or_field="300 Feet", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field=[], method="PLANAR")


#combining both buffers
water_buffer = "Water_Buffer.shp"
arcpy.management.Merge(inputs=[Rivers_Buffer, Lakes_Buffer], output=water_buffer, field_mappings='StrmOrder "StrmOrder"')

print("Creating buffer around lakes and rivers to find areas of highest bird concentration...")

#finding where in preserve there is a near-water areas by intersecting water buffer with areas of preserves with high bird count
best_observation_areas = "Best_Obs_Areas.shp"
arcpy.analysis.Intersect(in_features=[[reserve_w_birds, ""], [water_buffer, ""]], out_feature_class=best_observation_areas, join_attributes="ALL", cluster_tolerance="", output_type="INPUT")
print("Intersecting river-lake buffer with conservation areas...")

#dissolving for easier usage
best_observation_area = "Best_Obs_Area.shp"
arcpy.management.Dissolve(in_features=best_observation_areas, out_feature_class=best_observation_area, dissolve_field=[], statistics_fields=[], multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")
print("Dissolving polygons...")

arcpy.Delete_management("Birds_Area.shp")
arcpy.Delete_management("Reserve_Birds_often.shp")
arcpy.Delete_management("Rivers_Buffer.shp")
arcpy.Delete_management("Lakes_Buffer.shp")
arcpy.Delete_management("Water_Buffer.shp")
arcpy.Delete_management("Best_Obs_Areas.shp")

print("Deleting intermediate files...")
