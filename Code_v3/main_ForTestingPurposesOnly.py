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


def PlotMultipleTrips(TripInfo, ac, cruiseAltitudeInFeet, Show = True, Save = False, PlotGraphs = False):
    Chicago = TripMapper("Chicago","Map", PlotGraphs) # options for 2nd input either "Satellite" or "Map"
    arr = TripInfo[3] #, 9, 13, 19]
    dep = TripInfo[1]#, 6, 7, 8, 11]
    arrType = TripInfo[2]
    depType = TripInfo[0]
    print(arr, dep, arrType, depType)
    
    """
    DEFINE WAYPOINTS HERE, MANUALLY, FOR NOW
    """
    lonWP_inDeg = []
    latWP_inDeg = []
    # TripD = Chicago.TripDistance(depType,arrType,dep,arr)  # in miles      
    WayPoints = [lonWP_inDeg, latWP_inDeg]
    FP1, Heading, TripDistanceNonDirectRoute, distance, direction, aerodromeType = Chicago.DrawNonDirectRoutingTrip(depType, arrType, dep,arr, ac, cruiseAltitudeInFeet, WayPoints, Save=Save)
    
    ## ENABLE THIS WHEN PLOTTING POLAR PLOTS:
    # PlotPolar(ac, FP1, cruiseAltitudeInFeet, Heading, TripDistanceNonDirectRoute, distance, direction, aerodromeType)

    if Show == True:
        Chicago.ShowMap()
    return (Chicago.CLAP, Chicago.flightTime, Chicago.energyConsumed, Chicago.FLT_ref, Chicago.EC_ref)

def PlotCLAP(TripInfo, ac):
    altitude = np.linspace(1500,15000,60) # desired cruising altitude(s) in feet - it is in an array to be able to plot CLAP vs cruising altitudes
    CLAP = []
    
    for h in altitude:
        clap, fltTime, eneConsumed, fltTime_ref, eneConsumed_ref = PlotMultipleTrips(TripInfo, ac, h, False)
        CLAP.append(100-clap)
    
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(altitude, CLAP,linewidth='3')
    ax.set_xlabel('Cruise Altitude (ft.)')
    ax.set_ylabel('Contingency Landing Assurance Percentage (%)')
    ax.set_title('Contingency Landing Assurance Pecentage vs. Cruise Altitude Floor')
    ax.set_yticks([0,10,20,30,40,50,60,70,80,90,100])
    ax.set_xticks(np.arange(1500,7500,500))
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.25', color='black')
    ax.grid(which='minor', linestyle=':', linewidth='0.25', color='black')
    # plt.grid()
    # plt.savefig('C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/CLAPvsAltRevised.png', dpi=500)
    plt.show()
    
    return (altitude, CLAP)
# PlotMultipleTrips()

# PLOT IN POLAR COORDINATES
def PlotPolar(Joby, FP1, cruiseAltitudeInFeet, Heading, TripD, distance, direction, aerodromeType):
    """
    COMPASS PLOT GENERATION (I.E., POLAR PLOT)
    """
    # https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/
    # https://www.kite.com/python/answers/how-to-add-leading-zeros-to-a-number-in-python
    # https://matplotlib.org/stable/api/projections_api.html
    # https://stackoverflow.com/questions/16085397/changing-labels-in-matplotlib-polar-plot
    TripDistanceArray = np.linspace(0,TripD,len(distance)-1) # an array of the trip route in miles
    for t in range(len(distance)-1): 
        # fig, ax = PlotInPolarCoordinates(distance[t:t+1], direction[t:t+1], teta, r)
        TripHeading = Heading[t] * math.pi/180

        # Account for takeoff, climb, descend, land changes in altitude footprint
        if TripDistanceArray[t] <= (0.621371*FP1.dx/1000) or TripDistanceArray[t] >= TripD - (0.621371*(FP1.dx)/1000):
            x_altitude, z = FP1.GivenRangeOutputAltitude(TripDistanceArray[t]) # z is in meters
            z = z * 3.28084 # in ft
            dist_speed, V = FP1.GivenRangeOutputSpeed(TripDistanceArray[t])
            X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(z, V, 45,0)
            FootprintDistance = FootprintDistance * 0.621371 # km to miles
            altitude_ft = z
        else:
            altitude_ft = cruiseAltitudeInFeet
            dist_speed, V = FP1.GivenRangeOutputSpeed(TripDistanceArray[t])
            X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(cruiseAltitudeInFeet, V, 45,0)
            FootprintDistance = FootprintDistance * 0.621371 # km to miles
        
        # Rotate the footprint to match the heading direction
        Radial_Rotated = Radial + (np.ones(len(Radial))*TripHeading)
        fig, ax = PlotInPolarCoordinates(distance[t:t+1], direction[t:t+1])
        ax.plot(Radial_Rotated,FootprintDistance)
        
        if aerodromeType[t] == 0: # if regional airport
            colorTarget = 'ws'
            label = "Regional Airport"
        elif aerodromeType[t] == 1: # if heliport
            colorTarget = 'yo'
            label = "Heliport"
        elif aerodromeType[t] == 2:
            colorTarget = 'r^'
            label = "Major Airport"
        
        ax.plot(direction[t]*math.pi/180, distance[t],colorTarget,markeredgecolor='black',label=label)
        
        ax.set_theta_direction(-1) # CW direction 
        #ax.set_theta_zero_location('N')
        ax.set_theta_offset(math.pi/2)
        # ax.set_theta_offset(math.pi/2 + Heading[t]*math.pi/180)
        ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
        ax.set_title("Reachable Ground Footprint (miles) \n of Joby eVTOL Vehicle under Gliding Conditions\n Altitude (ft): " + str(round(altitude_ft,0)) + " || Trip Completion Percentage: " + str(round(100*TripDistanceArray[t]/TripD,0)) +" %" )
        ax.legend(loc='lower right',bbox_to_anchor=(1, 0))
        plt.tight_layout()
        number_str = str(t)
        plt.savefig('C:/Users/saimu/Documents/AAE_MS_Thesis_Documentation_v2/Python_Code/Results/Compass_Map/step' + number_str.zfill(4) + '.png', dpi=300)