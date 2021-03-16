import arcpy
import csv

arcpy.env.overwriteOutput = True

# Set your workspace to the directory where you are storing your files
arcpy.env.workspace = r"C:\Users\lubad\OneDrive\Documents\pythonArcGIS\mod5"

# Split the input file into two separate CSV files - 1 for Panthera tigris tigris
# and 1 for this anthera_tigris_altaica

species_list = []


# trying to filter by subspecies - subspecies tigris goes to one layer and altaica to another

for species in species_list:
    with open('panthera_tigris.csv') as tigris_table:
        next(tigris_table)
        for row in tigris_table:
            id, sp, subsp, name, lat, lon  = row.split(sep=',')
            if subsp == "altaica":
                in_Table = r"panthera_tigris.csv"
                x_coords = "decimalLongitude"
                y_coords = "decimalLatitude"
                z_coords = ""
                out_Layer = "Panthera_tigris_altaica"
                saved_Layer = r"Panthera_tigris_altaica.shp"
            else:
                in_Table = r"panthera_tigris.csv"
                x_coords = "decimalLongitude"
                y_coords = "decimalLatitude"
                z_coords = ""
                out_Layer = "Panthera_tigris_tigris"
                saved_Layer = r"Panthera_tigris_tigris.shp"

    # Set the spatial reference
    spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984

    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

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