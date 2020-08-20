#Script to append feature class to AGOL
import arcpy
from arcgis import gis, features
import os
import shutil

#Update URL if using a version of data you published
pizza_url = "https://services3.arcgis.com/U26uBjSD32d7xvm2/arcgis/rest/services/Pizza_Restaurants/FeatureServer/0"

#Connect to AGOL Org
gis = gis.GIS('https://learngis2.maps.arcgis.com', '*****your username****', '*******your password******')

#Update to feature service to append data to ***********************************************************************************************************
fs = features.FeatureLayer(pizza_url, gis)
#*******************************************************************************************************************************************************

#Update to feature class for appending ***************************************************************************
check_fld = r"************************folder on your computer*****************\Check_Folder"

#get list of geodatabases in the check folder
gdb_list = os.listdir(check_fld)

#iterate through geodatabases in folder
for gdb in gdb_list:
    print(gdb)
    #Change environmental workspace for each geodatabase
    arcpy.env.workspace = os.path.join(check_fld, gdb)
    #Get a list of feature classes in the geodatabase
    for fc in arcpy.ListFeatureClasses():
        #Convert the feature class into a featureset
        sdf = features.GeoAccessor.from_featureclass(fc)
        fset = features.FeatureSet.from_dataframe(sdf)
        #Check the name of each restaurant to see if it's already in the AGOL feature service
        for feature in fset:
            print(feature.attributes['Name'])
            #Remove ' from name
            rest_name = feature.attributes['Name'].replace("'", "")
            query = "Name = '{}'".format(rest_name)
            #Use the formatted restaurant name to query the existing feature service to see if it already has the restaurant
            q_check = fs.query(where=query)
            #if the query returns an empty featureset, then we know that this restaurant isn't in AGOL already and we want to add it
            if q_check.features == []:
                #the edit features function is looking for a list to add, because we are adding one feature, we need to put it in a list 
                fs.edit_features(adds=[feature])
                print('New restaurant', feature.attributes['Name'])

            else:
                #if the query returns something, we know the restaurant is in AGOL and we can skip it
                print(feature.attributes['Name'], 'already in feature service')

#delete the geodatabase once it's been added to AGOL
for gdb in gdb_list:
    shutil.rmtree(os.path.join(check_fld, gdb))

