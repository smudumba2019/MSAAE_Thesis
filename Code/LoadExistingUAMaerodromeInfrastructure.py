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
    LoadExistingUAMAerodromeInfrastructure is a class that loads an excel spreadsheet of aerodrome locations from a folder
    
    Inputs:
        Name of the metropolitan area (e.g., "Chicago" or "Dallas")
    
    Attributes:
        1. FilePath
        2. ...
        
        
    Methods:
        1. ReadExcelSheet - reads in mercator coordinates with units in meters
        2. ReadExcelSheetInDegreesOnly
        3. InMercator
        4. Degrees2Mercator
        5. Mercator2Degrees
    
    """
    
    def __init__(self, MetroName):
        self.MetroName = MetroName
        self.FilePath = "C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Datasets/" + self.MetroName + "/" + self.MetroName + ".xlsx"
        
        self.lat_regional_merc, self.lon_regional_merc = self.ReadExcelSheet(self.FilePath, "Regional")
        self.lat_major_merc, self.lon_major_merc = self.ReadExcelSheet(self.FilePath, "Major")
        self.lat_heliports_merc, self.lon_heliports_merc = self.ReadExcelSheet(self.FilePath, "Heliports")
        
        self.lat_regional_deg, self.lon_regional_deg = self.ReadExcelSheetInDegreesOnly(self.FilePath, "Regional")
        self.lat_major_deg, self.lon_major_deg = self.ReadExcelSheetInDegreesOnly(self.FilePath, "Major")
        self.lat_heliports_deg, self.lon_heliports_deg = self.ReadExcelSheetInDegreesOnly(self.FilePath, "Heliports")

    def ReadExcelSheet(self, FilePath, SheetName):
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
        d = {"LatD" : lat_deg, "LonD" : lon_deg}
        all_p = pd.DataFrame(data = d)
        
        lat_merc = []
        lon_merc = []
        for i in range(len(all_p)):
            lat, lon = self.Degrees2Mercator((all_p["LatD"][i], all_p["LonD"][i]))
            lat_merc.append(lat)
            lon_merc.append(lon)
        
        return lat_merc, lon_merc
    
    def Degrees2Mercator(self, Coords):
        """
        Converts to Mercator Coordinates from Latitude, Longitude in degrees because bokeh module depends on it
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
    