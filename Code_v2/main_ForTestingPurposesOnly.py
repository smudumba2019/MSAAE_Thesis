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


def PlotMultipleTrips(ac, cruiseAltitudeInFeet, Show = True, Save = False):
    Chicago = TripMapper("Chicago","Satellite") # options for 2nd input either "Satellite" or "Map"
    # Joby = Aircraft("Joby", 4, 200, 150, 13.8, 45, 2177, 200, S=10.7*1.7)
    X, Y, Radial, FootprintDistance = ac.ReachableGroundFootprint(cruiseAltitudeInFeet,45,0)
    # Specify trip aerodrome departure and arrival 
    dep = 7 #, 9, 13, 19]
    arr = 8#, 6, 7, 8, 11]
    depType = "Regional"
    arrType = "Heliport"
    
    # FOR PLOTTING MULTIPLE TRIPS
    DEP = [7, 9, 13, 9]
    ARR = [8, 6, 7, 11]
    
    """
    DEFINE WAYPOINTS HERE, MANUALLY, FOR NOW
    """
    # lonWP_inDeg = [-88.02517, -87.81231]#[-88.10121, -87.9838, -87.89202] #(lonDep_deg + lonArr_deg) / 2
    # latWP_inDeg = [41.93893, 41.91313]#[41.96701,41.9642, 41.91506] #(latDep_deg + latArr_deg) / 2
    # lonWP_inDeg = [-88.10121, -87.9838, -87.89202] #(lonDep_deg + lonArr_deg) / 2
    # latWP_inDeg = [41.96701,41.9642, 41.91506]
    lonWP_inDeg = [] #[-88.10121, -87.9838, -87.89202] #(lonDep_deg + lonArr_deg) / 2
    latWP_inDeg = [] #[41.96701,41.9642, 41.91506] #(latDep_deg + latArr_deg) / 2
    
    # TripD = Chicago.TripDistance(depType,arrType,dep,arr)  # in miles      
    WayPoints = [lonWP_inDeg, latWP_inDeg]
    FP1, Heading, TripDistanceNonDirectRoute, distance, direction, aerodromeType = Chicago.DrawNonDirectRoutingTrip(depType, arrType, dep,arr, ac, cruiseAltitudeInFeet, WayPoints, Save=Save)
    
    # PlotPolar(ac, FP1, cruiseAltitudeInFeet, Heading, TripDistanceNonDirectRoute, distance, direction, aerodromeType)
   
    # lonWP_inDeg = []#[-88.10121, -87.9838, -87.89202] #(lonDep_deg + lonArr_deg) / 2
    # latWP_inDeg = []#[41.96701,41.9642, 41.91506] #(latDep_deg + latArr_deg) / 2
    # # lonWP_inDeg = []#[-88.10121, -87.9838, -87.89202] #(lonDep_deg + lonArr_deg) / 2
    # # latWP_inDeg = []#[41.96701,41.9642, 41.91506]
    # WayPoints = [lonWP_inDeg, latWP_inDeg]
    # Chicago.DrawNonDirectRoutingTrip(depType, arrType, dep,arr, Joby, cruiseAltitudeInFeet, WayPoints, Save=False)

    # for dep in DEP:
    #     for arr in ARR:
    #         # Chicago.DrawGeodesicTrip(depType, arrType, dep,arr, X, Y)
    #         FP1, Heading, TripDistanceNonDirectRoute, distance, direction, aerodromeType = Chicago.DrawNonDirectRoutingTrip(depType, arrType, dep,arr, Joby, cruiseAltitudeInFeet, WayPoints, Save=Save)
    # Chicago.ShowMap()

    if Show == True:
        Chicago.ShowMap()
    return Chicago.CLAP
    
def PlotCLAP(ac):
    altitude = np.linspace(1500,20000,30) # desired cruising altitude(s) in feet - it is in an array to be able to plot CLAP vs cruising altitudes
    CLAP = []
    
    for h in altitude:
        clap = PlotMultipleTrips(ac, h, False)
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
            X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(z,45,0)
            FootprintDistance = FootprintDistance * 0.621371 # km to miles
            altitude_ft = z
        else:
            altitude_ft = cruiseAltitudeInFeet
            X, Y, Radial, FootprintDistance = Joby.ReachableGroundFootprint(cruiseAltitudeInFeet,45,0)
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
        ax.set_title("Reachable Ground Footprint (miles) \n of Joby-like S4 eVTOL Vehicles under Gliding Conditions\n Altitude (ft): " + str(round(altitude_ft,0)) + " Trip Completion Percentage: " + str(round(100*TripDistanceArray[t]/TripD,0)) +" %" )
        ax.legend(loc='lower right',bbox_to_anchor=(1, 0))
        plt.tight_layout()
        number_str = str(t)
        plt.savefig('C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/Compass/step' + number_str.zfill(4) + '.png', dpi=300)