# -*- coding: utf-8 -*-
"""
Created on Sat May 15 22:08:02 2021

@author: Sai Mudumba
"""
import math
import matplotlib.pyplot as plt
import numpy as np
import itertools

class FlightProfile:
    def __init__(self, cruise_alt, trip_distance):
        # Define mission segments 
        # The input is the trip information origin and destination (i.e., trip distance), cruise height
        # Segments A, B, C are defined in the following ways [height (m), range (m), horizontal speed (m/s), vertical speed (m/s)]
        
        numPoints = 10
        self.altitude_cr = cruise_alt * 0.3048
        self.tripDistance = trip_distance * 1609.34 # trip geodesic distance in meters
        self.velocity_cr = 67 
        
        dh = self.altitude_cr - 3.048
        self.dx = self.velocity_cr * 60
        self.climbAngle = math.atan(dh/self.dx) # climb angle in radians
        self.ROC = math.tan(self.climbAngle) * self.velocity_cr
        if self.ROC >= 10: # cap rate of climb to 10 m/s
            self.ROC = 10
        
        self.ROD = -self.ROC
    
        self.segment_A_altitude = np.linspace(0, 3.048, numPoints)
        self.segment_B_altitude = np.linspace(3.048, self.altitude_cr, numPoints)
        self.segment_C_altitude = np.linspace(self.altitude_cr, self.altitude_cr, numPoints)
        self.segment_D_altitude = np.linspace(self.altitude_cr, 3.048, numPoints)
        self.segment_E_altitude = np.linspace(3.048, 0, numPoints)
    
        self.segment_A_range = np.linspace(0, 0, numPoints)
        self.segment_B_range = np.linspace(0, self.dx, numPoints)
        self.segment_C_range = np.linspace(self.dx, self.tripDistance - self.dx, numPoints)
        self.segment_D_range = np.linspace(self.tripDistance - self.dx, self.tripDistance, numPoints)
        self.segment_E_range = np.linspace(self.tripDistance, self.tripDistance, numPoints)
    
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

    def PlotMissionProfile(self):
        fig, ax = plt.subplots(figsize = (8, 5),dpi=300)
        ax.plot(self.segment_A_range, self.segment_A_altitude, '-b', linewidth=2)
        ax.plot(self.segment_B_range, self.segment_B_altitude, '-b', linewidth=2)
        ax.plot(self.segment_C_range, self.segment_C_altitude, '-b', linewidth=2)
        ax.plot(self.segment_D_range, self.segment_D_altitude, '-b', linewidth=2)
        ax.plot(self.segment_E_range, self.segment_E_altitude, '-b', linewidth=2)
        ax.grid()
        plt.show()
        
    def FlightTime(self):
        time_takeoff = 3.048 / 0.1016 # in seconds
        time_climb = self.altitude_cr / self.ROC # in seconds
        time_cruise = (self.tripDistance - self.dx) / self.velocity_cr
        time_descend = time_climb
        time_land = time_takeoff
        
        timeFlight = (time_takeoff + time_climb + time_cruise + time_descend + time_land) / 60 # in minutes
        print(f"Cruise Altitude: {int(self.altitude_cr)} meters , Flight Time: {round(timeFlight,2)} minutes")
        return timeFlight
    
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
        

# FP1 = FlightProfile(1500, 30)
# FP1.PlotMissionProfile()
# FP1_time = FP1.FlightTime()
# X,Y = FP1.GivenRangeOutputAltitude(2000)
# X,Y = FP1.GivenRangeOutputAltitude(20000)
# X,Y = FP1.GivenRangeOutputAltitude(45000)
# X,Y = FP1.GivenRangeOutputAltitude(30 * 1609.34)

# FP2 = FlightProfile(3000, 30)
# FP2.PlotMissionProfile()
# FP2_time = FP2.FlightTime()
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