# -*- coding: utf-8 -*-
"""
Created on Tue May 18 15:33:44 2021

@author: Sai Mudumba
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import itertools

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
        print(f"Wing Surface Area (m^3): {self.S}")
      
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
                        ETA.append(math.atan(x/y))
                    elif (x > 0 and y < 0) or (x < 0 and y < 0):
                        ETA.append(math.pi + math.atan(x/y))
                    elif (x < 0 and y > 0):
                        ETA.append(2 * math.pi + math.atan(x/y))
                print("I")
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
        
        self.PlotReachabilityFootprint(X, Y)
        self.PolarPlotReachabilityFootprint(ETA_final, np.multiply(1/1000,Distance))
        
        # print(Distance)
        return (X, Y, ETA_final, np.multiply(0.621371/1000,Distance))
        
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
        ax.set_theta_zero_location('N')
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
        

        
JobyS4 = Aircraft("Joby", 4, 200, 150, 13.8, 45, 2177, 254.4, S=10.7*1.7)
JobyS4.Characteristics()
X_JobyS4, Y_JobyS4, Radial_JobyS4, Distance_JobyS4 = JobyS4.ReachableGroundFootprint(1500,35,0)

Lilium7 = Aircraft("Joby", 7, 175, 124, 16.3, 53, 3175, 305, S=11*1.1)
Lilium7.Characteristics()
X_Lilium7, Y_Lilium7, Radial_Lilium7, Distance_Lilium7 = Lilium7.ReachableGroundFootprint(1500,35,0)

Archer5 = Aircraft("Joby", 5, 150, 60, 11.3, 24, 3175, 160, S=13*1.1)
Archer5.Characteristics()
X_Archer5, Y_Archer5, Radial_Archer5, Distance_Archer5 = Archer5.ReachableGroundFootprint(1500,35,0)

Volocopter1 = Aircraft("Joby", 1, 56, 22, 2.5, 19, 900, 83.3, S=1**2)
Volocopter1.Characteristics()
X_Volocopter1, Y_Volocopter1, Radial_Volocopter1, Distance_Volocopter1 = Volocopter1.ReachableGroundFootprint(1500,35,0)

EHang1 = Aircraft("Joby", 1, 62, 22, 1.5, 21, 1322, 206.2, S=1**2)
EHang1.Characteristics()
X_EHang1, Y_EHang1, Radial_EHang1, Distance_EHang1 = EHang1.ReachableGroundFootprint(1500,35,0)

# PLOT ALL ON THE SAME POLAR PLOT
linewidth=2
fig, ax = plt.subplots(subplot_kw=dict(polar=True), dpi=300, figsize=(6,6))
ax.plot(Radial_JobyS4, Distance_JobyS4, 'b', linewidth=linewidth, label='Joby-like S4')
ax.plot(Radial_Lilium7, Distance_Lilium7, 'r', linewidth=linewidth,label='Lilium-like S7')
ax.plot(Radial_Archer5, Distance_Archer5, 'g', linewidth=linewidth,label='Archer-like S5')
ax.plot(Radial_Volocopter1, Distance_Volocopter1, 'm', linewidth=linewidth,label='Volocopter-like S1')
ax.plot(Radial_EHang1, Distance_EHang1, 'k', linewidth=linewidth,label='EHang-like S1')
ax.set_theta_direction(-1) # CW direction 
ax.set_theta_zero_location('N')
ax.set_title("Comparison of Reachable Ground Footprint (miles) \n of eVTOL Vehicles under Gliding Conditions")
ax.legend(loc='lower left',bbox_to_anchor=(1, 0.6))
ax.set_rticks([0,1, 2,3, 4,5])
plt.tight_layout()
plt.savefig('C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Images/ComparisonOfReachableFootprint.png', dpi=300)
plt.show()