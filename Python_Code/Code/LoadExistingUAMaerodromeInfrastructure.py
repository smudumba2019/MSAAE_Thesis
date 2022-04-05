# -*- coding: utf-8 -*-
"""
Author: Sai V. Mudumba
Code Conceived: March, 2021
Code Last Modified: May 15, 2021
"""

import pandas as pd # see pandas documentation
import math

class LoadExistingUAMaerodromeInfrastructure:
    """
    CLASS DEFINITION:
        LoadExistingUAMAerodromeInfrastructure is a class that
        - loads an excel spreadsheet (.xlsx) of aerodrome locations from a folder
        - converts the lat, lon coordinates from degrees to mercator so that they can be plotted on a tilemap using Bokeh library
        *** see the excel document to see how it is formatted ***
        
    INPUT(S):
        Name of the metropolitan area (e.g., "Chicago" or "Dallas")
    
    ATTRIBUTE(S):
        1. MetroName: name of the metropolitan area (e.g., "Chicago") 
        2. FilePath: this is the location of the excel spreadsheet
        3. lat_regional_merc: read latitude information in mercator coordinates
        4. lon_regional_merc: read longitude information in mercator coordinates
        5. lat_regional_deg: read latitude information in degree coordinates
        6. lon_regional_deg: read latitude information in degree coordinates
        7. (...) same as above for other types of aerodromes (i.e., major and heliports)    
    
    METHOD(S):
        1. ReadExcelSheetInMercatorOnly - reads lat, lon coordinates (provided in degrees) in mercator coordinates, with units in meters
        2. ReadExcelSheetInDegreesOnly - reads lat, lon coordinates as provided in the excel spreadsheet, without converting it to mercator coordinates
        3. InMercator - this function creates two more columns in the pandas database for lat and lon in mercator coordinates
        4. Degrees2Mercator - converts (lat, lon) from degrees to mercator coordinates
        5. Mercator2Degrees - converts (lat, lon) from mercator to degrees
    """
    
    def __init__(self, MetroName):
        self.MetroName = MetroName
        self.FilePath = "C:/Users/saimu/OneDrive - purdue.edu/Purdue Graduate School/MS_Aeronautical_Astronautical_Engineering/MS Thesis Research/Spring 2022/Python_Code/Datasets/" + self.MetroName + "/" + self.MetroName + ".xlsx"
        
        self.lat_regional_merc, self.lon_regional_merc = self.ReadExcelSheetInMercatorOnly(self.FilePath, "Regional")
        self.lat_major_merc, self.lon_major_merc = self.ReadExcelSheetInMercatorOnly(self.FilePath, "Major")
        self.lat_heliports_merc, self.lon_heliports_merc = self.ReadExcelSheetInMercatorOnly(self.FilePath, "Heliports")
        self.lat_golfcourses_merc, self.lon_golfcourses_merc = self.ReadExcelSheetInMercatorOnly(self.FilePath, "GolfCourses")

        self.lat_regional_deg, self.lon_regional_deg = self.ReadExcelSheetInDegreesOnly(self.FilePath, "Regional")
        self.lat_major_deg, self.lon_major_deg = self.ReadExcelSheetInDegreesOnly(self.FilePath, "Major")
        self.lat_heliports_deg, self.lon_heliports_deg = self.ReadExcelSheetInDegreesOnly(self.FilePath, "Heliports")
        self.lat_golfcourses_deg, self.lon_golfcoursess_deg = self.ReadExcelSheetInDegreesOnly(self.FilePath, "GolfCourses")        

    def ReadExcelSheetInMercatorOnly(self, FilePath, SheetName):
        loadSheet = pd.read_excel(FilePath, sheet_name = SheetName)
        lat_deg = loadSheet["LatD"]
        lon_deg = loadSheet["LonD"]
        lat_merc, lon_merc = self.InMercator(lat_deg, lon_deg)
        return lat_merc, lon_merc
    
    def ReadExcelSheetInDegreesOnly(self, FilePath, SheetName):
        loadSheet = pd.read_excel(FilePath, sheet_name = SheetName)
        lat_deg = loadSheet["LatD"]
        lon_deg = loadSheet["LonD"]
        return lat_deg, lon_deg
        
    def InMercator(self, lat_deg, lon_deg):
        d = {"LatD" : lat_deg, "LonD" : lon_deg} # a dictionary - keys: Lat, Lon - values: list of coordinates in degrees
        all_p = pd.DataFrame(data = d) # creates a 2D data structure, with two columns named LatD, LonD
        
        lat_merc = []
        lon_merc = []
        for i in range(len(all_p)):
            lat, lon = self.Degrees2Mercator((all_p["LatD"][i], all_p["LonD"][i]))
            lat_merc.append(lat)
            lon_merc.append(lon)
        
        return lat_merc, lon_merc
    
    def Degrees2Mercator(self, Coords):
        """
        Takes in a tuple as an input.
        Converts to Mercator Coordinates from Latitude, Longitude in degrees
        Input = e.g., (42, -88)
        Output = e.g., (-9780000, -9745000)
        """
        Coordinates = Coords
    
        lat = Coordinates[0]
        lon = Coordinates[1]
    
        r_major = 6378137.000
        x = r_major * math.radians(lon)
        scale = x/lon
        y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 + lat * (math.pi/180.0)/2.0)) * scale
    
        return (x, y)
    
    def Mercator2Degrees(self, x, y):
        """
        https://www.usna.edu/Users/oceano/pguth/md_help/html/mapb0iem.htm
        """
        R = 6378137.000
        lat = math.pi/2 - 2 * math.atan(math.exp(-y/R))
        lon = x/R
        return (lat*180/math.pi, lon*180/math.pi)        
        
    def __call__(self):
        print(self.lat_regional_merc, self.lon_regional_merc, self.lat_major_merc, self.lon_major_merc, self.lat_heliports_merc, self.lon_heliports_merc)
        return self.lat_regional_merc, self.lon_regional_merc, self.lat_major_merc, self.lon_major_merc, self.lat_heliports_merc, self.lon_heliports_merc

## TEST SCRIPT:
# a = LoadExistingUAMaerodromeInfrastructure("Chicago")
# b = a.lat_regional_deg
# print(type(list(b)))
# l = len(a.lat_regional_deg)
# print(l)
# for i in range(l):
#     print(b[i])