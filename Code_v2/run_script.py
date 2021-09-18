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

def PlotAllCLAP(altitude_Joby, CLAP_Joby, altitude_Lilium, CLAP_Lilium, altitude_Archer, CLAP_Archer, altitude_Volocopter, CLAP_Volocopter, altitude_Ehang, CLAP_Ehang):
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(altitude_Joby, CLAP_Joby, linewidth='3',color='blue',label='Joby')
    ax.plot(altitude_Lilium, CLAP_Lilium, linewidth='3', color='red',label='Lilium')
    ax.plot(altitude_Archer, CLAP_Archer, linewidth='3', color='green',label='Archer')
    ax.plot(altitude_Volocopter, CLAP_Volocopter, linewidth='3', color='magenta',label='Volocopter')
    ax.plot(altitude_Ehang, CLAP_Ehang, linewidth='3', color='black',label='EHang')
    
    ax.set_xlabel('Cruise Altitude (ft.)')
    ax.set_ylabel('Contingency Landing Assurance Percentage (%)')
    ax.set_title('Contingency Landing Assurance Pecentage vs. Cruise Altitude')
    ax.set_yticks([0,10,20,30,40,50,60,70,80,90,100])
    ax.set_xticks(np.arange(1500,7500,500))
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.25', color='black')
    ax.grid(which='minor', linestyle=':', linewidth='0.25', color='black')
    ax.legend(loc='center right')
    plt.savefig('C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/AllCLAPvsAltRevised.png', dpi=900)
    plt.show()
    
    
def RunScript(Option, SaveMap = False, GenerateMapVideo = False, GeneratePolarPlotVideo = False):
    """
    Parameters
    ----------
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

    Returns
    -------
    altitude : array
        an array of cruise altitudes in feet
    CLAP : array
        an array of Contingency Landing Assurance Percentages (CLAP)
    """
    
    Joby = Aircraft("Joby", 4, 200, 150, 13.8, 45, 2177, 200, S=10.7*1.7)
    Lilium7 = Aircraft("Lilium", 7, 186, 186, 16.3, 60, 1700, 187.8, S=10.7*1.7)
    Archer5 = Aircraft("Archer", 5, 175, 60, 11.3, 24, 3175, 160, S=10.7*1.7)
    Volocopter1 = Aircraft("Volocopter", 1, 70.6, 22, 2.5, 19, 900, 83.3, S=1.7*1.7)
    EHang1 = Aircraft("Ehang", 1, 62, 22, 1.5, 21, 1322, 206.2, S=10.7*1.7)
    AAE451 = Aircraft("AAE451", 1, 50, 8, 11.5, 10, 5.6, 0.048, 0.5)

    if Option == 1: # IF YOU WANT TO PLOT FOR A SPECIFIC CRUISING ALTITUDE, RUN THIS CODE
        PlotMultipleTrips(Joby, 3900, True, False) # input is the cruising altitude in ft
        # 2nd input is a boolean, to show the map once the analysis is done running
        # 3rd input is a boolean, to save the map once the analysis is done running
        
    elif Option == 2: # IF YOU WANT TO PLOT CLAP VS ALTITUDE, RUN THIS CODE
        altitude_Joby, CLAP_Joby = PlotCLAP(Joby)
        altitude_Lilium, CLAP_Lilium = PlotCLAP(Lilium7)
        altitude_Archer, CLAP_Archer = PlotCLAP(Archer5)
        altitude_Volocopter, CLAP_Volocopter = PlotCLAP(Volocopter1)
        altitude_Ehang, CLAP_Ehang = PlotCLAP(EHang1)
        PlotAllCLAP(altitude_Joby, CLAP_Joby, altitude_Lilium, CLAP_Lilium, altitude_Archer, CLAP_Archer, altitude_Volocopter, CLAP_Volocopter, altitude_Ehang, CLAP_Ehang)

    else:
        print("Pick the correct option")
    
    if GenerateMapVideo == True:
        """
        GENERATE VIDEO FROM THE ABOVE TRIP SEQUENCE
        """
        # Calling the generate_video function
        image_folder = "C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\TripAnimation\\" # make sure to use your folder
        video_name = 'DuPage2JHSHH.avi'
        os.chdir("C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\TripAnimation")
        generate_video(image_folder, video_name, 30)
        
    if GeneratePolarPlotVideo == True:
        """
        GENERATE VIDEO FROM THE ABOVE SEQUENCE OF POLAR PLOTS
        """
        # Calling the generate_video function
        image_folder = "C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\Compass\\" # make sure to use your folder
        video_name = 'DuPage2JHSHH.avi'
        os.chdir("C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\Compass")
        generate_video(image_folder, video_name, 30)
    
    try:
        return altitude_Joby, CLAP_Joby, altitude_Lilium, CLAP_Lilium, altitude_Archer, CLAP_Archer, altitude_Volocopter, CLAP_Volocopter, altitude_Ehang, CLAP_Ehang
    except:
        return None



# RunScript(1, GenerateMapVideo = False, GeneratePolarPlotVideo = False)
RunScript(2, GenerateMapVideo = False, GeneratePolarPlotVideo = False)


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

