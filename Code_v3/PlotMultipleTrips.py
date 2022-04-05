# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 10:46:07 2021

@author: saimu

PLOT MULTPIPLE TRIPS ON THE SAME BOKEH GRAPH
"""

from bokeh.plotting import figure, show, output_notebook, output_file, save
from bokeh.tile_providers import CARTODBPOSITRON, ESRI_IMAGERY, OSM, STAMEN_TERRAIN, STAMEN_TERRAIN_RETINA
from bokeh.tile_providers import get_provider, Vendors 
from bokeh.io import export_png

from LoadExistingUAMaerodromeInfrastructure import *
import numpy as np

class PlotMultipleTrips(LoadExistingUAMaerodromeInfrastructure):
    def __init__(self, MetroName, MapType, PlotGraphs):
        LoadExistingUAMaerodromeInfrastructure.__init__(self, MetroName)
        self.MapType = MapType
        self.p = self.MapperInfrastructure()
        self.plotgraphs = PlotGraphs
        
    def MapperInfrastructure(self):
        if self.MapType == "Satellite":
            tile_provider = get_provider(Vendors.ESRI_IMAGERY)
            # p = figure(x_range=(-9780000-100000, -9745000+100000), y_range=(5130000, 5160000),x_axis_type="mercator", y_axis_type="mercator", title="Chicago Metropolitan Area", plot_width=1875, plot_height=910)
            p = figure(x_range=(-9780000-10000, -9745000+5000), y_range=(5130000-80000, 5160000+80000),x_axis_type="mercator", y_axis_type="mercator", x_axis_label='Longitude (deg)', y_axis_label='Latitude (deg)', title="Chicago Metropolitan Area", plot_width=7680, plot_height=4320)
            p.title.text_font_size = '120pt'
            p.xaxis.axis_label_text_font_size = "80pt"
            p.yaxis.axis_label_text_font_size = "80pt"
            p.xaxis.major_label_text_font_size = "80pt"
            p.yaxis.major_label_text_font_size = "80pt"
            p.add_tile(tile_provider)
            p.square(self.lat_regional_merc, self.lon_regional_merc, color = 'white', line_color="black", line_width=2, alpha = 1, size = 100)
            p.triangle(self.lat_major_merc, self.lon_major_merc, color = 'red', line_color="black", alpha = 1,line_width=2, size = 100)
            p.circle(self.lat_heliports_merc, self.lon_heliports_merc, color = 'yellow', line_color="black", line_width=2, alpha = 1, size = 100)
        
        elif self.MapType == "Map":
            tile_provider = get_provider(Vendors.OSM) #40000
            p = figure(x_range=(-9780000-10000, -9745000+5000), y_range=(5130000-80000, 5160000+80000),x_axis_type="mercator", y_axis_type="mercator", x_axis_label='Longitude (deg)', y_axis_label='Latitude (deg)', title="Chicago Metropolitan Area", plot_width=7680, plot_height=4320)
            p.title.text_font_size = '120pt'
            p.xaxis.axis_label_text_font_size = "80pt"
            p.yaxis.axis_label_text_font_size = "80pt"
            p.xaxis.major_label_text_font_size = "80pt"
            p.yaxis.major_label_text_font_size = "80pt"
            p.add_tile(tile_provider)
            p.square(self.lat_regional_merc, self.lon_regional_merc, color = 'white', line_color="black", line_width=2, alpha = 1, size = 100)
            p.triangle(self.lat_major_merc, self.lon_major_merc, color = 'red', line_color="black", alpha = 1,line_width=2, size = 100)
            p.circle(self.lat_heliports_merc, self.lon_heliports_merc, color = 'yellow', line_color="black", line_width=2, alpha = 1, size = 100)
        
        return p
    
    def Trips(self, DepType, idxDep, ArrType, idxArr, wps):
        # FOR DEPARTURES
        if DepType == "Regional":
            latDep_deg = self.lat_regional_deg[idxDep]
            lonDep_deg = self.lon_regional_deg[idxDep]
            latDep_merc = self.lat_regional_merc[idxDep]
            lonDep_merc = self.lon_regional_merc[idxDep]
        elif DepType == "Major":
            latDep_deg = self.lat_major_deg[idxDep]
            lonDep_deg = self.lon_major_deg[idxDep]
            latDep_merc = self.lat_major_merc[idxDep]
            lonDep_merc = self.lon_major_merc[idxDep]
        elif DepType == "Heliport":
            latDep_deg = self.lat_heliports_deg[idxDep]
            lonDep_deg = self.lon_heliports_deg[idxDep]
            latDep_merc = self.lat_heliports_merc[idxDep]
            lonDep_merc = self.lon_heliports_merc[idxDep]
        
        # FOR ARRIVALS
        if ArrType == "Regional":
            latArr_deg = self.lat_regional_deg[idxArr]
            lonArr_deg = self.lon_regional_deg[idxArr]
            latArr_merc = self.lat_regional_merc[idxArr]
            lonArr_merc = self.lon_regional_merc[idxArr]
        elif ArrType == "Major":
            latArr_deg = self.lat_major_deg[idxArr]
            lonArr_deg = self.lon_major_deg[idxArr]
            latArr_merc = self.lat_major_merc[idxArr]
            lonArr_merc = self.lon_major_merc[idxArr]
        elif ArrType == "Heliport":
            latArr_deg = self.lat_heliports_deg[idxArr]
            lonArr_deg = self.lon_heliports_deg[idxArr]
            latArr_merc = self.lat_heliports_merc[idxArr]
            lonArr_merc = self.lon_heliports_merc[idxArr]
        
        geodesicDistance = self.GeodesicDistance(latDep_deg, lonDep_deg, latArr_deg, lonArr_deg)

        try:
            wp1 = wps
            # print(wp1)
            wp1y, wp1x = self.Degrees2Mercator(wp1)
            
            LonX = [lonDep_merc, wp1x, lonArr_merc]
            LatY = [latDep_merc, wp1y, latArr_merc]
        except:
            LonX = [lonDep_merc, lonArr_merc]
            LatY = [latDep_merc, latArr_merc]
        
        return (LatY, LonX, geodesicDistance)

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

    def PlotTrips(self, q, DepType, ArrType, DEP, ARR, wps):
        # q = self.MapperInfrastructure()
        ListGeodesicDistance = []
        for dep in DEP:
            for arr in ARR:
                LatY, LonX, geodesicDistance = self.Trips(DepType, dep, ArrType, arr, wps)
                q.line(LatY, LonX, color = 'white', line_width = 10)
                ListGeodesicDistance.append(geodesicDistance)
        self.geodistance = ListGeodesicDistance
        # output_file("C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/TripAnimation/test" + number_str.zfill(4) + ".png")
        return q
    
    def GeodesicDistance(self, lat1, long1, lat2, long2):
        # Convert latitude and longitude to
        # spherical coordinates in radians.
        degrees_to_radians = math.pi/180.0

        # phi = 90 - latitude
        phi1 = (90.0 - lat1)*degrees_to_radians
        phi2 = (90.0 - lat2)*degrees_to_radians

        # theta = longitude
        theta1 = long1*degrees_to_radians
        theta2 = long2*degrees_to_radians

        # Compute spherical distance from spherical coordinates.

        # For two locations in spherical coordinates
        # (1, theta, phi) and (1, theta', phi')
        # cosine( arc length ) =
        # sin phi sin phi' cos(theta-theta') + cos phi cos phi'
        # distance = rho * arc length

        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
        math.cos(phi1)*math.cos(phi2))
        try:
            arc = math.acos( cos )
        except ValueError:
            if cos>1:
                arc = math.acos(1)
            elif cos < -1:
                arc = math.acos(-1)
        

        # Remember to multiply arc by the radius of the earth
        # in your favorite set of units to get length. In this case, in miles
        return arc*6371*0.621371
    
    
Chicago_Network_A = PlotMultipleTrips("Chicago", "Satellite", False)
q = Chicago_Network_A.MapperInfrastructure()

# FOR PLOTTING MULTIPLE TRIPS
# DepType = "Regional"
# ArrType = "Heliport"
# DEP = [7, 9, 13, 9]
# ARR = [8, 6, 7, 11]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR)

# DepType = "Heliport"
# ArrType = "Heliport"
# DEP = [1, 2, 3, 4, 5, 8, 6, 7, 11]
# ARR = [1, 2, 3, 4, 5, 6, 7, 11, 8]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR)

""" USE CASE A: MULTIPLE DEPARTURE AERODROMES, ONE ARRIVAL AERODROME"""
# DepType = "Regional"
# ArrType = "Heliport"
# DEP = [13]
# ARR = [8]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR,(()))

# DepType = "Regional"
# ArrType = "Heliport"
# DEP = [9, 7, 2, 0, 8, 10, 3]
# ARR = [8]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR, ((41.89177, -88.05804)))

# DepType = "Regional"
# ArrType = "Heliport"
# DEP = [4, 6, 11, 14, 1]
# ARR = [8]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR, ((42.2165, -88.05187)))

# DepType = "Regional"
# ArrType = "Heliport"
# DEP = [16, 15]
# ARR = [8]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR, ((41.68056, -87.62217)))

# DepType = "Heliport"
# ArrType = "Heliport"
# DEP = [4, 2, 3, 5]
# ARR = [8]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR, ((41.68056, -87.62217)))

# DepType = "Heliport"
# ArrType = "Heliport"
# DEP = [9, 10]
# ARR = [8]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR, ((41.89177, -88.05804)))

# DepType = "Heliport"
# ArrType = "Heliport"
# DEP = [12, 13]
# ARR = [8]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR, ((42.2165, -88.05187)))

# DepType = "Heliport"
# ArrType = "Heliport"
# DEP = [11]
# ARR = [8]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR, (()))

""" USE CASE A: MULTIPLE DEPARTURE AERODROMES, ONE ARRIVAL AERODROME"""
# DepType = "Regional"
# ArrType = "Regional"
# DEP = [0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 13, 14, 15, 16]
# ARR = [7]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR, (()))

# """ USE CASE B: MULTIPLE DEPARTURE AERODROMES, ONE ARRIVAL AERODROME"""
# DepType = "Heliport"
# ArrType = "Heliport"
# DEP = [2, 3, 4, 5, 9, 10, 11, 12, 13]
# ARR = [8]
# q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR, (()))

# """ USE CASE C: MULTIPLE DEPARTURE AERODROMES, ONE ARRIVAL AERODROME"""
DepType = "Heliport"
ArrType = "Heliport"
# DEP = [2, 3, 4, 5, 8, 9, 10, 11, 12, 13]
# ARR = [2, 3, 4, 5, 8, 9, 10, 11, 12, 13]
DEP = [2, 3, 4, 5, 8, 9, 10, 11, 12, 13]
ARR = [2, 3, 4, 5, 8, 9, 10, 11, 12, 13]

q = Chicago_Network_A.PlotTrips(q, DepType, ArrType, DEP, ARR, (()))

geodistance_numpy = np.array(Chicago_Network_A.geodistance)
df = pd.DataFrame(geodistance_numpy, columns=['Geodesic Distance [miles]'])
df.to_excel (r'C:/Users/Sai Mudumba/OneDrive - purdue.edu/Purdue Graduate School/MS_Aeronautical_Astronautical_Engineering/MS Thesis Research/Fall 2021/GeodesicDistance.xlsx', index = False, header=True)

filename="C:/Users/Sai Mudumba/OneDrive - purdue.edu/Purdue Graduate School/MS_Aeronautical_Astronautical_Engineering/MS Thesis Research/Fall 2021/Python_Code/Results/Miscellaneous/MultipleTrips.png"
export_png(q, filename=filename)