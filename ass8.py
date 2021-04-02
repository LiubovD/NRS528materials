import arcpy

arcpy.env.workspace = 'D:\Luba\pythonArcGIS\mod8\data'
arcpy.env.overwriteOutput = True

#let's make a tool for creating buffers with a custom distance within choosen area
def making_river_buffer(towns, rivers, study_area, buffer_dist):
    if arcpy.Exists:
        # for starters, let's establish a study area
        town_selected = 'Study_area.shp'
        arcpy.Select_analysis(towns, town_selected, study_area)
        #to continue, let's clip our rivers layer to the study area
        clipped_to_area = "Rivers_clipped.shp"
        arcpy.analysis.Clip(rivers, town_selected, clipped_to_area)
        # finally, we can create a buffer
        river_buffer = "River_buffer.shp"
        line_side = ""
        line_end_type = ""
        dissolve_option = ""
        sideType = "FULL"
        endType = "ROUND"
        dissolveType = "LIST"
        dissolve_field = ""
        method = ""
        arcpy.Buffer_analysis(clipped_to_area, river_buffer, buffer_dist,  line_side, line_end_type, dissolve_option, dissolve_field, method)
        print("created River buffer shape layer")

    else:
        print("Dataset not found, please check the file path..")

making_river_buffer(r"D:\Luba\pythonArcGIS\mod8\data\towns.shp", r"D:\Luba\pythonArcGIS\mod8\data\Rivers.shp","NAME = 'SOUTH KINGSTOWN'", "100 Feet")

arcpy.Delete_management('Study_area.shp')
arcpy.Delete_management('Rivers_clipped.shp')
