# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:41:45 2019

@author: JacobNordberg
"""

import arcpy

def Erase_analysis(in_source, in_erase,  out_fc):
    # List Input Fields
    fieldnames = []
    fields = arcpy.ListFields(in_source)            
    for field in fields:
        if not field.required:                              
            fieldnames.append(field.name)
    # Copy Input
    arcpy.Select_analysis(in_erase, "EraseGeo")
    arcpy.Select_analysis(in_source, "SourceGeo")
    # Union FC
    arcpy.Union_analysis(["SourceGeo", "EraseGeo"],out_fc+"Union"+phi)
    # Export Output
    arcpy.Select_analysis(out_fc+"Union"+phi, out_fc, 'FID_EraseGeo = -1')

    # Delete Intermediate
    arcpy.Delete_management("EraseGeo")
    arcpy.Delete_management("SourceGeo")
    arcpy.Delete_management(out_fc+"Union"+phi)