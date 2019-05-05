## Import arcpy module and set up workspace
import arcpy
from arcpy import env
env.workspace = "C:/Users/xiaoqiu2\Documents\FinalProject"
env.overwriteOutput = True
## Create buffer based on the hospital shapefile
arcpy.Buffer_analysis("Chicago_hospitals_pts.shp","Hospital_Buffer_1mile","1 MILE")
## Erase the area that already covered by the current hospital
arcpy.Erase_analysis("CensusTract_prj.shp", "Hospital_Buffer_1mile.shp", "District_Erase_1mile")
## Count the number of bulglaries on the un-erased area of each district
arcpy.SpatialJoin_analysis("District_Erase_1mile.shp","Burglaries_2016.shp","SpatialJoin_B_1mile")
## Add a new field to the new spatial join layer
fc = "SpatialJoin_B_1mile.shp"
newfield = "Add hos"
fieldtype = "TEXT"
fieldname = arcpy.ValidateFieldName(newfield)
arcpy.AddField_management(fc, fieldname, fieldtype, "", "", 12)
## Use field calculator to update the new field to show whether new hospitals should be built on the current district
inTable = "SpatialJoin_B_1mile.shp"
fieldName = "Add_hos"
expression = "Ifadd(int(!Join_Count!))"
codeblock = """
def Ifadd(number):
    if number <= 15:
        return "No"
    else:
        return "Yes" """
arcpy.CalculateField_management(inTable, fieldName,expression,"PYTHON_9.3",codeblock)

## Do the same thing, but use the number of homicides instead of bulglaries this time.
arcpy.SpatialJoin_analysis("District_Erase_1mile.shp","Homicides_2016.shp","SpatialJoin_H_1mile")
fc = "SpatialJoin_H_1mile.shp"
newfield = "Add hos"
fieldtype = "TEXT"
fieldname = arcpy.ValidateFieldName(newfield)
arcpy.AddField_management(fc, fieldname, fieldtype, "", "", 12)
inTable = "SpatialJoin_H_1mile.shp"
fieldName = "Add_hos"
expression = "Ifadd(int(!Join_Count!))"
codeblock = """
def Ifadd(number):
    if number <= 3:
        return "No"
    else:
        return "Yes" """
arcpy.CalculateField_management(inTable, fieldName,expression,"PYTHON_9.3",codeblock)
## Find out which districts have high homicides and bulglaries cases but are lack of hospitals
arcpy.Select_analysis("SpatialJoin_B_1mile.shp", "B_NeedNewHos", "Add_hos = 'YES'")
arcpy.Select_analysis("SpatialJoin_H_1mile.shp", "H_NeedNewHos", "Add_hos = 'YES'")
arcpy.Clip_analysis("B_NeedNewHos.shp", "H_NeedNewHos.shp", "Target_District")


         
