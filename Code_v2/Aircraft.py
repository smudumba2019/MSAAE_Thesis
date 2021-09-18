# -*- coding: utf-8 -*-
"""
Created on Tue May 18 15:33:44 2021

@author: Sai Mudumba
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import itertools
from shapely.geometry import Polygon

class Aircraft:
    def __init__(self, ACname, PAX, Speed_Cr, Range, LD_Ratio, Max_Flt_Time, MTOW, KWh_Batt, S):
        # Later on, this will be replaced by loading an excel sheet that automatically loads all the characteristics
        # This is written here only for ease of running the code
        self.acName = ACname
        self.pax = PAX
        self.cruiseSpeed = Speed_Cr
        self.acRange = Range
        self.LDratio = LD_Ratio
        self.maxFltTime = Max_Flt_Time
        self.MTOW = MTOW
        self.kWhBatt = KWh_Batt
        self.S = S
        self.DGlideStraight = 0
      
    def Characteristics(self):
        print(f"These are the aircraft characteristics for {self.acName}: ")
        print(f"Aircraft Name: {self.acName}")
        print(f"Passenger Capacity: {self.pax}")
        print(f"Maximum Cruise Speed (mph): {self.cruiseSpeed}")
        print(f"Range (mi): {self.acRange}")
        print(f"Lift to Drag Ratio (Cruise): {self.LDratio}")
        print(f"Endurance (minutes): {self.maxFltTime}")
        print(f"Maximum Takeoff Weight (kg): {self.MTOW}")
        print(f"Battery Capacity (kWh): {self.kWhBatt}")
        print(f"Wing Surface Area (m^2): {self.S}")
      
    def ReachableGroundFootprint(self, altitude, mu_deg, PowFailure):
        alt = altitude * 0.3048 # cruising altitude in meters
        self.rho = 1.225 # density of air in kg/m^3
        self.g = 9.81 # acceleration due to gravity in m/s^2
        g = self.g
        speed = self.cruiseSpeed # cruising speed in mph
        speed = speed * 0.44704 # converting mph to m/s 
        W = self.MTOW * 9.81
        T = (1 - (PowFailure/100)) * W
        CD0 = 0.037
        k = 0.037
        
        # Define Heading Change angles from 0 deg to 270 degrees, with a condition to stop when radial angle is 180 degrees
        PSI = np.linspace(0, 3*math.pi/2, 100)
        
        """
        For each PSI angle, find the x, y coordinates where it touches the ground
        """
        X_RHS = []
        Y_RHS = []
        Distance = []
        ETA_final = []
        
        for i, HC in enumerate(PSI):
            if HC <= math.pi/6:
                mu_rad = self.degrees2radians(10)
            elif HC <= math.pi/3:
                mu_rad = self.degrees2radians(20)
            elif HC <= math.pi/2:
                mu_rad = self.degrees2radians(30)
            elif HC <= 4*math.pi/6:
                mu_rad = self.degrees2radians(40)
            else:
                mu_rad = self.degrees2radians(45)
            # mu_rad = self.degrees2radians(mu_deg)
            
            r = self.FindTurnRadius(speed, mu_rad) # radius of the turn
            Larc = self.FindTurnRadiusArcLength(r, HC)  # given change in heading, find arc length of the turn
            L, D = self.EstimateLiftandDrag(speed, mu_rad)
            VsV = self.EstimateSinkRate(D)
            dH_turn = self.EstimateAltitudeLossDuringTurn(Larc, VsV, mu_rad)
            DGlide = (alt - dH_turn) * (self.LDratio)

            if DGlide >= 0:
                x = r * math.cos(math.pi - HC) + r
                y = r * math.sin(math.pi - HC)                    
                x = x + DGlide * math.sin(HC)
                y = y + DGlide * math.cos(HC)
                ETA_estimated = math.atan(x/y)
                if (x > 0 and y < 0) or (x < 0 and y < 0):
                    ETA_estimated = math.pi + ETA_estimated
                if ETA_estimated >= math.pi:
                    break
            elif DGlide < 0:
                hc = np.linspace(0,PSI[i-1],100)
                X_turn = []
                Y_turn = []
                TurnDistance = []
                ETA = []
                for j in hc:
                    x = r * math.cos(math.pi - j) + r
                    y = r * math.sin(math.pi - j)
                    X_turn.append(x)
                    Y_turn.append(y)
                    TurnDistance.append(math.sqrt(x ** 2 + y ** 2))
                    if x >= 0 and y >= 0:
                        if y == 0:
                            ETA.append(math.pi/2)
                        else:
                            ETA.append(math.atan(x/y))
                    elif (x > 0 and y < 0) or (x < 0 and y < 0):
                        ETA.append(math.pi + math.atan(x/y))
                    elif (x < 0 and y > 0):
                        ETA.append(2 * math.pi + math.atan(x/y))
                # print("I")
                break
            
            X_RHS.append(x)
            Y_RHS.append(y)
            Distance.append(math.sqrt(x ** 2 + y ** 2))
            ETA_final.append(ETA_estimated)    
        
        try: # if footprint is not an ellipsoid
            X_RHS, Y_RHS = self.Combine(X_turn, Y_turn, self.Reverse(X_RHS), self.Reverse(Y_RHS))
            X_LHS, Y_LHS = self.Symmetry(X_RHS,Y_RHS)
            X, Y = self.Combine(X_RHS, Y_RHS, X_LHS, Y_LHS)
                
            Distance_RHS, NullArray = self.Combine(TurnDistance, [1], self.Reverse(Distance), [1])
            Distance_LHS = Distance_RHS
            Distance, NullArray = self.Combine(Distance_RHS, [1], self.Reverse(Distance_LHS), [1])
            
            ETA_RHS, NullArray = self.Combine(ETA, [1], self.Reverse(ETA_final),[1])
            ETA_LHS = np.multiply(-1,ETA_RHS)
            ETA_LHS = self.Reverse(ETA_LHS)
            ETA_final, NullArray = self.Combine(ETA_RHS, [1], ETA_LHS, [1])
        except:
            X_LHS, Y_LHS = self.Symmetry(X_RHS,Y_RHS)
            X, Y = self.Combine(X_RHS, Y_RHS, X_LHS, Y_LHS)
            
            Distance_RHS = Distance
            Distance_LHS = Distance_RHS
            Distance, NullArray = self.Combine(Distance_RHS, [1], self.Reverse(Distance_LHS), [1])
        
            ETA_RHS = ETA_final
            ETA_LHS = np.multiply(-1,ETA_RHS)
            ETA_LHS = self.Reverse(ETA_LHS)
            ETA_final, NullArray = self.Combine(ETA_RHS, [1], ETA_LHS, [1])
        
        # self.PlotReachabilityFootprint(X, Y)
        # self.PolarPlotReachabilityFootprint(ETA_final, np.multiply(1/1000,Distance))
        
        # print(Distance)
        return (X, Y, ETA_final, np.multiply(1/1000,Distance))
        
    def FindTurnRadius(self, speed, mu):
        r = speed ** 2 / (self.g * math.tan(mu)) # radius of the turn
        return r    
    
    def FindTurnRadiusArcLength(self, r, hc):
        Larc = r * abs(hc)
        return Larc
    
    def EstimateLiftandDrag(self, speed, mu):
        CL = 2 * (self.MTOW * self.g) / (self.rho * self.S * speed ** 2)
        CD = CL/self.LDratio # Find CD from L/D ratio
        L = 0.5 * self.rho * speed ** 2 * self.S * CL * math.cos(mu)
        D = 0.5 * self.rho * speed**2 * self.S * CD
        return (L, D)
    
    def EstimateSinkRate(self, D):
        return D/(self.MTOW*self.g)
    
    def EstimateAltitudeLossDuringTurn(self, Larc, VsV, mu):
        dH_turn = Larc * VsV / math.cos(mu) # height loss
        return dH_turn
    
    def Symmetry(self,X_RHS,Y_RHS):
        X_LHS = np.multiply(-1,X_RHS)
        Y_LHS = Y_RHS
        
        X_LHS = self.Reverse(X_LHS) #reversing using list slicing
        Y_LHS = self.Reverse(Y_LHS) #reversing using list slicing
        return (X_LHS, Y_LHS)
    
    def Reverse(self, x):
        x = x[::-1]
        return x
    
    def Combine(self, xr, yr, xl, yl):
        x = list(itertools.chain(xr,xl))
        y = list(itertools.chain(yr,yl))
        return (x, y)
    
    def PlotReachabilityFootprint(self, X, Y):
        fig, ax = plt.subplots(figsize=(8,5), dpi=300)
        ax.plot(X, Y)
        plt.show()
    
    def PolarPlotReachabilityFootprint(self, teta, r):
        fig, ax = plt.subplots(subplot_kw=dict(polar=True), dpi=300)
        ax.plot(teta, r)
        ax.set_theta_direction(-1) # CW direction 
        # ax.set_theta_zero_location('N')
        plt.show() # comment this line when comparing all vehicles; uncomment when running for big code
    
    def radians2degrees(self,angle):
        try:
            angle = angle * 180 / math.pi
        except:
            for i in range(len(angle)):
                angle[i] = angle[i] * 180 / math.pi
        return angle
    
    def degrees2radians(self,angle):
        angle = angle * math.pi / 180
        return angle
        # TurnRadius = (speed ** 2) * math.cos(gamma) / (g * math.tan(mu))
    
    def EstimateGlideRateOfDescent(self):
        speed = self.cruiseSpeed # cruising speed in mph
        speed = speed * 0.44704 # converting mph to m/s
        CL = 2 * (self.MTOW * self.g) / (self.rho * self.S * speed ** 2)
        ROD_glide = math.sqrt((self.MTOW * self.g) / (0.5 * self.rho * self.S * CL)) * (1/self.LDratio)
        return ROD_glide
    
    def EstimateAltitudeDropInGlide(self,altitude, startle_delay):
        altitude = 0.3048 * altitude # feet to meters
        ROD_glide = self.EstimateGlideRateOfDescent()
        final_altitude = altitude - (startle_delay * ROD_glide)
        final_altitude = 3.28084 * final_altitude # meters to feet
        return (final_altitude)

        
# JobyS4 = Aircraft("Joby", 4, 200, 150, 13.8, 45, 2177, 254.4, S=10.7*1.7)
# JobyS4.Characteristics()
# """
# Determine the Reachable Footprint and Estimate its Footprint Area
# """
# X, Y, ETA, DistanceRadial = JobyS4.ReachableGroundFootprint(1500,35,0)
# RGF_Area_Ref = Polygon(zip(X, Y)) # Assuming the OP's x,y coordinates
# RGF_Area_Ref = RGF_Area_Ref.area/(1000**2) # in km^2
# print(f"The Reachable Ground Footprint (RGF) Area for 1500 ft cruising altitude is: {RGF_Area_Ref} km^2")
# plt.plot(X,Y)
# plt.show()
# """
# Estimate the altitude loss in the case of a delayed response to emergency power failure case.
# """
# AltitudeLoss = []
# Loss_RGF_Area = []
# PercentLoss_RGF_Area = []
# timeDelay = range(0,10,1)

# for t in timeDelay:
#     AltitudeDrop = JobyS4.EstimateAltitudeDropInGlide(1500,t)
#     AltitudeLoss.append(AltitudeDrop - 1500)
    
#     X, Y, ETA, DistanceRadial = JobyS4.ReachableGroundFootprint(AltitudeDrop,35,0)
#     RGF_Area = Polygon(zip(X, Y)) # Assuming the OP's x,y coordinates
#     RGF_Area = RGF_Area.area/(1000**2)
#     Loss_RGF_Area.append(RGF_Area)
    
#     Percent_Loss_Of_RGB_Area = -100 * (RGF_Area - RGF_Area_Ref) / RGF_Area_Ref
#     PercentLoss_RGF_Area.append(Percent_Loss_Of_RGB_Area)    
    
#     # plt.plot(X,Y)
#     # plt.show()
    
# plt.plot(timeDelay, PercentLoss_RGF_Area)
# plt.show()

# plt.plot(timeDelay, Loss_RGF_Area)
# plt.show()

# print(AltitudeLoss)
# print(PercentLoss_RGF_Area)

# Lilium7 = Aircraft("Joby", 7, 186, 186, 16.3, 60, 1700, 187.8, S=10.7*1.7)
# Lilium7.Characteristics()
# Lilium7.ReachableGroundFootprint(1500,35,0)

# Archer5 = Aircraft("Joby", 5, 175, 60, 11.3, 24, 3175, 160, S=10.7*1.7)
# Archer5.Characteristics()
# Archer5.ReachableGroundFootprint(1500,35,0)

# Volocopter1 = Aircraft("Joby", 1, 56, 22, 2.5, 19, 900, 83.3, S=10.7*1.7)
# Volocopter1.Characteristics()
# Volocopter1.ReachableGroundFootprint(1500,35,0)

# EHang1 = Aircraft("Joby", 1, 62, 22, 1.5, 21, 1322, 206.2, S=10.7*1.7)
# EHang1.Characteristics()
# EHang1.ReachableGroundFootprint(1500,35,0)
# plt.show()