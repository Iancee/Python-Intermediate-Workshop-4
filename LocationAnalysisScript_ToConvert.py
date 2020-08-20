#Script to create point features from csv
import arcpy
import os

arcpy.env.overwriteOutput = True

loc_int = r"*******************Insert path from your computer*****************************\Locations_of_Interest.shp"

neighborhoods = r"*******************Insert path from your computer*****************************\SF_Neighborhoods.shp"

output_loc = r"*******************Insert path from your computer*****************************"

#This should be the folder containing the SF testing shapefiles
arcpy.env.workspace = r"*******************Insert path from your computer*****************************\SF_SHPs"

shp_list = arcpy.ListFeatureClasses()

arcpy.MakeFeatureLayer_management(loc_int, "loc_int_lyr")

arcpy.SpatialJoin_analysis(loc_int, neighborhoods, os.path.join(output_loc, 'LocationPointsJoined.shp'))

with arcpy.da.SearchCursor(loc_int, '*') as point_cursor:
    for row in point_cursor:
        print(row[2])
        #Making folders
        os.mkdir(os.path.join(output_loc, row[2]))
        
        #Making selections
        query = "Location = '{}'".format(row[2])
        print(query)
        arcpy.SelectLayerByAttribute_management("loc_int_lyr", "NEW_SELECTION", query)
        arcpy.Buffer_analysis("loc_int_lyr", r"memory\Buffer", "1 Mile")
        for shp in shp_list:
            print(shp)
            arcpy.Clip_analysis(shp, r"memory\Buffer", os.path.join(output_loc, row[2], shp))



