# Coding Challenge 5
# Generating Heatmaps for Two Species
# For this coding challenge I used two subspecies of Panthera tigris -
# Panthera tigris tigris and Panthera tigris altaica.

import arcpy
import csv
import os

arcpy.env.overwriteOutput = True

working_directory = r"D:\Luba\pythonArcGIS\mod5\ass_5"
arcpy.env.workspace = working_directory
os.chdir(working_directory)

#writing function to create shp file of species location
def make_layer(in_Table, x_coords, y_coords, out_Layer, spRef):
    print(in_Table)
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef)
    arcpy.CopyFeatures_management(lyr, out_Layer)
    return lyr

spRef = arcpy.SpatialReference(4326)

# opening table with species and creating separate tables for every species
with open('panthera_tigris.csv') as tigris_table:
    csv_reader = csv.reader(tigris_table, delimiter=',')
    next(csv_reader)
    species_list = []
    for row in csv_reader:
        if row[3] not in species_list:
            species_list.append(row[3])

#printing all species in the file
print(species_list)

for species in species_list:
#Making shapefile for species
    with open('panthera_tigris.csv') as tigris_table:
        csv_reader = csv.reader(tigris_table, delimiter=',')
        header_row = next(csv_reader)
        new_csv_write = open(species + ".csv", "w")
        new_csv_write.write(", ".join(header_row))
        new_csv_write.write("\n")
        for row in csv_reader:
            if row[3] == species:
                new_csv_write.write(", ".join(row))
                new_csv_write.write("\n")
        new_csv_write.close()

    make_layer(species + ".csv", "decimalLongitude", "decimalLatitude", species + ".shp", spRef)

    #Check if shp file was created
    if arcpy.Exists(species + ".shp"):
        print("Created the shapefile successfully for" + species)
    else:
        print("Error")

#writing function to create fishnet files of species location
def make_fishnet(outFeatureClass, originCoordinate,yAxisCoordinate, cellSizeWidth, cellSizeHeight, numRows, numColumns,oppositeCorner):
    arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                                         cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                         oppositeCorner, "", "", "POLYGON")
    arcpy.DefineProjection_management(outFeatureClass, spRef)
    return


# Setting the origin of the fishnet
for species in species_list:
    desc = arcpy.Describe(species + ".shp")
    X_Min = desc.extent.XMin
    X_Max = desc.extent.XMax
    Y_Min = desc.extent.YMin
    Y_Max = desc.extent.YMax
    print(desc, X_Min, X_Max, Y_Min, Y_Max)

    # Making Fishnet for all species
    make_fishnet(species + "_fishnet.shp", str(X_Min) + " " + str(Y_Min),
                 str(X_Min) + " " + str(Y_Min + 10), (X_Max- X_Min)/10, (X_Max- X_Min)/10,
                 "", "", str(X_Max) + " " + str(Y_Max))

    #Check if shp file was created
    if arcpy.Exists(species + "_fishnet.shp"):
        print("Created the fishnet successfully for" + species)
    else:
        print("Error")

# writing function to spatially join fishnet and shp files
def spatial_join(target_features, join_features, out_feature_class):
    join_operation = "JOIN_ONE_TO_ONE"
    join_type = "KEEP_ALL"
    field_mapping = ""
    match_option = "INTERSECT"
    search_radius = ""
    distance_field_name = ""
    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                                     join_operation, join_type, field_mapping, match_option)
    return

# Spatial Join of fishnet and species location for all species
for species in species_list:
    spatial_join(os.path.join(working_directory, species + "_fishnet.shp"), os.path.join(working_directory, species + ".shp"), os.path.join(working_directory, species + "heatmap.shp"))

# Deleting intermediate files
    print('Deleting intermediate files')

for species in species_list:
    if arcpy.Exists(os.path.join(working_directory, species + "_fishnet.shp")):
        arcpy.Delete_management(os.path.join(working_directory, species + ".shp"))

    if arcpy.Exists(os.path.join(working_directory, species + "_fishnet.shp")):
        print("Created heatmaps successfully for" + species)
