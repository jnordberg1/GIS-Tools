# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:19:31 2019

@author: JacobNordberg
"""
import arcpy
from arcpy import env


env.workspace           =   r'PATH TO WORKSPACE OR DATABASE'
env.overwriteOutput     =   True

phi                     =   "_DeleteTemp"
out_point               =   "out_points"

def CreateCentroids(in_polygon, out_point):
    Spatial_Reference   =   arcpy.Describe(in_polygon).spatialReference
    arcpy.Select_analysis(in_polygon,"Zones",'Shape_Area <> 0')
    arcpy.AddField_management("Zones","XCentroid","DOUBLE")
    arcpy.AddField_management("Zones","YCentroid","DOUBLE")
    arcpy.CalculateField_management("Zones","XCentroid","!shape.centroid.X!","PYTHON_9.3")
    arcpy.CalculateField_management("Zones","YCentroid","!shape.centroid.Y!","PYTHON_9.3")
    arcpy.MakeXYEventLayer_management("Zones", "XCentroid", "YCentroid", "Centroids", Spatial_Reference)
    arcpy.Select_analysis("Centroids", out_point)
    arcpy.Delete_management("Zones", "Centroids")
    
CreateCentroids("merged"+phi, out_point)