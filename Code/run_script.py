# -*- coding: utf-8 -*-
"""
Author: Sai V. Mudumba
Code Conceived: March, 2021
Code Last Modified: May 15, 2021
"""

from main import *
from PlotInPolarCoordinates import *
from generate_video import *
from FlightProfile import *
from Aircraft import *

import math
import matplotlib.pyplot as plt

main()

"""
GENERATE VIDEO FROM THE ABOVE SEQUENCE OF POLAR PLOTS
"""
# Calling the generate_video function
generate_video()



# FP1 = FlightProfile(1500, 30)
# FP1.PlotMissionProfile()
# FP1_time = FP1.FlightTime()
# print(FP1_time)

# FP2 = FlightProfile(3000, 30)
# FP2.PlotMissionProfile()
# FP2_time = FP2.FlightTime()
# print(FP2_time)