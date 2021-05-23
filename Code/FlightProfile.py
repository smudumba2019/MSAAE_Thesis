# -*- coding: utf-8 -*-
"""
Created on Sat May 15 22:08:02 2021

@author: Sai Mudumba
"""
import math
import matplotlib.pyplot as plt
import numpy as np
import itertools
from Aircraft import *

class FlightProfile:
    def __init__(self, cruise_alt, trip_distance):
        self.JobyS4 = Aircraft("Joby", 4, 200, 150, 13.8, 45, 2177, 254.4, S=10.7*1.7)

        # Define mission segments 
        # The input is the trip information origin and destination (i.e., trip distance), cruise height
        # Segments A, B, C are defined in the following ways [height (m), range (m), horizontal speed (m/s), vertical speed (m/s)]
        
        numPoints = 10
        self.altitude_cr = cruise_alt * 0.3048
        self.tripDistance = trip_distance * 1609.34 # trip geodesic distance in meters
        if cruise_alt == 1500:
            # self.cruiseSpeed = 150 * 0.44704
            self.cruiseSpeed = self.JobyS4.cruiseSpeed * 0.44704
        else:
            self.cruiseSpeed = self.JobyS4.cruiseSpeed * 0.44704
        self.velocity_cr = self.cruiseSpeed 
        
        dh = self.altitude_cr - 3.048
        self.dx = self.velocity_cr * 60
        self.climbAngle = math.atan(dh/self.dx) # climb angle in radians
        self.ROC = math.tan(self.climbAngle) * self.velocity_cr
        if self.ROC >= 10: # cap rate of climb to 10 m/s
            self.ROC = 10
        
        self.ROD = -self.ROC
    
        self.segment_A_altitude = np.multiply(np.linspace(0, 3.048, numPoints),3.28084)
        self.segment_B_altitude = np.multiply(np.linspace(3.048, self.altitude_cr, numPoints),3.28084)
        self.segment_C_altitude = np.multiply(np.linspace(self.altitude_cr, self.altitude_cr, numPoints),3.28084)
        self.segment_D_altitude = np.multiply(np.linspace(self.altitude_cr, 3.048, numPoints),3.28084)
        self.segment_E_altitude = np.multiply(np.linspace(3.048, 0, numPoints),3.28084)
    
        self.segment_A_range = np.multiply(np.linspace(0, 0, numPoints), 0.000621371)
        self.segment_B_range = np.multiply(np.linspace(0, self.dx, numPoints), 0.000621371)
        self.segment_C_range = np.multiply(np.linspace(self.dx, self.tripDistance - self.dx, numPoints),0.000621371)
        self.segment_D_range = np.multiply(np.linspace(self.tripDistance - self.dx, self.tripDistance, numPoints),0.000621371)
        self.segment_E_range = np.multiply(np.linspace(self.tripDistance, self.tripDistance, numPoints),0.000621371)
    
        self.segment_A_horz_vel = np.linspace(0, 0, numPoints)
        self.segment_B_horz_vel = np.linspace(0, self.velocity_cr, numPoints)
        self.segment_C_horz_vel = np.linspace(self.velocity_cr, self.velocity_cr, numPoints)
        self.segment_D_horz_vel = np.linspace(self.velocity_cr, 0, numPoints)
        self.segment_E_horz_vel = np.linspace(0, 0, numPoints)
    
        self.segment_A_vert_vel = np.linspace(0.1016, 0.1016, numPoints)
        self.segment_B_vert_vel = np.linspace(self.ROC, self.ROC, numPoints)
        self.segment_C_vert_vel = np.linspace(0, 0, numPoints)
        self.segment_D_vert_vel = np.linspace(self.ROD, self.ROD, numPoints)
        self.segment_E_vert_vel = np.linspace(-0.1016, -0.1016, numPoints)

    def PlotMissionProfile(self, fig, ax, color, case):
        ax.plot(self.segment_A_range, self.segment_A_altitude, '-b', color=color, linewidth=2)
        ax.plot(self.segment_B_range, self.segment_B_altitude, '-b', color=color, linewidth=2)
        ax.plot(self.segment_C_range, self.segment_C_altitude, '-b', color=color, linewidth=2, label=case + str(round(max(self.segment_C_altitude))) + " ft., " "Cruise Speed: " + str(round(self.cruiseSpeed/0.44704)) + " mph")
        ax.plot(self.segment_D_range, self.segment_D_altitude, '-b', color=color, linewidth=2)
        ax.plot(self.segment_E_range, self.segment_E_altitude, '-b', color=color, linewidth=2)
        ax.set_title("Mission Profile using Joby-like S4 eVTOL Aircraft: \nDuPage Airport to John H. Stroger Hospital Helipad Trips")
        ax.set_xlabel("Trip Distance (miles)")
        ax.set_ylabel("Altitude above Mean Sea Level (feet)")
        plt.grid()
        
        
       
        
    def FlightTime(self):
        time_takeoff = 3.048 / 0.1016 # in seconds
        self.time_takeoff = time_takeoff
        time_climb = self.altitude_cr / self.ROC # in seconds
        self.time_climb = time_climb
        time_cruise = (self.tripDistance - self.dx) / self.velocity_cr
        self.time_cruise = time_cruise
        time_descend = time_climb
        self.time_descend = time_descend
        time_land = time_takeoff
        self.time_land = time_land
        
        timeFlight = (time_takeoff + time_climb + time_cruise + time_descend + time_land) / 60 # in minutes
        print(f"Cruise Altitude: {int(self.altitude_cr)} meters , Flight Time: {round(timeFlight,2)} minutes")
        return timeFlight
    
    def EnergyConsumption(self):
        self.g = 9.81
        E_TO = self.time_takeoff * self.JobyS4.MTOW*self.g * math.sqrt(45.8948 / (2 * 1.225)) / 0.63
        E_CL = self.time_climb * (self.JobyS4.MTOW*self.g / 0.765) * (self.ROC + (self.cruiseSpeed / self.JobyS4.LDratio))
        E_CR = self.time_cruise * (self.JobyS4.MTOW*self.g / self.JobyS4.LDratio) * self.cruiseSpeed / 0.765
        E_DS = self.time_descend * (self.JobyS4.MTOW*self.g / 0.765) * (self.ROD + (self.cruiseSpeed / self.JobyS4.LDratio))
        E_LND = self.time_land * self.JobyS4.MTOW*self.g * math.sqrt(45.8948 / (2 * 1.225)) / 0.63
        self.E_TOTAL = (E_TO + E_CL + E_CR + E_DS + E_LND) / 3600 / 1000
        print(f"Energy Consumed: {round(self.E_TOTAL,2)} kWh")
        return (self.E_TOTAL)
    
    def GivenRangeOutputAltitude(self, distance):
        distance = 1609.34 * distance # miles to m
        
        if distance >= self.dx and distance <= self.tripDistance - self.dx:
            Y = self.altitude_cr
        elif distance > 0 and distance <= self.dx:
            dX = self.segment_B_range[-1] - self.segment_B_range[0] 
            dY = self.segment_B_altitude[-1] - self.segment_B_altitude[0]
            slope = dY / dX
            X0 = self.segment_B_range[0]
            Y0 = self.segment_B_altitude[0]
            Y = slope * (distance - X0) + Y0
        elif distance < self.tripDistance and distance > (self.tripDistance - self.dx):
            dX = self.segment_D_range[-1] - self.segment_D_range[0] 
            dY = self.segment_D_altitude[-1] - self.segment_D_altitude[0]
            slope = dY / dX
            X0 = self.segment_D_range[0]
            Y0 = self.segment_D_altitude[0]
            Y = slope * (distance - X0) + Y0
        elif distance == 0:
            Y = 3.048
        elif distance == self.tripDistance:
            Y = 3.048
        
        # X = list(itertools.chain(self.segment_A_range , self.segment_B_range , self.segment_C_range , self.segment_D_range , self.segment_E_range))
        # Y = list(itertools.chain(self.segment_A_altitude , self.segment_B_altitude , self.segment_C_altitude , self.segment_D_altitude , self.segment_E_altitude))
        return (distance, Y)
        
    def __call__(self):
        print(f'Takeoff Vertical Velocity: {self.segment_A_vert_vel[0]} m/s')
        print(f'Rate of Climb: {self.ROC} m/s and Climb Angle: {self.climbAngle*180/math.pi} deg')

        
# font = {'family': 'serif',
#         'color':  'darkred',
#         'weight': 'normal',
#         'size': 12,
#         }
# fig, ax = plt.subplots(figsize = (8, 5),dpi=300)

# FP1 = FlightProfile(3750, 30)
# one = FP1.PlotMissionProfile(fig, ax, "red","Cruise Altitude Floor: ")
# FP1_time = FP1.FlightTime()
# E1 = FP1.EnergyConsumption()

# FP2 = FlightProfile(1500, 30)
# two = FP2.PlotMissionProfile(fig, ax, "blue","Reference Flight Case: ")
# FP2_time = FP2.FlightTime()
# E2 = FP2.EnergyConsumption()


# plt.text(5, 1250, " Total Energy Consumed: " + str(round(E2))+" kWh", fontdict=font)
# plt.text(5, 950, " Total Flight Time: " + str(round(FP2_time))+" minutes", fontdict=font)

# plt.text(5, 3450, " Total Energy Consumed: " + str(round(E1))+" kWh", fontdict=font)
# plt.text(5, 3150, " Total Flight Time: " + str(round(FP1_time))+" minutes", fontdict=font)
# plt.legend()
# plt.show()
# X,Y = FP2.GivenRangeOutputAltitude(2000)
# X,Y = FP2.GivenRangeOutputAltitude(20000)
# X,Y = FP2.GivenRangeOutputAltitude(45000)
# X,Y = FP2.GivenRangeOutputAltitude(30 * 1609.34)

# FP3 = FlightProfile(5000, 30)
# FP3.PlotMissionProfile()
# FP3_time = FP3.FlightTime()
# X,Y = FP3.GivenRangeOutputAltitude(2000)
# X,Y = FP3.GivenRangeOutputAltitude(20000)
# X,Y = FP3.GivenRangeOutputAltitude(45000)
# X,Y = FP3.GivenRangeOutputAltitude(30 * 1609.34)