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
from bokeh.plotting import figure, show, output_notebook, output_file, save
from bokeh.tile_providers import CARTODBPOSITRON, ESRI_IMAGERY, OSM, STAMEN_TERRAIN, STAMEN_TERRAIN_RETINA
from bokeh.tile_providers import get_provider, Vendors 
from bokeh.io import export_png

import matplotlib.pyplot as plt
from LoadExistingUAMaerodromeInfrastructure import *
from FlightProfile import *

class TripMapper(LoadExistingUAMaerodromeInfrastructure):
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
    
    def TripDistance(self, idxDep, idxArr):
        latDep_deg = self.lat_regional_deg[idxDep]
        lonDep_deg = self.lon_regional_deg[idxDep]
        latArr_deg = self.lat_heliports_deg[idxArr]
        lonArr_deg = self.lon_heliports_deg[idxArr]
        geodesicDistance = self.GeodesicDistance(self.lat_regional_deg[idxDep], self.lon_regional_deg[idxDep], self.lat_heliports_deg[idxArr], self.lon_heliports_deg[idxArr])
        tripDistance = geodesicDistance
        return tripDistance
        
    def DrawGeodesicTrip(self, idxDep, idxArr, X, Y):
        sampSize = 500
        self.sampleSize = sampSize
        latDep_deg = self.lat_regional_deg[idxDep]
        lonDep_deg = self.lon_regional_deg[idxDep]
        latArr_deg = self.lat_heliports_deg[idxArr]
        lonArr_deg = self.lon_heliports_deg[idxArr]
        
        geodesicDistance = self.GeodesicDistance(self.lat_regional_deg[idxDep], self.lon_regional_deg[idxDep], self.lat_heliports_deg[idxArr], self.lon_heliports_deg[idxArr])
        self.tripDistance = geodesicDistance
        print(f'Geodesic Trip Distance between {idxDep} - {idxArr}: {geodesicDistance} miles')
        
        latDep_merc = self.lat_regional_merc[idxDep]
        lonDep_merc = self.lon_regional_merc[idxDep]
        latArr_merc = self.lat_heliports_merc[idxArr]
        lonArr_merc = self.lon_heliports_merc[idxArr]
        
        # Find the slope of the trip, with longitudinal axis being the x-axis and latitude axis being the y-axis
        delta = (self.lat_heliports_merc[idxArr]-self.lat_regional_merc[idxDep])/(self.lon_heliports_merc[idxArr]-self.lon_regional_merc[idxDep])
        
        # Find the angle of the slope relative to the North
        TripHeading = math.atan(1/delta) * 180/math.pi
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
        
        # Use the linear function equation to define the time steps, in mercator coordinates
        Lon = np.linspace(self.lon_regional_merc[idxDep], self.lon_heliports_merc[idxArr], sampSize) 
        Lat = (delta * (Lon - self.lon_regional_merc[idxDep]) + self.lat_regional_merc[idxDep])
        self.p.line(Lat, Lon, color = 'white', line_width = 2)
        
        # same thing as above, but this is in degrees
        delta_deg = (self.lat_heliports_deg[idxArr]-self.lat_regional_deg[idxDep])/(self.lon_heliports_deg[idxArr]-self.lon_regional_deg[idxDep])
        Lon_deg = np.linspace(self.lon_regional_deg[idxDep], self.lon_heliports_deg[idxArr], sampSize) 
        Lat_deg = (delta_deg * (Lon_deg - self.lon_regional_deg[idxDep]) + self.lat_regional_deg[idxDep])
        
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

    def SimplifiedReachabilityFootprint(self, altitude):
        # altitide will be in feet
        altitude = altitude * 0.3048
        LDratio = 13.8
        GlideRange = altitude * LDratio
        print(f'The simplified Glide Radius is {GlideRange} meters')
        
        teta = np.linspace(0,2*math.pi,100)
        X = []
        Y = []
        
        for i, t in enumerate(teta):
          X.append(GlideRange * math.cos(t) * 5000/3730) # multiply by 5000/3730 to project it to mercator meters
          Y.append(GlideRange * math.sin(t) * 5000/3730) # multiply by 5000/3730 to project it to mercator meters
        
        return (X, Y)

    def PlotContingencyLandingAssurance_vs_CruiseAltitude(self, altitude, CLAP):
        fig, ax = plt.subplots()
        ax.plot(altitude, CLAP)
        ax.set_xlabel('Altitude (ft.)')
        ax.set_ylabel('Contingency Landing Assurance Percentage (%)')
        ax.set_title('Contingency Landing Assurance Pecentage vs. Altitude')
        plt.savefig('C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/CLAPvsAlt.png', dpi=300)
        plt.show()
        
        
    
    def ReachableCircle(self, idxDep, idxArr, desired_distance):
        error = 10
        step = 0.01
        Lat1 = self.lat_regional_deg[idxDep]
        Lat2 = Lat1
        Lon1 = self.lon_regional_deg[idxDep]
        Lon2 = Lon1
        while abs(error) > 1:
            dist_mi = self.GeodesicDistance(Lat1,Lon1,Lat2,Lon2)
            error = abs(dist_mi - desired_distance)
            Lon2 += step
        x, y = LoadExistingUAMaerodromeInfrastructure.Degrees2Mercator(self,(Lat2, Lon2))
        u,v = LoadExistingUAMaerodromeInfrastructure.Degrees2Mercator(self,(Lat1, Lon1))
        width = x-u
        return width
     
    def __call__(self):
        print(f'Geodesic Trip Distance: {self.geodesicDistance} miles')
        
        

