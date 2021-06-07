# -*- coding: utf-8 -*-
"""
Author: Sai V. Mudumba
Code Conceived: March, 2021
Code Last Modified: June 2, 2021
"""

# LOAD THE FOLLOWING INTO THIS SCRIPT
from TripMapper import *
from LoadExistingUAMaerodromeInfrastructure import *
from Aircraft import *
from PlotInPolarCoordinates import *
import numpy as np

def main():
    # This is the main code that creates instances of trips
    Chicago = TripMapper("Chicago","Satellite") # option for 2nd input is either "Satellite" or "Map"
    
    DEP = [7, 9, 13, 19] # indices for departure aerodromes
    ARR = [5, 6, 7, 8, 11] # indices for arrival aerodromes
    
    DepAerodromeType = "Regional"
    ArrAerodromeType = "Regional"
    
    idxDep = DEP[0] # indicate the departure aerodrome
    idxArr = DEP[1] # indicate the arrival aerodrome
    
    
    altitude = np.linspace(3750,5000,1) # desired cruising altitude(s) in feet - it is in an array to be able to plot CLAP vs cruising altitudes
    CLAP = [] # Contingency Landing Assurance Percentage (%) empty list defined

    Joby = Aircraft("Joby", 4, 200, 150, 13.8, 45, 2177, 200, S=10.7*1.7) # define the aircraft
    Joby.Characteristics() # print out the aircraft characteristics

    # Iterate through each cruising altitude values in the array
    for h in altitude:
        fig, ax = plt.subplots(figsize = (8, 5),dpi=300)
        TripD = Chicago.TripDistance(DepAerodromeType,ArrAerodromeType,idxDep,idxArr)  # in miles      
        FP1 = FlightProfile(Joby, h, TripD)
        FP1.PlotMissionProfile(fig, ax, "red","Cruise Altitude Floor: ")
        # # FP1_time = FP1.FlightTime()
        # dx, dh = FP1.GivenRangeOutputAltitude()
        
        # determine the reachable ground footprint for the aircraft defined
        # the inputs are altitude, bank angle (but it doesn't play a role in the code), power failure level (doesn't play a role in the code yet)
        # the outputs are X, Y of the footprint, also equivalent Radial and Distance for polar plots
        X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(h,45,0)
        FootprintDistance = FootprintDistance * 0.621371 # km to miles
        
        # Draw the geodesic trip on a map with the following information:
        # (a) all existing infrastructures, 
        # (b) departure aerodrome and arrival aerodrome 
        # (c) the route path (i.e., geodesic or non-direct routing)
        # (d) the footprint along the route
        # Output(s): distance, its direction, and aerodrome type to any contingency landing site along the route
        distance, direction, aerodromeType = Chicago.DrawGeodesicTrip(DepAerodromeType,ArrAerodromeType,idxDep,idxArr, X, Y)
        
        
        TripDistanceArray = np.linspace(0,TripD,len(distance)-1) # an array of the trip route in miles
        
        if len(altitude) == 1: # this condition only exists because I don't want to run this for all indices in the altitude array
            """
            COMPASS PLOT GENERATION (I.E., POLAR PLOT)
            """
            # https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/
            # https://www.kite.com/python/answers/how-to-add-leading-zeros-to-a-number-in-python
            # https://matplotlib.org/stable/api/projections_api.html
            # https://stackoverflow.com/questions/16085397/changing-labels-in-matplotlib-polar-plot
            
            TripHeading = math.pi/2 - Chicago.triphead * math.pi/180
            for t in range(len(distance)-1): 
                # fig, ax = PlotInPolarCoordinates(distance[t:t+1], direction[t:t+1], teta, r)
                
                # Account for takeoff, climb, descend, land changes in altitude footprint
                if TripDistanceArray[t] <= (0.621371*FP1.dx/1000) or TripDistanceArray[t] >= TripD - (0.621371*(FP1.dx)/1000):
                    x_altitude, z = FP1.GivenRangeOutputAltitude(TripDistanceArray[t]) # z is in meters
                    z = z * 3.28084 # in ft
                    X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(z,45,0)
                    FootprintDistance = FootprintDistance * 0.621371 # km to miles
                    altitude_ft = z
                else:
                    altitude_ft = h
                    X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(h,45,0)
                    FootprintDistance = FootprintDistance * 0.621371 # km to miles
                
                # Rotate the footprint to match the heading direction
                Radial_Rotated = Radial + (np.ones(len(Radial))*TripHeading)
                fig, ax = PlotInPolarCoordinates(distance[t:t+1], direction[t:t+1])
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
    X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(1000,45,0)
    # Specify trip aerodrome departure and arrival 
    DEP = [7] #, 9, 13, 19]
    ARR = [13]#, 6, 7, 8, 11]
    depType = "Regional"
    arrType = "Regional"
    for dep in DEP:
        for arr in ARR:
            # Chicago.DrawGeodesicTrip(depType, arrType, dep,arr, X, Y)
            Chicago.DrawNonDirectRoutingTrip(depType, arrType, dep,arr, Joby, 1000)
    Chicago.ShowMap()

# PlotMultipleTrips()