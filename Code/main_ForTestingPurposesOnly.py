# -*- coding: utf-8 -*-
"""
Author: Sai V. Mudumba
Code Conceived: March, 2021
Code Last Modified: May 15, 2021
"""
from TripMapper import *
from LoadExistingUAMaerodromeInfrastructure import *
from Aircraft import *
from PlotInPolarCoordinates import *

import numpy as np

def main():
    # This is the main code that creates instances
    Chicago = TripMapper("Chicago","Satellite") # options for 2nd input either "Satellite" or "Map"
    DEP = [7, 9, 13, 19] # indices for departure aerodromes
    ARR = [5, 6, 7, 8, 11] # indices for arrival aerodromes
    idxDep = DEP[0]
    idxArr = ARR[3]
    # Specify trip aerodrome departure and arrival 
    #for dep in range(1,3):
    #    for arr in range(4,9):
    #        Chicago.DrawGeodesicTrip(dep,arr, X[0], Y[0])
    altitude = np.linspace(3750,5000,1) # in ft.
    CLAP = []

    Joby = Aircraft("Joby", 4, 200, 150, 13.8, 45, 2177, 200, S=10.7*1.7)
    Joby.Characteristics()

    for h in altitude:
        fig, ax = plt.subplots(figsize = (8, 5),dpi=300)
        TripD = Chicago.TripDistance(idxDep,idxArr)  # in miles      
        FP1 = FlightProfile(Joby, h, TripD)
        FP1.PlotMissionProfile(fig, ax, "red","Cruise Altitude Floor: ")
        # # FP1_time = FP1.FlightTime()
        # dx, dh = FP1.GivenRangeOutputAltitude()
        
        
        
        
        X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(h,45,0)
        FootprintDistance = FootprintDistance * 0.621371 # km to miles
        distance, direction, aerodromeType = Chicago.DrawGeodesicTrip(idxDep,idxArr, X, Y)
        
        TripDistanceArray = np.linspace(0,TripD,len(distance)-1)# in miles

        if len(altitude) == 1:
            """
            COMPASS PLOT GENERATION (I.E., POLAR PLOT)
            """
            # https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/
            # https://www.kite.com/python/answers/how-to-add-leading-zeros-to-a-number-in-python
            # https://matplotlib.org/stable/api/projections_api.html
            # https://stackoverflow.com/questions/16085397/changing-labels-in-matplotlib-polar-plot
            teta = np.linspace(0,2*math.pi,100)
            r = 12.6
            
            TripHeading = math.pi/2 - Chicago.triphead * math.pi/180
            for t in range(len(distance)-1): 
                # fig, ax = PlotInPolarCoordinates(distance[t:t+1], direction[t:t+1], teta, r)
                
                # Account for takeoff, climb, descend, land changes in altitude footprint
                if TripDistanceArray[t] <= (0.621371*FP1.dx/1000) or TripDistanceArray[t] >= TripD - (0.621371*(FP1.dx)/1000):
                    x_altitude, z = FP1.GivenRangeOutputAltitude(TripDistanceArray[t]) # z is in meters
                    z = z * 3.28084 # in ft
                    X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(z,45,0)
                    FootprintDistance = FootprintDistance * 0.621371 # km to miles
                    # print(0.621371*x_altitude/1000, z, TripDistanceArray[t],0.621371*FP1.dx/1000, TripD - (0.621371*(FP1.dx)/1000))
                    altitude_ft = z
                    # print(TripDistanceArray[t],0.621371*FP1.dx/1000, FP1.dx )
                else:
                    altitude_ft = h
                    X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(h,45,0)
                    FootprintDistance = FootprintDistance * 0.621371 # km to miles
                    # print(0.621371*x_altitude/1000, z, TripDistanceArray[t],0.621371*FP1.dx/1000, TripD - (0.621371*(FP1.dx)/1000))
                # Rotate the footprint to match the heading direction
                
                Radial_Rotated = Radial + (np.ones(len(Radial))*TripHeading)
                fig, ax = PlotInPolarCoordinates(distance[t:t+1], direction[t:t+1], teta, r)
                ax.plot(Radial_Rotated,FootprintDistance)
               
                    
            
                if aerodromeType[t] == 0: # if regional airport
                    colorTarget = 'ro'
                    label = "Regional Airport"
                elif aerodromeType[t] == 1: # if heliport
                    colorTarget = 'yo'
                    label = "Heliport"
                elif aerodromeType[t] == 2:
                    colorTarget = 'bo'
                    label = "Major Airport"
                
                ax.plot(direction[t]*math.pi/180, distance[t],colorTarget,label=label)
                
                ax.set_theta_direction(-1) # CW direction 
                #ax.set_theta_zero_location('N')
                ax.set_theta_offset((math.pi)-((Chicago.triphead)*math.pi/180))
                ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
                ax.set_title("Reachable Ground Footprint (miles) \n of Joby-like S4 eVTOL Vehicles under Gliding Conditions\n Altitude (ft): " + str(round(altitude_ft,0)) + " Trip Completion Percentage: " + str(round(100*TripDistanceArray[t]/TripD,0)) +" %" )
                ax.legend(loc='lower right',bbox_to_anchor=(1, 0))
                plt.tight_layout()
                number_str = str(t)
                plt.savefig('C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/Compass/step' + number_str.zfill(4) + '.png', dpi=300)
        
        
        CLAP.append(100-Chicago.CLAP)
    Chicago.ShowMap()
    Chicago.PlotContingencyLandingAssurance_vs_CruiseAltitude(altitude, CLAP)
    
    return None
    # return (Radial, FootprintDistance, distance, direction, aerodromeType, Chicago.triphead)

def PlotMultipleTrips():
    Chicago = TripMapper("Chicago","Satellite") # options for 2nd input either "Satellite" or "Map"
    Joby = Aircraft("Joby", 4, 200, 150, 13.8, 45, 2177, 200, S=10.7*1.7)
    X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(1500,45,0)
    # Specify trip aerodrome departure and arrival 
    DEP = [7] #, 9, 13, 19]
    ARR = [5, 6, 7, 8, 11]
    for dep in DEP:
        for arr in ARR:
            Chicago.DrawGeodesicTrip(dep,arr, X, Y)
    Chicago.ShowMap()

# PlotMultipleTrips()