# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:14:29 2019

@author: JacobNordberg
"""

def Delete_duplicates(in_source, out_fc):
    fieldnames = []
    fields = arcpy.ListFields(in_source)
    for field in fields:
        if not field.required:
            fieldnames.append(field.name)
    arcpy.Select_analysis(in_source, "Drop_duplicated")
    #add x y fields
    spatial_ref = arcpy.SpatialReference(4326)
    arcpy.Project_management(in_source, "Drop_duplicated", spatial_ref)
    arcpy.AddField_management("Drop_duplicated", "X", "DOUBLE")
    arcpy.AddField_management("Drop_duplicated", "Y", "DOUBLE")
    arcpy.CalculateField_management("Drop_duplicated", "Y", "!shape.firstpoint.X!","PYTHON_9.3")
    arcpy.CalculateField_management("Drop_duplicated", "X", "!shape.firstpoint.Y!","PYTHON_9.3")
    #dissolve on the X &Y fields
    arcpy.Dissolve_management("Drop_duplicated", out_fc+phi, ["X","Y"])
    arcpy.AddField_management("Drop_duplicated", "concat_1", "TEXT")
    #concatenate the X & Y fields
    arcpy.AddField_management(out_fc+phi, "concat", "TEXT")
    arcpy.CalculateField_management("Drop_duplicated", "concat_1", 'str( !X!)+", "+str( !Y!)', "PYTHON_9.3")
    arcpy.CalculateField_management(out_fc+phi, "concat", 'str( !X!)+", "+str( !Y!)', "PYTHON_9.3")

    #Join to FC that has proper number of features and cope to out_fc
    arcpy.JoinField_management(out_fc+phi, "concat", "Drop_duplicated", "concat_1")
    arcpy.Select_analysis(out_fc+phi, out_fc)
    #delete temp files
    arcpy.Delete_management("Drop_duplicated")
    arcpy.Delete_management(out_fc+phi)