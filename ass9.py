# In this coding challenge, your objective is to utilize the arcpy.da module to undertake some basic partitioning
# of your dataset. In this coding challenge, I want you to work with the Forest Health Works dataset
# from RI GIS (I have provided this as a downloadable ZIP file in this repository).

# Using the arcpy.da module (yes, there are other ways and better tools to do this),
# I want you to extract all sites that have a photo of the invasive species (Field: PHOTO)
# into a new Shapefile, and do some basic counts of the dataset. In summary, please addressing
# the following:
# Count how many sites have photos, and how many do not (2 numbers), print the results.
# Count how many unique species there are in the dataset, print the result.
# Generate two shapefiles, one with photos and the other without.


import arcpy

# set work repository and allow to overwrite content
arcpy.env.workspace = r"D:\Luba\pythonArcGIS\mod9\ass_9"
arcpy.env.overwriteOutput = True

#set our source file and rows we will be using
input_shp = r'D:\Luba\pythonArcGIS\mod9\ass_9\RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp'
fields = ["Point_num", "Site","Species", "photo"]

# create a new file based on photo presence - indicated as "y" in field "photo"
expression = arcpy.AddFieldDelimiters(input_shp, "photo") + " = 'y'"
arcpy.Select_analysis(input_shp,"areas_with_photo.shp", expression)

#count how many sites have photos - for this we are using list of sites to avoid double-counting our sites
counter = 0
list_sites = list()
expression = arcpy.AddFieldDelimiters("areas_with_photo.shp", "photo") + " = 'y'"
with arcpy.da.SearchCursor("areas_with_photo.shp", fields, expression) as cursor:
    for row in cursor:
        if row[1] not in list_sites:
            counter += 1
            list_sites.append(row[1])
print("Number of sites with photo = ", counter)


# However if we decide to do the same procedure with the database as before, we won't provide true information
# because while some points from dataset might not have photos, others wouldn't have it. So if our purpose
# to find sites for which we doens't have a single photos available, we'd need to make a list of ALL sites and
# then exclude those of them which would have at least one photo. Let's try it.

list_all_sites = list()

with arcpy.da.SearchCursor("areas_with_photo.shp", fields) as cursor:
    for row in cursor:
        if row[1] not in list_all_sites:
            list_sites.append(row[1])
counter2 = 0
for site in list_all_sites:
    if site not in list_sites:
        counter2 += 1
        print(site)
print("Number of sites which doesn't contain at least one photo = ", counter2)
print("List of sites", list_all_sites)

# Let's count species now.

species_list = list()
with arcpy.da.SearchCursor("areas_with_photo.shp", fields) as cursor:
    for row in cursor:
        if row[2] not in species_list:
            species_list.append(row[2])
print("Invasive species identified are ", species_list)
print("total number of species is ", len(species_list))