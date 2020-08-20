#Script to create point features from csv

import csv
import os
import arcpy

arcpy.env.overwriteOutput = True

#Csv file to plot
pizza_csv = arcpy.GetParameterAsText(0)

#Output folder
output_fld = arcpy.GetParameterAsText(1)

#XY fields
lat_field = arcpy.GetParameterAsText(2)
long_field = arcpy.GetParameterAsText(3)

#Output coordinate system
coord_system = int(arcpy.GetParameterAsText(4))
output_coordsys = arcpy.SpatialReference(coord_system)

#Create variables to store information from csv file
bad_coord_rest = []
good_coord_rest = []
fieldnames = []
bad_coord_csv = os.path.join(output_fld, 'Bad Coordinates.csv')
good_coord_csv = os.path.join(output_fld, 'Good Coordinates.csv')

#Create gdb to hold the new feature class
arcpy.CreateFileGDB_management(output_fld, 'Plotted_Coordinates.gdb')

#Read input csv and test the coordinates
arcpy.AddMessage('Evaluating csv for valid coordinates')
with open(pizza_csv, newline='') as csvfile:
    pizzareader = csv.DictReader(csvfile)
    fieldnames = pizzareader.fieldnames
    for row in pizzareader:
        try:
            float(row[lat_field])
            float(row[long_field])
            good_coord_rest.append(row)

        except ValueError:
            bad_coord_rest.append(row)

#Seperate the original csv into two csv files, one for records with valid coordinates, the other for the records that didn't have valid coordinates
with open(good_coord_csv, 'w', newline='') as newfile:
    writer = csv.DictWriter(newfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(good_coord_rest)

with open(bad_coord_csv, 'w', newline='') as newfile:
    writer = csv.DictWriter(newfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(bad_coord_rest)

#Create point feature using the valid coordinates
arcpy.AddMessage('Creating Feature Class')
arcpy.management.XYTableToPoint(good_coord_csv, os.path.join(output_fld, 'Plotted_Coordinates.gdb', 'Plotted_PointsTemp'), lat_field, long_field)
arcpy.Project_management(os.path.join(output_fld, 'Plotted_Coordinates.gdb', 'Plotted_PointsTemp'), os.path.join(output_fld, 'Plotted_Coordinates.gdb', 'Plotted_Points'), output_coordsys)

#Delete the temp csv and feature class
os.remove(good_coord_csv)
arcpy.Delete_management(os.path.join(output_fld, 'Plotted_Coordinates.gdb', 'Plotted_PointsTemp'))

