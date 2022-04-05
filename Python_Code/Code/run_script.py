# -*- coding: utf-8 -*-
"""
Author: Sai V. Mudumba
Code Conceived: March, 2021
Code Last Modified: May 15, 2021
"""

# from main import *
from main_ForTestingPurposesOnly import *
from PlotInPolarCoordinates import *
from generate_video import *
from FlightProfile import *
from Aircraft import *
from TripMapper import *
import os

import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import time
start_time = time.time()

import numba
from numba import jit, cuda # https://www.geeksforgeeks.org/running-python-script-on-gpu/

def PlotAllCLAP(altitude_Joby, CLAP_Joby, altitude_Lilium, CLAP_Lilium, altitude_Archer, CLAP_Archer, altitude_Volocopter, CLAP_Volocopter, altitude_Ehang, CLAP_Ehang):
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(altitude_Joby, CLAP_Joby, linewidth='2', color='blue', marker = 'P', label='Joby')
    ax.plot(altitude_Lilium, CLAP_Lilium, linewidth='2', color='red', marker = 'o', label='Lilium')
    ax.plot(altitude_Archer, CLAP_Archer, linewidth='2', color='green', marker = '^', label='Archer')
    ax.plot(altitude_Volocopter, CLAP_Volocopter, linewidth='2', color='magenta', marker = 's', label='Volocopter')
    ax.plot(altitude_Ehang, CLAP_Ehang, linewidth='2', color='black', marker = 'D', label='EHang')
    
    ax.set_xlabel('Cruise Altitude (ft.)')
    ax.set_ylabel('Contingency Landing Assurance Percentage (%)')
    ax.set_title('Contingency Landing Assurance Pecentage vs. Cruise Altitude')
    ax.set_yticks([0,10,20,30,40,50,60,70,80,90,100])
    ax.set_xticks(np.arange(1500,7500,500))
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.25', color='black')
    ax.grid(which='minor', linestyle=':', linewidth='0.25', color='black')
    ax.legend(loc='upper right')
    plt.savefig('C:/Users/saimu/OneDrive - purdue.edu/Purdue Graduate School/MS_Aeronautical_Astronautical_Engineering/MS Thesis Research/Spring 2022/Python_Code/Results/AllCLAPvsAltRevised.png', dpi=600)
    plt.show()

def FindCruiseAltitudeFloor(altitude, CLAP):
    for i in range(0, len(altitude)):
        if CLAP[i] >= 90:
            CAF = altitude[i]
            break
        else:
            CAF = altitude[i]
    return CAF

def RunScript(TripInfo, CAF, Option, SaveMap = False, GenerateMapVideo = False, GeneratePolarPlotVideo = False, PlotGraphs = False):
    """
    Parameters
    ----------
    TripInfo
        DepType = "Heliport"
        DepartureID = 7
        ArrType = "Regional"
        ArrivalID = 8
    
    CAF : float
        CAF stands for Cruise Altitude Floor, in feet
    
    Option : integer
        This input tells the function what analysis to run. 
        Option 1 means plot multiple trips, their respective distance and polar plots 
        Option 2 means plot CLAP versus various cruising altitudes
        
    SaveMap : boolean, optional
        Do you want to save the map? The default is False.
    
    GenerateMapVideo : boolean, optional
        Do you want to generate map video from the map images you saved? The default is False.
    
    GeneratePolarPlotVideo : boolean, optional
        Do you want to generate polar plots from the polar plots you saved? The default is False.

    PlotsGraphs : boolean, optional
        Do you want to plot graphs in this run? The graphs include distance to contingency landing sites and flight profile
    
    Returns
    -------
    altitude : array
        an array of cruise altitudes in feet
    CLAP : array
        an array of Contingency Landing Assurance Percentages (CLAP)
    """
    
    Joby = Aircraft("Joby", 4, 165, 150, 13.8, 45, 2177, 200, S=10.7*1.7)
    Lilium7 = Aircraft("Lilium", 7, 175, 124, 16.3, 53, 3175, 305, S=10.7*1.7)
    Archer5 = Aircraft("Archer", 5, 150, 60, 11.3, 24, 3175, 160, S=10.7*1.7)
    Volocopter1 = Aircraft("Volocopter", 1, 56, 22, 2.5, 19, 900, 83.3, S=1.7*1.7)
    EHang1 = Aircraft("Ehang", 1, 62, 22, 1.5, 21, 1322, 206.2, S=10.7*1.7)
    AAE451 = Aircraft("AAE451", 1, 50, 8, 11.5, 10, 5.6, 0.048, 0.5)
    
    if Option == 1: # IF YOU WANT TO PLOT FOR A SPECIFIC CRUISING ALTITUDE, RUN THIS CODE
        """
        1st input is TripInfo
        2nd input is the cruising altitude in ft
        3rd input is a boolean, to show the map once the analysis is done running
        4th input is a boolean, to save the map once the analysis is done running
        5th input is a boolean, to shows any graphs done in the analysis
        """   
        CLAP_Joby_atCAF, FltTime_Joby, EneConsumed_Joby, FltTime_Joby_ref, EneConsumed_Joby_ref = PlotMultipleTrips(TripInfo, Joby, CAF[0], False, False, PlotGraphs) 
        CLAP_Lilium_atCAF, FltTime_Lilium, EneConsumed_Lilium, FltTime_Lilium_ref, EneConsumed_Lilium_ref = PlotMultipleTrips(TripInfo, Lilium7, CAF[1], False, False, PlotGraphs) 
        CLAP_Archer_atCAF, FltTime_Archer, EneConsumed_Archer, FltTime_Archer_ref, EneConsumed_Archer_ref = PlotMultipleTrips(TripInfo, Archer5, CAF[2], False, False, PlotGraphs) 
        
    elif Option == 2: # IF YOU WANT TO PLOT CLAP VS ALTITUDE, RUN THIS CODE
        altitude_Joby, CLAP_Joby = PlotCLAP(TripInfo, Joby)
        CAF_Joby = FindCruiseAltitudeFloor(altitude_Joby, CLAP_Joby)
        
        altitude_Lilium, CLAP_Lilium = PlotCLAP(TripInfo, Lilium7)
        CAF_Lilium = FindCruiseAltitudeFloor(altitude_Lilium, CLAP_Lilium)
        
        altitude_Archer, CLAP_Archer = PlotCLAP(TripInfo, Archer5)
        CAF_Archer = FindCruiseAltitudeFloor(altitude_Archer, CLAP_Archer)
        
        altitude_Volocopter, CLAP_Volocopter = ([],[])#PlotCLAP(TripInfo, Volocopter1)
        altitude_Ehang, CLAP_Ehang = ([],[]) #PlotCLAP(TripInfo, EHang1)
        # altitude_Volocopter, CLAP_Volocopter = PlotCLAP(TripInfo, Volocopter1)
        # altitude_Ehang, CLAP_Ehang = PlotCLAP(TripInfo, EHang1)
        
        PlotAllCLAP(altitude_Joby, CLAP_Joby, altitude_Lilium, CLAP_Lilium, altitude_Archer, CLAP_Archer, altitude_Volocopter, CLAP_Volocopter, altitude_Ehang, CLAP_Ehang)
        
        ## Optional:
        # print(CAF_Joby, CAF_Lilium, CAF_Archer)
    elif Option == 3:
        CLAP_Joby_atCAF, FltTime_Joby, EneConsumed_Joby, FltTime_Joby_ref, EneConsumed_Joby_ref = PlotMultipleTrips(TripInfo, Joby, 7220, True, False, PlotGraphs) 
    
    else:
        print("Pick the correct option")
    
    if GenerateMapVideo == True:
        """
        GENERATE VIDEO FROM THE ABOVE TRIP SEQUENCE
        """
        # Calling the generate_video function
        image_folder = 'C:/Users/saimu/Documents/AAE_MS_Thesis_Documentation_v2/Python_Code/Results/Trip_Map/' # make sure to use your folder
        video_name = 'DuPage2JHSHH_map.avi'
        os.chdir('C:/Users/saimu/Documents/AAE_MS_Thesis_Documentation_v2/Python_Code/Results')
        generate_video(image_folder, video_name, 30)
        
    if GeneratePolarPlotVideo == True:
        """
        GENERATE VIDEO FROM THE ABOVE SEQUENCE OF POLAR PLOTS
        """
        # Calling the generate_video function
        image_folder = 'C:/Users/saimu/Documents/AAE_MS_Thesis_Documentation_v2/Python_Code/Results/Compass_Map/' # make sure to use your folder
        video_name = 'DuPage2JHSHH_polar.avi'
        os.chdir('C:/Users/saimu/Documents/AAE_MS_Thesis_Documentation_v2/Python_Code/Results')
        generate_video(image_folder, video_name, 30)
    
    try: # IF OPTION 2 WAS CHOSEN
        return (CAF_Joby, CAF_Lilium, CAF_Archer)
    except: # IF OPTION 1 WAS CHOSEN
        return ((CLAP_Joby_atCAF, FltTime_Joby, EneConsumed_Joby, FltTime_Joby_ref, EneConsumed_Joby_ref),(CLAP_Lilium_atCAF, FltTime_Lilium, EneConsumed_Lilium, FltTime_Lilium_ref, EneConsumed_Lilium_ref),(CLAP_Archer_atCAF, FltTime_Archer, EneConsumed_Archer, FltTime_Archer_ref, EneConsumed_Archer_ref))

"""
RUN THE CODE FOR FINDING THE CRUISE ALTITUDE FLOOR OF EACH VEHICLE BELOW FOR MULTIPLE TRIPS IN A NETWORK
"""

DepType = "Regional"
ArrType = "Regional"
DEP = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16]
ARR = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16] #[2, 3, 4, 5, 8, 9, 10, 11, 12, 13]
# DEP = [2, 3, 4, 5, 8, 9, 10, 11, 12, 13]
#ARR = [2, 3, 4, 5, 8, 9, 10, 11, 12, 13]
#DEP = [2]
#ARR = [4]
# RunScript((DepType, DEP[0], ArrType, ARR[0]), 7220, 3, GenerateMapVideo = False, GeneratePolarPlotVideo = False, PlotGraphs = True)

AerodromeKeys = [] # Store the from and to trip information as a string
TripsCAF = [] # Store a list of Cruise Altitude Floor values with each column representing an eVTOL vehicle and each row being the trip
TripsFlightTime = []
TripsEnergyConsumed = []
TripsFlightTime_Ref = []
TripsEnergyConsumed_Ref = []

for dep in DEP: # example: DEP = [7, 9, 13, 9]
    for arr in ARR: # example: ARR = [8, 6, 7, 11]
        TripInfo = (DepType, dep, ArrType, arr) # a tuple that contains Departure Type, Departure ID, Arrival Type, Arrival ID
        FromTo = DepType + " ID: " + str(dep) + " to " + ArrType + " ID: " + str(arr) # a string that summarizes trip info
        
        """The line below runs the script and gets the Cruise Altitude Floor Req for each vehicle, for each trip in a network"""
        if arr != dep or ArrType != DepType:
            CAF_Joby, CAF_Lilium, CAF_Archer = RunScript(TripInfo, 0, 2, GenerateMapVideo = False, GeneratePolarPlotVideo = False, PlotGraphs = False)
            Joby_Data, Lilium_Data, Archer_Data = RunScript(TripInfo, (CAF_Joby, CAF_Lilium, CAF_Archer), 1, GenerateMapVideo = False, GeneratePolarPlotVideo = False, PlotGraphs = False)
    
            # Append to a List
            TripsCAF.append([CAF_Joby, CAF_Lilium, CAF_Archer])
            TripsFlightTime.append([Joby_Data[1], Lilium_Data[1], Archer_Data[1], Joby_Data[3], Lilium_Data[3], Archer_Data[3]])
            TripsEnergyConsumed.append([Joby_Data[2], Lilium_Data[2], Archer_Data[2], Joby_Data[4], Lilium_Data[4], Archer_Data[4]])
            AerodromeKeys.append([FromTo])


"""    
1. CONVERT CRUISE ALTITUDE FLOORS TO A NUMPY ARRAY
2. CREATE A PANDAS DATAFRAME
3. EXPORT THE PANDAS DATAFRAME TO EXCEL

Ref: 
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
    https://datatofish.com/export-dataframe-to-excel/

"""
TripsCAF_numpy = np.array(TripsCAF)
df = pd.DataFrame(TripsCAF_numpy, columns=['Joby','Lilium','Archer'])
df.to_excel (r'C:/Users/saimu/OneDrive - purdue.edu/Purdue Graduate School/MS_Aeronautical_Astronautical_Engineering/MS Thesis Research/Spring 2022/TripsCruiseAltitudeFloor_Dataframe.xlsx', index = False, header=True)

TripsFlightTime_numpy = np.array(TripsFlightTime)
df1 = pd.DataFrame(TripsFlightTime_numpy, columns=['Joby','Lilium','Archer','Joby','Lilium','Archer'])
df1.to_excel (r'C:/Users/saimu/OneDrive - purdue.edu/Purdue Graduate School/MS_Aeronautical_Astronautical_Engineering/MS Thesis Research/Spring 2022/TripsFlightTimes_Dataframe.xlsx', index = False, header=True)

TripsEnergyConsumed_numpy = np.array(TripsEnergyConsumed)
df2 = pd.DataFrame(TripsEnergyConsumed_numpy, columns=['Joby','Lilium','Archer','Joby','Lilium','Archer'])
df2.to_excel (r'C:/Users/saimu/OneDrive - purdue.edu/Purdue Graduate School/MS_Aeronautical_Astronautical_Engineering/MS Thesis Research/Spring 2022/TripsEnergyConsumed_Dataframe.xlsx', index = False, header=True)

Trips_numpy = np.array(AerodromeKeys)
df3 = pd.DataFrame(Trips_numpy, columns=['TripsInfo'])
df3.to_excel (r'C:/Users/saimu/OneDrive - purdue.edu/Purdue Graduate School/MS_Aeronautical_Astronautical_Engineering/MS Thesis Research/Spring 2022/Trips_Dataframe.xlsx', index = False, header=True)

print("--- %s seconds ---" % (time.time() - start_time))

# altitudeD, CLAPD = RunScript(2, GenerateMapVideo = False, GeneratePolarPlotVideo = False)
# altitudeND, CLAPND = RunScript(2, GenerateMapVideo = False, GeneratePolarPlotVideo = False)

# #  PLOTTING MULTIPLE CLAP VS ALTITUDES FOR DIRECT AND NON-DIRECT ROUTES 
# #  UNCOMMENT ONLY WHEN IT IS NEEDED
# fig, ax = plt.subplots(figsize=(8,5))
# ax.plot(altitudeD, CLAPD,linewidth='3',color='blue',label='Direct Route: 30 miles long')
# ax.plot(altitudeND, CLAPND, linewidth='3', color='red',label='Non-direct Route: 3.3% longer')
# ax.set_xlabel('Cruise Altitude Floor (ft.)')
# ax.set_ylabel('Contingency Landing Assurance Percentage (%)')
# ax.set_title('Contingency Landing Assurance Pecentage vs. Cruise Altitude Floor')
# ax.set_yticks([0,10,20,30,40,50,60,70,80,90,100])
# ax.set_xticks(np.arange(1500,7500,500))
# ax.minorticks_on()
# ax.grid(which='major', linestyle='-', linewidth='0.25', color='black')
# ax.grid(which='minor', linestyle=':', linewidth='0.25', color='black')
# ax.legend(loc='lower right')
# plt.savefig('C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/AllCLAPvsAltRevised.png', dpi=900)
# plt.show()

#  PLOTTING MULTIPLE CLAP VS ALTITUDES FOR DIRECT AND NON-DIRECT ROUTES 
#  UNCOMMENT ONLY WHEN IT IS NEEDED

