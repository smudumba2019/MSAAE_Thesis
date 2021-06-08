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

PlotMultipleTrips()
# main()

# """
# GENERATE VIDEO FROM THE ABOVE TRIP SEQUENCE
# """
# # Calling the generate_video function
# image_folder = "C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\TripAnimation\\" # make sure to use your folder
# video_name = 'DuPage2JHSHH.avi'
# os.chdir("C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\TripAnimation")
# generate_video(image_folder, video_name, 15)

# """
# GENERATE VIDEO FROM THE ABOVE SEQUENCE OF POLAR PLOTS
# """
# # Calling the generate_video function
# image_folder = "C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\Compass\\" # make sure to use your folder
# video_name = 'DuPage2JHSHH.avi'
# os.chdir("C:\\Users\\Sai Mudumba\\Documents\\MSAAE_Thesis_Code\\Images\\Compass")
# generate_video(image_folder, video_name, 10)



# FP1 = FlightProfile(1500, 30)
# FP1.PlotMissionProfile()
# FP1_time = FP1.FlightTime()
# print(FP1_time)

# FP2 = FlightProfile(3000, 30)
# FP2.PlotMissionProfile()
# FP2_time = FP2.FlightTime()
# print(FP2_time)