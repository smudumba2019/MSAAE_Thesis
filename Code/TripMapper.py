# -*- coding: utf-8 -*-
"""
Author: Sai V. Mudumba
Code Conceived: March, 2021
Code Last Modified: May 15, 2021
"""

"""
Ref 1: https://towardsdatascience.com/exploring-and-visualizing-chicago-transit-data-using-pandas-and-bokeh-part-ii-intro-to-bokeh-5dca6c5ced10
Ref 2: https://stackoverflow.com/questions/57051517/cant-plot-dots-over-tile-on-bokeh
Ref 3: https://docs.bokeh.org/en/latest/docs/reference/tile_providers.html
Ref 4: https://matplotlib.org/2.0.2/examples/color/named_colors.html
Ref 5: https://stackoverflow.com/questions/44281863/saving-html-file-with-images-in-bokeh/44282125
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain

from bokeh.plotting import figure, show, output_notebook, output_file, save
from bokeh.tile_providers import CARTODBPOSITRON, ESRI_IMAGERY, OSM, STAMEN_TERRAIN, STAMEN_TERRAIN_RETINA
from bokeh.tile_providers import get_provider, Vendors 
from bokeh.io import export_png

from LoadExistingUAMaerodromeInfrastructure import *
from FlightProfile import *
from Aircraft import *

class TripMapper(LoadExistingUAMaerodromeInfrastructure):
    """
    CLASS DEFINITION:
        TripMapper is in charge of mapping the trip on a graph. It
        - inherits LoadExistingUAMaerodromeInfrastructure class, so that the coordinates of existing aerodrome could be used for plotting and analysis
    
    INPUT(S):
        1. MetroName: name of the metropolitan area (e.g., "Chicago", "Dallas")
        2. MapType: map style (e.g, "Satellite", "terrain", "OSM", etc.)
        
    ATTRIBUTE(S):
        1. LoadExistingUAMaerodromeInfrastructure.__init__(self, MetroName) inherits this class and the attributes related to the input metroname
        2. MapType: map style (e.g, "Satellite", "terrain", "OSM", etc.)
        3. p: data structure that contains the plotter information from running MapperInfrastructure Method
    
    METHOD(S):
        1. MapperInfrastructure: maps out the metro area, on a specified map style, and the existing aerodromes using Bokeh library
        2. TripDistance: given two aerodromes, this function estimates the geodesic trip distance between these two points in miles, using GeodesicDistance Method
        3. DrawGeodesicTrip: given two aerodromes, one departing and one arrival, this function plots the geodesic trip route on the map attribute "p"; also plots the reachable footprint of an aircraft under emergency conditions
            - in most cases, a trip may not be on a geodesic route; so waypoints, in mercator coordinates, should be incorporated for defining non-direct routes; the number of waypoints is up to the user
        4. (Coming Soon!) DrawNonDirectRoutingTrip: incorporating waypoints, this function does the same execution as Method 3, but for non-direct routing cases
    
    """
    
    def __init__(self, MetroName, MapType):
        LoadExistingUAMaerodromeInfrastructure.__init__(self, MetroName)
        self.MapType = MapType
        self.p = self.MapperInfrastructure()
        
    def MapperInfrastructure(self):
        if self.MapType == "Satellite":
            tile_provider = get_provider(Vendors.ESRI_IMAGERY)
        elif self.MapType == "Map":
            tile_provider = get_provider(Vendors.OSM)
            
        p = figure(x_range=(-9780000-100000, -9745000+100000), y_range=(5130000, 5160000),x_axis_type="mercator", y_axis_type="mercator", title="Chicago Metropolitan Area", plot_width=1875, plot_height=910)
        p.add_tile(tile_provider)
        p.circle(self.lat_regional_merc, self.lon_regional_merc, color = 'white', alpha = 1, size = 10)
        p.circle(self.lat_major_merc, self.lon_major_merc, color = 'deepskyblue', alpha = 1, size = 10)
        p.circle(self.lat_heliports_merc, self.lon_heliports_merc, color = 'yellow', alpha = 1, size = 10)
        return p
    
    def TripDistance(self, DepType, ArrType, idxDep, idxArr):
        if DepType == "Regional":
            latDep_deg = self.lat_regional_deg[idxDep]
            lonDep_deg = self.lon_regional_deg[idxDep]
        elif DepType == "Major":
            latDep_deg = self.lat_major_deg[idxDep]
            lonDep_deg = self.lon_major_deg[idxDep]
        elif DepType == "Heliport":
            latDep_deg = self.lat_heliports_deg[idxDep]
            lonDep_deg = self.lon_heliports_deg[idxDep]
        
        if ArrType == "Regional":
            latArr_deg = self.lat_regional_deg[idxArr]
            lonArr_deg = self.lon_regional_deg[idxArr]
        elif ArrType == "Major":
            latArr_deg = self.lat_major_deg[idxArr]
            lonArr_deg = self.lon_major_deg[idxArr]
        elif ArrType == "Heliport":
            latArr_deg = self.lat_heliports_deg[idxArr]
            lonArr_deg = self.lon_heliports_deg[idxArr]
    
        geodesicDistance = self.GeodesicDistance(latDep_deg, lonDep_deg, latArr_deg, lonArr_deg)
        tripDistance = geodesicDistance
        return tripDistance
    
    def DrawNonDirectRoutingTrip(self, DepType, ArrType, idxDep, idxArr, Aircraft, CruiseAltitudeInFeet):
        X, Y, Radial, FootprintDistance = Aircraft.ReachableGroundFootprint(CruiseAltitudeInFeet,45,0)
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
        
        # FIND GEODESIC TRIP DISTANCE
        geodesicDistance = self.GeodesicDistance(latDep_deg, lonDep_deg, latArr_deg, lonArr_deg)
        self.tripDistance = geodesicDistance
        print(f'Geodesic Trip Distance between {DepType} {idxDep} - {ArrType} {idxArr}: {geodesicDistance} miles')
        
        # DEFINE WAYPOINTS
        LatWaypoints_inDeg = [latDep_deg, latArr_deg]
        LonWaypoints_inDeg = [lonDep_deg, lonArr_deg]
        LatWaypoints_inMerc = [latDep_merc, latArr_merc]
        LonWaypoints_inMerc = [lonDep_merc, lonArr_merc]
        
        lonWP_inDeg = [-88.2,-88.108, -88] #(lonDep_deg + lonArr_deg) / 2
        latWP_inDeg = [41.83,41.99,42] #(latDep_deg + latArr_deg) / 2
        howManyWaypoints = len(lonWP_inDeg)

        for w in range(howManyWaypoints):
            latWP_inMerc, lonWP_inMerc = self.Degrees2Mercator((latWP_inDeg[w], lonWP_inDeg[w]))
            LatWaypoints_inDeg.insert(w+1, latWP_inDeg[w])
            LonWaypoints_inDeg.insert(w+1, lonWP_inDeg[w])
            LatWaypoints_inMerc.insert(w+1, latWP_inMerc)
            LonWaypoints_inMerc.insert(w+1, lonWP_inMerc)
                
        LatArrayforAllWaypoints_inMerc = []
        LonArrayforAllWaypoints_inMerc = []
        LatArrayforAllWaypoints_inDeg = []
        LonArrayforAllWaypoints_inDeg = []
        TripHeadingArrayforAllWaypoints_inDeg = []
        TripDistanceNonDirectRouteArray = []
        
        for l in range(len(LonWaypoints_inMerc)-1):
            Lat_inMerc, Lon_inMerc, TripHeading = self.WaypointsConnector((LatWaypoints_inMerc[l], LonWaypoints_inMerc[l]),(LatWaypoints_inMerc[l+1], LonWaypoints_inMerc[l+1]),250)
            LatArrayforAllWaypoints_inMerc.append(Lat_inMerc)
            LonArrayforAllWaypoints_inMerc.append(Lon_inMerc)
            
            Lat_inDeg, Lon_inDeg, TripHeading_deg = self.WaypointsConnector((LatWaypoints_inDeg[l], LonWaypoints_inDeg[l]),(LatWaypoints_inDeg[l+1], LonWaypoints_inDeg[l+1]),250)
            LatArrayforAllWaypoints_inDeg.append(Lat_inDeg)
            LonArrayforAllWaypoints_inDeg.append(Lon_inDeg)
            
            TripHeadingArrayforAllWaypoints_inDeg.append(TripHeading_deg) # node it's TripHeading_deg

            TripDistanceWP = self.GeodesicDistance(LatWaypoints_inDeg[l], LonWaypoints_inDeg[l], LatWaypoints_inDeg[l+1], LonWaypoints_inDeg[l+1])
            TripDistanceNonDirectRouteArray.append(TripDistanceWP)
            
        # FLATTEN THE NESTED LISTS INTO ONE SINGLE LIST
        self.LatArrayforAllWaypoints_inMerc_flattened = list(chain.from_iterable(LatArrayforAllWaypoints_inMerc))
        self.LonArrayforAllWaypoints_inMerc_flattened = list(chain.from_iterable(LonArrayforAllWaypoints_inMerc))
        self.LatArrayforAllWaypoints_inDeg_flattened = list(chain.from_iterable(LatArrayforAllWaypoints_inDeg))
        self.LonArrayforAllWaypoints_inDeg_flattened = list(chain.from_iterable(LonArrayforAllWaypoints_inDeg))
        
        TripDistanceNonDirectRoute = sum(TripDistanceNonDirectRouteArray)
        self.TripDistanceNonDirectRoute = TripDistanceNonDirectRoute
        DetourRatio = self.CalculateDetourRatio()

        print(f'Trip Distance with Non-direct routing: {TripDistanceNonDirectRoute} miles')
        print(f'Detour Ratio: {DetourRatio*100} % Longer')
        print(f'Heading Direction: {TripHeadingArrayforAllWaypoints_inDeg} deg')

        # FIND THE CLOSEST CONTINGENCY UAM AERODROME FROM THE VEHICLE'S POSITION ALONG THE ROUTE
        Distance2ClosestContingencySite, Direction, Labeling = self.FindClosestUAMaerodromeAlongTheRoute()      

        # PLOT THE PATH ON THE BOKEH PLOT, ALSO THE REACHABLE RADIUS ON THE PLOT
        # ROTATE THE REACHABLE FOOTPRINT COORDINATES BY TRIP HEADING DIRECTION
        for n in range(howManyWaypoints+1):
            self.p.line(LatArrayforAllWaypoints_inMerc[n], LonArrayforAllWaypoints_inMerc[n], color = 'white', line_width = 2)
            X_new, Y_new = self.RotateReachableFootprintByTripHeading(X, Y, TripHeadingArrayforAllWaypoints_inDeg[n])
            self.PlotReachableRadiusAlongRoute(LatArrayforAllWaypoints_inMerc[n], LonArrayforAllWaypoints_inMerc[n], X_new, Y_new)
    
    def FindClosestUAMaerodromeAlongTheRoute(self):
        DistanceLinspace = np.linspace(0, self.TripDistanceNonDirectRoute, len(self.LatArrayforAllWaypoints_inMerc_flattened))        
        Distance2ClosestContingencySite = [] # in miles
        Labeling = [] # type of aerodrome (e.g., regional, major, or heliport?)
        Direction = [] # finds the direction of the closest contingency landing site relative to Northward reference
        
        for j in range(len(self.LatArrayforAllWaypoints_inMerc_flattened)): # j represents the each step of the vehicle along the path
            Distance2ContingencySite_Regional_Airport = [] # array containing distance from current position to the regional airports
            Distance2ContingencySite_Major_Airport = [] # array containing distance from current position to the major airports
            Distance2ContingencySite_Heliport = [] # array containing distance from current position to the heliports

            for k in range(len(self.lat_regional_deg)): # k represents each location index of regional airport
                Distance2ContingencySite_Regional_Airport.append(self.GeodesicDistance(self.LatArrayforAllWaypoints_inDeg_flattened[j], self.LonArrayforAllWaypoints_inDeg_flattened[j], self.lat_regional_deg[k], self.lon_regional_deg[k])) # in miles
            
            for l in range(len(self.lat_heliports_deg)): # l represents each location index of heliports
                Distance2ContingencySite_Heliport.append(self.GeodesicDistance(self.LatArrayforAllWaypoints_inDeg_flattened[j], self.LonArrayforAllWaypoints_inDeg_flattened[j], self.lat_heliports_deg[l], self.lon_heliports_deg[l])) # in miles
            
            for m in range(len(self.lat_major_deg)): # m represents each location index of major airport
                Distance2ContingencySite_Major_Airport.append(self.GeodesicDistance(self.LatArrayforAllWaypoints_inDeg_flattened[j], self.LonArrayforAllWaypoints_inDeg_flattened[j], self.lat_major_deg[m], self.lon_major_deg[m])) # in miles    
            
            # FIND THE CLOSEST OF [REGIONAL, HELIPORT, MAJOR] TO THE CURRENT LOCATION
            # THIS IS AN IMPORTANT PART OF THE CODE THAT COULD BE USED TO EXCLUDE CERTAIN TYPES OF AERODROMES
            minOfAll = [min(Distance2ContingencySite_Regional_Airport), min(Distance2ContingencySite_Heliport), min(Distance2ContingencySite_Major_Airport)]
            
            Distance2ClosestContingencySite.append(min(minOfAll)) # find the closest one at the current location
            indexMin = minOfAll.index(min(minOfAll)) # find the index: 0 - regional, 1 - heliport, 2 - major airport
            Labeling.append(int(indexMin)) 
            
            # FIND THE DIRECTION OF THE CLOSEST CONTINGENCY LANDING SITE RELATIVE TO NORTH POLE REFERENCE
            if int(indexMin) == 0: # if regional airport
                idx = Distance2ContingencySite_Regional_Airport.index(min(minOfAll))
                deltaLat = self.lat_regional_deg[idx] - self.LatArrayforAllWaypoints_inDeg_flattened[j]
                deltaLon = self.lon_regional_deg[idx] - self.LonArrayforAllWaypoints_inDeg_flattened[j]
                
            elif int(indexMin) == 1: # if heliport
                idx = Distance2ContingencySite_Heliport.index(min(minOfAll))
                deltaLat = self.lat_heliports_deg[idx] - self.LatArrayforAllWaypoints_inDeg_flattened[j]
                deltaLon = self.lon_heliports_deg[idx] - self.LonArrayforAllWaypoints_inDeg_flattened[j]
                
            elif int(indexMin) == 2: # if major airport
                idx = Distance2ContingencySite_Major_Airport.index(min(minOfAll))
                deltaLat = self.lat_major_deg[idx] - self.LatArrayforAllWaypoints_inDeg_flattened[j]
                deltaLon = self.lon_major_deg[idx] - self.LonArrayforAllWaypoints_inDeg_flattened[j]
            
            if deltaLon >= 0 and deltaLat >= 0: # the first quadrant
                if deltaLon == 0 and deltaLat == 0:
                    directionAngle_rad = 0
                    directionAngle_deg = 0
                    Direction.append(directionAngle_deg)
                else:
                    directionAngle_rad = math.atan(deltaLon/deltaLat)
                    directionAngle_deg = directionAngle_rad * 180 / math.pi
                    Direction.append(directionAngle_deg)
            elif deltaLon < 0 and deltaLat >= 0: # the second quadrant
                directionAngle_rad = 2 * math.pi + math.atan(deltaLon/deltaLat)
                directionAngle_deg = directionAngle_rad * 180 / math.pi
                Direction.append(directionAngle_deg)
            elif deltaLon > 0 and deltaLat < 0: # the fourth quadrant
                directionAngle_rad = math.pi + math.atan(deltaLon/deltaLat)
                directionAngle_deg = directionAngle_rad * 180 / math.pi
                Direction.append(directionAngle_deg)
            elif deltaLon < 0 and deltaLat < 0: # the third quadrant
                directionAngle_rad = math.atan(deltaLon/deltaLat) + math.pi
                directionAngle_deg = directionAngle_rad * 180 / math.pi
                Direction.append(directionAngle_deg)
            elif deltaLon == 0 and deltaLat > 0:
                directionAngle_rad = math.pi / 2
                directionAngle_deg = directionAngle_rad * 180 / math.pi
                Direction.append(directionAngle_deg)
            elif deltaLon == 0 and deltaLat < 0:
                directionAngle_rad = 2 * math.pi - (math.pi / 2)
                directionAngle_deg = directionAngle_rad * 180 / math.pi
                Direction.append(directionAngle_deg)
                
        fig, (ax1, ax2, ax3) = plt.subplots(3,1)
        fig.set_size_inches(8, 16)
        ax1.plot(DistanceLinspace, Distance2ClosestContingencySite, label="Flight Path")
        #plt.plot(DistanceLinspace, [glideDistance]*sampSize, 'r--', label="Threshold Line")
        ax1.set_xlabel("Trip Length Completed [miles]")
        ax1.set_ylabel("Closest Contingency Landing Site Distance [miles]")
        ax1.grid()

        #plt.figure(figsize=(8,5))
        ax2.plot(DistanceLinspace, Labeling, 'r-', label="Threshold Line")
        ax2.set_xlabel("Trip Length Completed [miles]")
        ax2.set_label("Closest Contingency Landing Site Distance [miles]")
        ax2.set_yticks([0,1,2])
        ax2.set_yticklabels(['Regional', 'Heliport', 'Major'])
        ax2.grid()

        
        #plt.figure(figsize=(8,5)) [0:sampSize-2]
        ax3.plot(DistanceLinspace, Direction, 'r-', label="Threshold Line")
        ax3.set_xlabel("Trip Length Completed [miles]")
        ax3.set_ylabel("Heading Direction [degrees]")
        ax3.set_title("Direction of Contingency Landing Site Rel. To North")
        ax3.grid()

        plt.savefig('C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/HeadingDirectionVsTripLength_nonDirect.png', dpi=300)
        return (Distance2ClosestContingencySite, Direction, Labeling)
                
    def RotateReachableFootprintByTripHeading(self, X, Y, teta):
        X_new = []
        Y_new = []
        teta = (teta) * math.pi/180
        phaseShift = -math.pi/2
        # BECAUSE THERE IS DISCREPENCY BETWEEN MERCATOR METERS AND ACTUAL METERS, MULTIPLY BY 5000/3730 
        # THIS CONVERTS FROM ACTUAL METERS TO MERCATOR METERS FOR PROJECTION
        for i in range(len(X)):
            X_new.append((X[i]*np.cos(teta - phaseShift) - Y[i]*np.sin(teta - phaseShift)) * 5000/3730) 
            Y_new.append(-(X[i]*np.sin(teta - phaseShift) + Y[i]*np.cos(teta - phaseShift)) * 5000/3730)
        
        self.X = X_new
        self.Y = Y_new
        return X_new, Y_new  
    
    def PlotReachableRadiusAlongRoute(self, Lat, Lon, X_new, Y_new):
        for j in range(len(Lat)):
            # LAT_DEG = []
            # LON_DEG = []
            # DIST = []
            # for i in range(len(X)):
            #     lat_deg, lon_deg = self.Mercator2Degrees((Lat[j]+Y_new[i]),(Lon[j]-X_new[i]))
            #     #print(Lat_deg[j], Lon_deg[j], lat_deg, lon_deg)
            #     DST = self.GeodesicDistance(Lat_deg[j], Lon_deg[j], lat_deg, lon_deg)
            #     LAT_DEG.append(lat_deg)
            #     LON_DEG.append(lon_deg)
            #     DIST.append(DST)
                            
            if j % 100 == 50:
                self.p.circle(Lat[j], Lon[j], color = 'yellow', alpha = 1, size = 3)
                self.p.patch(Lat[j]*np.ones(len(Y_new))+Y_new, Lon[j]*np.ones(len(X_new))-X_new, alpha = 0.3, color="white")
        return None
    
        
    def CalculateDetourRatio(self):
        DR = (self.TripDistanceNonDirectRoute - self.tripDistance) / self.tripDistance 
        return DR
    
    def DrawGeodesicTrip(self, DepType, ArrType, idxDep, idxArr, X, Y):
        sampSize = 500
        self.sampleSize = sampSize
        
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
        self.tripDistance = geodesicDistance
        print(f'Geodesic Trip Distance between {idxDep} - {idxArr}: {geodesicDistance} miles')
        
        # CREATES AN ARRAY OF LAT, LON COORDINATES BETWEEN WAYPOINTS FOR PLOTTING ON BOKEH TILEMAPS
        Lat, Lon, TripHeading = self.WaypointsConnector((latDep_merc, lonDep_merc),(latArr_merc, lonArr_merc),500)
        Lat_deg, Lon_deg, TripHeading_deg = self.WaypointsConnector((latDep_deg, lonDep_deg),(latArr_deg, lonArr_deg),500)

        self.p.line(Lat, Lon, color = 'white', line_width = 2)
        
        # # Find the angle of the slope relative to the North
        # TripHeading = math.atan(1/delta) * 180/math.pi
        print(f'Heading Angle is {TripHeading} deg')
        self.triphead = TripHeading
        
        # Rotate the reachability footprint based on the trip heading angle
        if TripHeading < 0:
            teta = 2*np.pi + TripHeading*np.pi/180
        else:
            teta = 2*np.pi + TripHeading*np.pi/180
        
        X_new = []
        Y_new = []
        
        for i in range(len(X)):
            X_new.append((X[i]*np.cos(teta) - Y[i]*np.sin(teta)) * 5000/3730)
            Y_new.append((X[i]*np.sin(teta) + Y[i]*np.cos(teta)) * 5000/3730)
        
        self.X = X_new
        self.Y = Y_new
        
        # # Use the linear function equation to define the time steps, in mercator coordinates
        # Lon = np.linspace(lonDep_merc, lonArr_merc, sampSize) 
        # Lat = (delta * (Lon - lonDep_merc) + latDep_merc)
        # self.p.line(Lat, Lon, color = 'white', line_width = 2)
        
        # # same thing as above, but this is in degrees
        # delta_deg = (latArr_deg-latDep_deg)/(lonArr_deg-lonDep_deg)
        # Lon_deg = np.linspace(lonDep_deg, lonArr_deg, sampSize) 
        # Lat_deg = (delta_deg * (Lon_deg - lonDep_deg) + latDep_deg)
        # Lat_deg, Lon_deg, TripHeading_deg = self.WaypointsConnector((latDep_deg, lonDep_deg),(latArr_deg, lonArr_deg),500)

        # plot the reachable radius along the trip
        
        DistanceLinspace = np.linspace(0,geodesicDistance,sampSize)
        
        for j in range(len(Lat)):
            LAT_DEG = []
            LON_DEG = []
            DIST = []
            for i in range(len(X)):
                lat_deg, lon_deg = self.Mercator2Degrees((Lat[j]+Y_new[i]),(Lon[j]-X_new[i]))
                #print(Lat_deg[j], Lon_deg[j], lat_deg, lon_deg)
                DST = self.GeodesicDistance(Lat_deg[j], Lon_deg[j], lat_deg, lon_deg)
                LAT_DEG.append(lat_deg)
                LON_DEG.append(lon_deg)
                DIST.append(DST)
                            
            if j % 100 == 10000:
                self.p.circle(Lat[j], Lon[j], color = 'yellow', alpha = 1, size = 3)
                #self.p.ellipse(Lat[j],Lon[j], alpha = 0.3, width=width, height=width, color="white")
                self.p.patch(Lat[j]*np.ones(len(Y))+Y_new, Lon[j]*np.ones(len(X))-X_new, alpha = 0.3, color="white")
                if False:
                    self.SaveMap(Lon, Lat, j, Lat[j], Lon[j], Lat[j]*np.ones(len(Y))+Y_new, Lon[j]*np.ones(len(X))-X_new )
        plt.show()
            
        # Here, find the closest contingency UAM aerodrome from a vehicle's current position
        Distance2ClosestContingencySite = []
        Labeling = []
        Direction = [] # finds the direction of the closest contingency landing site relative to Northward reference
        
        for j in range(len(Lat)): # j represents the each step of the vehicle along the path
            Distance2ContingencySite_Regional_Airport = [] # array containing distance from current position to the regional airports
            Distance2ContingencySite_Major_Airport = [] # array containing distance from current position to the major airports
            Distance2ContingencySite_Heliport = [] # array containing distance from current position to the heliports

            for k in range(len(self.lat_regional_deg)): # k represents each location index of regional airport
                Distance2ContingencySite_Regional_Airport.append(self.GeodesicDistance(Lat_deg[j], Lon_deg[j], self.lat_regional_deg[k], self.lon_regional_deg[k])) # in miles
            
            for l in range(len(self.lat_heliports_deg)): # l represents each location index of heliports
                Distance2ContingencySite_Heliport.append(self.GeodesicDistance(Lat_deg[j], Lon_deg[j], self.lat_heliports_deg[l], self.lon_heliports_deg[l])) # in miles
            
            for m in range(len(self.lat_major_deg)): # m represents each location index of major airport
                Distance2ContingencySite_Major_Airport.append(self.GeodesicDistance(Lat_deg[j], Lon_deg[j], self.lat_major_deg[m], self.lon_major_deg[m])) # in miles    
            
            # find the closest of [regional, heliport, major] to the current location
            minOfAll = [min(Distance2ContingencySite_Regional_Airport), min(Distance2ContingencySite_Heliport), min(Distance2ContingencySite_Major_Airport)]
            
            Distance2ClosestContingencySite.append(min(minOfAll)) # find the closest one at the current location
            indexMin = minOfAll.index(min(minOfAll)) # find the index: 0 - regional, 1 - heliport, 2 - major airport
            Labeling.append(int(indexMin)) 
            
            # find the direction of the closest contingency landing site relative to North Pole reference
            if int(indexMin) == 0: # if regional airport
                idx = Distance2ContingencySite_Regional_Airport.index(min(minOfAll))
                deltaLat = self.lat_regional_deg[idx] - Lat_deg[j]
                deltaLon = self.lon_regional_deg[idx] - Lon_deg[j]
                
            elif int(indexMin) == 1: # if heliport
                idx = Distance2ContingencySite_Heliport.index(min(minOfAll))
                deltaLat = self.lat_heliports_deg[idx] - Lat_deg[j]
                deltaLon = self.lon_heliports_deg[idx] - Lon_deg[j]
                
            elif int(indexMin) == 2: # if major airport
                idx = Distance2ContingencySite_Major_Airport.index(min(minOfAll))
                deltaLat = self.lat_major_deg[idx] - Lat_deg[j]
                deltaLon = self.lon_major_deg[idx] - Lon_deg[j]
            
            if deltaLon >= 0 and deltaLat >= 0: # the first quadrant
                if deltaLon == 0 and deltaLat == 0:
                    directionAngle_rad = 0
                    directionAngle_deg = 0
                    Direction.append(directionAngle_deg)
                else:
                    directionAngle_rad = math.atan(deltaLon/deltaLat)
                    directionAngle_deg = directionAngle_rad * 180 / math.pi
                    Direction.append(directionAngle_deg)
            elif deltaLon < 0 and deltaLat >= 0: # the second quadrant
                directionAngle_rad = 2 * math.pi + math.atan(deltaLon/deltaLat)
                directionAngle_deg = directionAngle_rad * 180 / math.pi
                Direction.append(directionAngle_deg)
            elif deltaLon > 0 and deltaLat < 0: # the fourth quadrant
                directionAngle_rad = math.pi + math.atan(deltaLon/deltaLat)
                directionAngle_deg = directionAngle_rad * 180 / math.pi
                Direction.append(directionAngle_deg)
            elif deltaLon < 0 and deltaLat < 0: # the third quadrant
                directionAngle_rad = math.atan(deltaLon/deltaLat) + math.pi
                directionAngle_deg = directionAngle_rad * 180 / math.pi
                Direction.append(directionAngle_deg)
            elif deltaLon == 0 and deltaLat > 0:
                directionAngle_rad = math.pi / 2
                directionAngle_deg = directionAngle_rad * 180 / math.pi
                Direction.append(directionAngle_deg)
            elif deltaLon == 0 and deltaLat < 0:
                directionAngle_rad = 2 * math.pi - (math.pi / 2)
                directionAngle_deg = directionAngle_rad * 180 / math.pi
                Direction.append(directionAngle_deg)
                
        #print(f'Distance to the closest contingency site is (in miles): {Distance2ClosestContingencySite}')
        #print(Labeling)
        
        # Check if any of the closest contingency landing locations along the route fall within the reachable footprint
        counter = 0 # count how many times the aircraft reachable footprint is outside the contingency landing sites
        for i in range(sampSize): # i represents each step along the route
            distShape = []
            footprintRadial = []
            for k in range(len(X)): # k represents each point in reachable footprint
                lat_deg, lon_deg = self.Mercator2Degrees((Lat[i]+Y_new[k]),(Lon[i]-X_new[k]))
                distS = self.GeodesicDistance(Lat_deg[i], Lon_deg[i], lat_deg, lon_deg) 
                distShape.append(distS)
                
                if (lon_deg - Lon_deg[i]) >= 0 and (lat_deg - Lat_deg[i]) >= 0:
                    footprintradial = math.atan((lon_deg - Lon_deg[i])/(lat_deg - Lat_deg[i]))
                elif (lon_deg - Lon_deg[i]) > 0 and (lat_deg - Lat_deg[i]) < 0:
                    footprintradial = math.pi + math.atan((lon_deg - Lon_deg[i])/(lat_deg - Lat_deg[i]))
                elif (lon_deg - Lon_deg[i]) < 0 and (lat_deg - Lat_deg[i]) < 0:
                    footprintradial = math.pi + math.atan((lon_deg - Lon_deg[i])/(lat_deg - Lat_deg[i]))
                elif (lon_deg - Lon_deg[i]) < 0 and (lat_deg - Lat_deg[i]) > 0:
                    footprintradial = 2 * math.pi + math.atan((lon_deg - Lon_deg[i])/(lat_deg - Lat_deg[i]))
                
                footprintRadial.append(footprintradial)
            
            n = Direction[i]
            # find out which angle in the footprint the direction of contingency landing site closely matches
            footprintRadial = np.multiply(180 / math.pi, footprintRadial) # convert radians to degrees
            # subtract n degree from footprintRadial and find the minimum value and index
            subtraction1 = np.subtract(footprintRadial,n)
            # find the minimum of the subtraction and its index
            IndxMin = np.where(subtraction1 == min(subtraction1))
            IndxMin = int(IndxMin[0])
            # use the index value to find the angle in footprintRadial that is closest to it
            ClosestFootPrintRadial = footprintRadial[IndxMin]
            # also find the distance of that from distShape
            distanceOfClosestFootprintRadial = distShape[IndxMin]
            # compare this distance to the landing site distance
            # if this distance is less than landing site distance, increase counter by 1
            # meaning landing site is outside the reachable footprint
            #print(Distance2ClosestContingencySite[i], distS)
            if Distance2ClosestContingencySite[i] >= distanceOfClosestFootprintRadial:
                if Labeling[i] == 0 or Labeling[i] == 2:
                    counter += 1
               
                
        # print(counter)           
        print(f'Percentage of trip that is outside the distance requirement: {100*counter/sampSize} %')
        self.CLAP = 100*counter/sampSize
        
        fig, (ax1, ax2, ax3) = plt.subplots(3,1)
        fig.set_size_inches(8, 16)
        ax1.plot(DistanceLinspace, Distance2ClosestContingencySite, label="Flight Path")
        #plt.plot(DistanceLinspace, [glideDistance]*sampSize, 'r--', label="Threshold Line")
        ax1.set_xlabel("Trip Length Completed [miles]")
        ax1.set_ylabel("Closest Contingency Landing Site Distance [miles]")
        ax1.grid()

        #plt.figure(figsize=(8,5))
        ax2.plot(DistanceLinspace, Labeling, 'r-', label="Threshold Line")
        ax2.set_xlabel("Trip Length Completed [miles]")
        ax2.set_label("Closest Contingency Landing Site Distance [miles]")
        ax2.set_yticks([0,1,2])
        ax2.set_yticklabels(['Regional', 'Heliport', 'Major'])
        ax2.grid()

        
        #plt.figure(figsize=(8,5)) [0:sampSize-2]
        ax3.plot(DistanceLinspace, Direction, 'r-', label="Threshold Line")
        ax3.set_xlabel("Trip Length Completed [miles]")
        ax3.set_ylabel("Heading Direction [degrees]")
        ax3.set_title("Direction of Contingency Landing Site Rel. To North")
        ax3.grid()

        plt.savefig('C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/HeadingDirectionVsTripLength.png', dpi=300)
        return (Distance2ClosestContingencySite, Direction, Labeling)
    
    def WaypointsConnector(self,LatLonFrom_merc, LatLonTo_merc, sampSize):
        # EXTRACT COORDINATES FROM THE TUPLES
        LatFrom_inMerc = LatLonFrom_merc[0] # latitude
        LonFrom_inMerc = LatLonFrom_merc[1] # longitude
        LatTo_inMerc = LatLonTo_merc[0] # latitude
        LonTo_inMerc = LatLonTo_merc[1] # longitude
        
        # FIND THE SLOPE OF THE WAYPOINT WITH LONGITUDE BEING X-AXIS, LATITUDE BEING Y-AXIS
        delLat = LatTo_inMerc - LatFrom_inMerc
        delLon = LonTo_inMerc - LonFrom_inMerc
        Slope = (delLat)/(delLon)

        # USE THE FIRST-ORDER LINEAR EQUATIONS TO DEFINE A LINE (simple algebra)
        #   if LonFrom_inMerc < LonTo_inMerc, linspace executes properly
        #   if LonFrom_inMerc > LonTo_inMerc, linspace fails
        #       to fix this issue, introduce an if-else statement
        if LonFrom_inMerc < LonTo_inMerc:
            LonArray_inMerc = np.linspace(LonFrom_inMerc, LonTo_inMerc, sampSize)
        elif LonFrom_inMerc > LonTo_inMerc:
            LonArray_inMerc = np.linspace(LonTo_inMerc, LonFrom_inMerc, sampSize)
        LatArray_inMerc = Slope * (LonArray_inMerc - LonFrom_inMerc) + LatFrom_inMerc
        
        # FIND THE HEADING DIRECTION IN DEGREES
        TripHeading = self.EstimateTripHeading(delLat, delLon)
        
        return LatArray_inMerc, LonArray_inMerc, TripHeading
   
    def EstimateTripHeading(self, delLat, delLon):     
        # FIND THE HEADING DIRECTION
        #   0 deg - North
        #   90 deg - East
        #   180 deg - South
        #   270 deg - West
        
        if delLat >= 0 and delLon >= 0:
            TripHeading = math.atan((delLon/delLat)) * 180/math.pi
        elif delLat <= 0 and delLon >= 0:
            TripHeading = 180 + math.atan((delLon/delLat)) * 180/math.pi
        elif delLat <= 0 and delLon <= 0:
            TripHeading = 180 + math.atan((delLon/delLat)) * 180/math.pi
        elif delLat >= 0 and delLon <= 0:
            TripHeading = 360 + math.atan((delLon/delLat)) * 180/math.pi
        return TripHeading
    
    def ShowMap(self): 
        output_notebook()
        show(self.p)
        output_file("test.html")
        save(self.p)
        plt.show()
    
        
    def SaveMap(self, Lon, Lat, imgNum, Latj, Lonj, PatchLatj, PatchLonj):
        # output_notebook()
        q = self.MapperInfrastructure()
        q.line(Lat, Lon, color = 'white', line_width = 2)
        q.circle(Latj, Lonj, color = 'yellow', alpha = 1, size = 3)
        q.patch(PatchLatj, PatchLonj, alpha = 0.3, color="white")
        number_str = str(imgNum)
        # output_file("C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/TripAnimation/test" + number_str.zfill(4) + ".png")
        filename="C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/TripAnimation/test" + number_str.zfill(4) + ".png"
        export_png(q, filename=filename )

    
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

    def PlotContingencyLandingAssurance_vs_CruiseAltitude(self, altitude, CLAP):
        fig, ax = plt.subplots()
        ax.plot(altitude, CLAP)
        ax.set_xlabel('Altitude (ft.)')
        ax.set_ylabel('Contingency Landing Assurance Percentage (%)')
        ax.set_title('Contingency Landing Assurance Pecentage vs. Altitude')
        plt.savefig('C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/CLAPvsAlt.png', dpi=300)
        plt.show()

     
    def __call__(self):
        print(f'Geodesic Trip Distance: {self.geodesicDistance} miles')
        
        

