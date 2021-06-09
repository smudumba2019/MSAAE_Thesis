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
import os

import math
import matplotlib.pyplot as plt


def RunScript(Option, SaveMap = False, GenerateMapVideo = False, GeneratePolarPlotVideo = False):
    if Option == 1: # IF YOU WANT TO PLOT FOR A SPECIFIC CRUISING ALTITUDE, RUN THIS CODE
        PlotMultipleTrips(3350, True) # input is the cruising altitude in ft
    elif Option == 2: # IF YOU WANT TO PLOT CLAP VS ALTITUDE, RUN THIS CODE
        PlotCLAP()
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
        generate_video(image_folder, video_name, 15)
        
    if GeneratePolarPlotVideo == True:
        """
        GENERATE VIDEO FROM THE ABOVE SEQUENCE OF POLAR PLOTS
        """
        # Calling the generate_video function
        image_folder = "C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\Compass\\" # make sure to use your folder
        video_name = 'DuPage2JHSHH.avi'
        os.chdir("C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\Compass")
        generate_video(image_folder, video_name, 10)

RunScript(1, GenerateMapVideo = False, GeneratePolarPlotVideo = False)