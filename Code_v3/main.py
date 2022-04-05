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
   
    # Specify trip aerodrome departure and arrival 
    #for dep in range(1,3):
    #    for arr in range(4,9):
    #        Chicago.DrawGeodesicTrip(dep,arr, X[0], Y[0])
    altitude = np.linspace(3500,5000,1)
    CLAP = []

    Joby = Aircraft("Joby", 4, 200, 150, 13.8, 45, 2177, 200, S=10.7*1.7)
    Joby.Characteristics()

    for h in altitude:
        
        # TripD = Chicago.TripDistance(1,8)        
        # FP1 = FlightProfile(h, TripDistance)
        # FP1.PlotMissionProfile()
        # # FP1_time = FP1.FlightTime()
        # for l in np.linspace(0,TripD,100)
        # dx, dh = FP1.GivenRangeOutputAltitude()
        
        
        
        
        X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(h,45,0)
        FootprintDistance = FootprintDistance * 0.621371 # km to miles
        distance, direction, aerodromeType = Chicago.DrawGeodesicTrip(7,8, X, Y)
        
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
                fig, ax = PlotInPolarCoordinates(distance[t:t+1], direction[t:t+1], teta, r)
                
                # Rotate the footprint to match the heading direction
                Radial_Rotated = Radial + (np.ones(len(Radial))*TripHeading)
                ax.plot(Radial_Rotated,FootprintDistance)
            
                if aerodromeType[t] == 0: # if regional airport
                    colorTarget = 'ro'
                elif aerodromeType[t] == 1: # if heliport
                    colorTarget = 'yo'
                elif aerodromeType[t] == 2:
                    colorTarget = 'bo'
                
                ax.plot(direction[t]*math.pi/180, distance[t],colorTarget)
                
                ax.set_theta_direction(-1) # CW direction 
                #ax.set_theta_zero_location('N')
                ax.set_theta_offset((math.pi)-((Chicago.triphead)*math.pi/180))
                ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
                number_str = str(t)
                plt.savefig('C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/Compass/step' + number_str.zfill(4) + '.png', dpi=300)
        
        
        CLAP.append(100-Chicago.CLAP)
    Chicago.ShowMap()
    Chicago.PlotContingencyLandingAssurance_vs_CruiseAltitude(altitude, CLAP)
    
    return None
    # return (Radial, FootprintDistance, distance, direction, aerodromeType, Chicago.triphead)