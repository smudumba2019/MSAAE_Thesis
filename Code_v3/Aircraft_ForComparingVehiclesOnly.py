 # -*- coding: utf-8 -*-
"""
Created on Tue May 18 15:33:44 2021

@author: Sai Mudumba
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import itertools
from Aircraft import *
from shapely.geometry import Polygon

cruiseAlt = 1500 # cruising altitude in feet
POV = 1 # percentage of velocity
velty_Joby = 1*74*POV # m/s
JobyS4 = Aircraft("Joby", 4, 165, 150, 13.8, 45, 2177, 254.4, S=10.7*1.7)
JobyS4.Characteristics()
X_JobyS4, Y_JobyS4, Radial_JobyS4, Distance_JobyS4 = JobyS4.ReachableGroundFootprint(cruiseAlt,velty_Joby,35,0)
RGF_Area_Ref_JobyS4 = Polygon(zip(X_JobyS4, Y_JobyS4)) # Assuming the OP's x,y coordinates
RGF_Area_Ref_JobyS4 = (RGF_Area_Ref_JobyS4.area/(1000**2)) * (0.621371**2) # in mi^2

velty_Lilium = 78*POV # m/s
Lilium7 = Aircraft("Joby", 7, 175, 124, 16.3, 53, 3175, 305, S=11*1.1)
Lilium7.Characteristics()
X_Lilium7, Y_Lilium7, Radial_Lilium7, Distance_Lilium7 = Lilium7.ReachableGroundFootprint(cruiseAlt,velty_Lilium,35,0)
RGF_Area_Ref_Lilium7 = Polygon(zip(X_Lilium7, Y_Lilium7)) # Assuming the OP's x,y coordinates
RGF_Area_Ref_Lilium7 = (RGF_Area_Ref_Lilium7.area/(1000**2)) * (0.621371**2) # in mi^2

velty_Archer = 67*POV # m/s
Archer5 = Aircraft("Joby", 5, 150, 60, 11.3, 24, 3175, 160, S=13*1.1)
Archer5.Characteristics()
X_Archer5, Y_Archer5, Radial_Archer5, Distance_Archer5 = Archer5.ReachableGroundFootprint(cruiseAlt,velty_Archer,35,0)
RGF_Area_Ref_Archer = Polygon(zip(X_Archer5, Y_Archer5)) # Assuming the OP's x,y coordinates
RGF_Area_Ref_Archer = (RGF_Area_Ref_Archer.area/(1000**2)) * (0.621371**2) # in mi^2

velty_Volo = 25*POV # m/s
Volocopter1 = Aircraft("Joby", 1, 56, 22, 2.5, 19, 900, 83.3, S=1**2)
Volocopter1.Characteristics()
X_Volocopter1, Y_Volocopter1, Radial_Volocopter1, Distance_Volocopter1 = Volocopter1.ReachableGroundFootprint(cruiseAlt,velty_Volo,35,0)
RGF_Area_Ref_Volo = Polygon(zip(X_Volocopter1, Y_Volocopter1)) # Assuming the OP's x,y coordinates
RGF_Area_Ref_Volo = (RGF_Area_Ref_Volo.area/(1000**2)) * (0.621371**2) # in mi^2

velty_Ehang = 28*POV # m/s
EHang1 = Aircraft("Joby", 1, 62, 22, 1.5, 21, 1322, 206.2, S=1**2)
EHang1.Characteristics()
X_EHang1, Y_EHang1, Radial_EHang1, Distance_EHang1 = EHang1.ReachableGroundFootprint(cruiseAlt,velty_Ehang,35,0)
RGF_Area_Ref_Ehang = Polygon(zip(X_EHang1, Y_EHang1)) # Assuming the OP's x,y coordinates
RGF_Area_Ref_Ehang = (RGF_Area_Ref_Ehang.area/(1000**2)) * (0.621371**2) # in mi^2

# PLOT ALL ON THE SAME POLAR PLOT
linewidth=2
fig, ax = plt.subplots(subplot_kw=dict(polar=True), dpi=600, figsize=(8,6))
ax.plot(Radial_JobyS4, Distance_JobyS4*0.621371, 'b', linewidth=linewidth, label='Joby S4: '+ str(round(RGF_Area_Ref_JobyS4,2)) + ' sq. mi')
ax.plot(Radial_Lilium7, Distance_Lilium7*0.621371, 'r', linewidth=linewidth,label='Lilium S7: ' + str(round(RGF_Area_Ref_Lilium7,2)) + ' sq. mi')
ax.plot(Radial_Archer5, Distance_Archer5*0.621371, 'g', linewidth=linewidth,label='Archer S5: ' + str(round(RGF_Area_Ref_Archer,2)) + ' sq. mi')
ax.plot(Radial_Volocopter1, Distance_Volocopter1*0.621371, 'm', linewidth=linewidth,label='Volocopter S1: ' + str(round(RGF_Area_Ref_Volo,2)) + ' sq. mi')
ax.plot(Radial_EHang1, Distance_EHang1*0.621371, 'k', linewidth=linewidth,label='EHang S1: '+ str(round(RGF_Area_Ref_Ehang,2)) + ' sq. mi')
ax.set_theta_direction(-1) # CW direction 
ax.set_theta_zero_location('N')
ax.set_title("Cruising Altitude: " + str(cruiseAlt) +" feet \nReachable Ground Footprint (mi) and its Footprint Area (sq. mi) \nComparison of eVTOL Vehicles under Gliding Conditions")
ax.legend(loc='lower left',bbox_to_anchor=(1, 0.6))
# ax.set_rticks([0,1, 2,3,4])
ax.set_rticks([0,1, 2,3, 4,5])
# ax.set_rticks([0,1, 2,3, 4,5,6,7,8])
# ax.set_rticks([0, 2, 4, 6, 8, 10, 12, 14, 16])
# ax.set_rticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])
plt.tight_layout()
plt.savefig('C:/Users/saimu/OneDrive - purdue.edu/Purdue Graduate School/MS_Aeronautical_Astronautical_Engineering/MS Thesis Research/Spring 2022/Python_Code/Results/Miscellaneous/ComparisonOfReachableFootprint1500FT_25deg.png', dpi=600)
plt.show()