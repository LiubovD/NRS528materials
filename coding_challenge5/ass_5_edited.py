import arcpy
import csv

arcpy.env.overwriteOutput = True

# Set your workspace to the directory where you are storing your files
arcpy.env.workspace = r"D:\Luba\pythonArcGIS\mod5"


def make_layer(in_Table, x_coords, y_coords, out_Layer, spRef):
    print(in_Table)
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef)
    arcpy.CopyFeatures_management(lyr, out_Layer)
    return lyr

spRef = arcpy.SpatialReference(4326)

# trying to filter by subspecies - subspecies tigris goes to one layer and altaica to another
with open('panthera_tigris.csv') as tigris_table:

    csv_reader = csv.reader(tigris_table, delimiter=',')
    next(csv_reader)

    species_list = []

    for row in csv_reader:
        #print(row[3]) # equals scientificName column for each row
        if row[3] not in species_list:
            species_list.append(row[3])

print(species_list)

for species in species_list:

#1. Make shapefile for species
    with open('panthera_tigris.csv') as tigris_table:

        csv_reader = csv.reader(tigris_table, delimiter=',')
        header_row = next(csv_reader)
        print(header_row)

        new_csv_write = open(species + ".csv", "a")
        new_csv_write.write(", ".join(header_row))
        new_csv_write.write("\n")

        for row in csv_reader:
            if row[3] == species:
                new_csv_write.write(", ".join(row))
                new_csv_write.write("\n")

        new_csv_write.close()

    make_layer(species + ".csv", "decimalLongitude", "decimalLatitude", species + ".shp", spRef)

# 2. Make Fishnet for species



def make_fishnet():
    cellSizeWidth = "1"
    cellSizeHeight = "1"
    numRows = ""
    numColumns = ""
    labels = "NO_LABELS"
    templateExtent = "#"
    geometryType = "POLYGON"
    lyr = arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                                         cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                         oppositeCorner, labels, templateExtent, geometryType)
    arcpy.CopyFeatures_management(lyr, out_Layer)
    return lyr


# Set the origin of the fishnet
for species in species_list:
    desc = arcpy.Describe(species + ".shp")
    X_Min = desc.extent.XMin
    X_Max = desc.extent.XMax
    Y_Min = desc.extent.YMin
    Y_Max = desc.extent.YMax
    print(desc, X_Min, X_Max, Y_Min, Y_Max)
    make_fishnet(species + "_fishnet.shp", str(X_Min) + " " + str(Y_Min),
                 str(X_Min) + " " + str(Y_Min + 10), cellSizeWidth, cellSizeHeight,
                 numRows, numColumns, str(X_Max) + " " + str(Y_Max), labels,
                 templateExtent, geometryType)


# 3. Spatial Join

def spatial_join():
    join_operation = "JOIN_ONE_TO_ONE"
    join_type = "KEEP_ALL"
    field_mapping = ""
    match_option = "INTERSECT"
    search_radius = ""
    distance_field_name = ""
    lyr = arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                           join_operation, join_type, field_mapping, match_option,
                           search_radius, distance_field_name)
    return lyr


for species in species_list:
    spatial_join(species + ".shp", species + "_fishnet.shp", species + "heatmap.shp")



# 4. Clean up and delete intermediate files.


#
