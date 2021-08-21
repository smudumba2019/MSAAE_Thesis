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


def RunScript(Option, SaveMap = False, GenerateMapVideo = False, GeneratePolarPlotVideo = False):
    if Option == 1: # IF YOU WANT TO PLOT FOR A SPECIFIC CRUISING ALTITUDE, RUN THIS CODE
        PlotMultipleTrips(2750, True, False) # input is the cruising altitude in ft
    elif Option == 2: # IF YOU WANT TO PLOT CLAP VS ALTITUDE, RUN THIS CODE
        altitude, CLAP = PlotCLAP()
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
        generate_video(image_folder, video_name, 10)
        
    if GeneratePolarPlotVideo == True:
        """
        GENERATE VIDEO FROM THE ABOVE SEQUENCE OF POLAR PLOTS
        """
        # Calling the generate_video function
        image_folder = "C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\Compass\\" # make sure to use your folder
        video_name = 'DuPage2JHSHH.avi'
        os.chdir("C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\Compass")
        generate_video(image_folder, video_name, 10)
    try:
        return (altitude, CLAP)
    except:
        return None

RunScript(1, GenerateMapVideo = False, GeneratePolarPlotVideo = False)


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