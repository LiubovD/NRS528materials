import arcpy
import csv

arcpy.env.overwriteOutput = True

# Set your workspace to the directory where you are storing your files
arcpy.env.workspace = r"C:\Data\Students_2021\Dumarevskaya\coding_challenge5"


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

    # 3. Spatial Join

    # 4. Clean up and delete intermediate files.


sdxhfgksdjhf

# Print the total rows
print(arcpy.GetCount_management(out_Layer))

# Save to a layer file
arcpy.CopyFeatures_management(lyr, saved_Layer)

if arcpy.Exists(saved_Layer):
    print("Created file successfully!")

desc = arcpy.Describe(saved_Layer)
print(desc.spatialReference.name)

desc = arcpy.Describe(saved_Layer)
XMin = desc.extent.XMin
XMax = desc.extent.XMax
YMin = desc.extent.YMin
YMax = desc.extent.YMax

print(XMin, XMax, YMin, YMax)


# this part is still in progress
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4326)

outFeatureClass = "Panthera_tigris_tigris.shp"

# Set the origin of the fishnet
originCoordinate = str(XMin) + ' ' + str(YMin)  # Left bottom of our point data
yAxisCoordinate = str(XMin) + ' ' + str(YMin + 0.25)  # This sets the orientation on the y-axis, so we head north
cellSizeWidth = "1"  # 1 degrees
cellSizeHeight = "1"
numRows = ""  # Leave blank, as we have set cellSize
numColumns = ""  # Leave blank, as we have set cellSize
oppositeCorner = str(XMax) + ' ' + str(YMax)  # i.e. max x and max y coordinate
labels = "NO_LABELS"
templateExtent = "#"  # No need to use, as we have set yAxisCoordinate and oppositeCorner
geometryType = "POLYGON"  # Create a polygon, could be POLYLINE

arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                               cellSizeWidth, cellSizeHeight, numRows, numColumns,
                               oppositeCorner, labels, templateExtent, geometryType)


# this part is still in progress

target_features="Fishnet_panthera_tigris_tigris.shp"
out_feature_class="Panthera_tigris_tigris_HeatMap.shp"
join_operation="JOIN_ONE_TO_ONE"
join_type="KEEP_ALL"
field_mapping=""
match_option="INTERSECT"
search_radius=""
distance_field_name=""

arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                           join_operation, join_type, field_mapping, match_option,
                           search_radius, distance_field_name)