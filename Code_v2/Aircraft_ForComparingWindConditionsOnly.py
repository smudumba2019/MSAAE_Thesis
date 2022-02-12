# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 17:26:34 2022

@author: saimu
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
      
    def ReachableGroundFootprint(self, altitude, speed, wind_speed, wind_direction):
        alt = altitude * 0.3048 # cruising altitude in meters
        self.rho = 1.225 # density of air in kg/m^3
        self.g = 9.81 # acceleration due to gravity in m/s^2
        g = self.g
        speed = speed # in m/s # self.cruiseSpeed # cruising speed in mph
        # speed = speed * 0.44704 # converting mph to m/s 
        W = self.MTOW * 9.81
        # T = (1 - (PowFailure/100)) * W
        CD0 = 0.037
        k = 0.037
        
        # Define Heading Change angles from 0 deg to 270 degrees, with a condition to stop when radial angle is 180 degrees
        # Note: this is only finding reachable footprint for half the circle; the other half is symmetric
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
            # mu_rad = self.degrees2radians(5)
            
            r = self.FindTurnRadius(speed, mu_rad) # radius of the turn
            Larc = self.FindTurnRadiusArcLength(r, HC)  # given change in heading, find arc length of the turn
            L, D = self.EstimateLiftandDrag(speed, mu_rad)
            VsV = self.EstimateSinkRate(D)
            dH_turn = self.EstimateAltitudeLossDuringTurn(Larc, VsV, mu_rad)
            DGlide = (alt - dH_turn) * (self.LDratio)
            self.VsV = VsV
            
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
        
        X_wind, Y_wind = self.WindAnalysis(alt, speed, X, Y, wind_speed, wind_direction) # altitude, groundspeed, X, Y, wind speed, wind direction to North Pole
        
        Distance_wind = [math.sqrt(X_wind[i] ** 2 + Y_wind[i] ** 2) for i in range(len(X_wind))]
        
        return (X_wind, Y_wind, ETA_final, np.multiply(1/1000,Distance_wind))
        
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
        # print(L/D)
        return (L, D)
    
    def EstimateSinkRate(self, D):
        return math.sin(math.atan(1/self.LDratio))#D/(self.MTOW*self.g)
    
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

    def WindAnalysis(self, altitude, speed, X, Y, wind_speed, wind_direction):
        Gmma = [] # the angle of the X, Y to the origin without wind
        Vx_groundspeed = []
        Vy_groundspeed = []
        
        for i in range(len(X)):
            # take care of divide 0 warning
            if X[i] != 0:
                gma_rad = math.atan(Y[i]/X[i])
            elif Y[i] > 0 and X[i] == 0:
                gma_rad = math.pi/2
            elif Y[i] < 0 and X[i] == 0:
                gma_rad = -math.pi/2
            else:
                gma_rad = 0
            
            # assign angles correctly based on the quadrant it is in
            if Y[i] < 0 and X[i] < 0:
                gma_rad = gma_rad - math.pi
            elif Y[i] > 0 and X[i] < 0:
                gma_rad = (gma_rad - math.pi)
                
            gma_deg = self.radians2degrees(gma_rad)
            Gmma.append(gma_rad)    
        
            Vx = speed * math.cos(gma_rad)
            Vy = speed * math.sin(gma_rad)
            
            Vx_groundspeed.append(Vx)
            Vy_groundspeed.append(Vy)
        
        Gmma[-1] = -3*math.pi/2
        
        wind_speed = wind_speed # wind speed in m/s
        wind_direction = math.pi/2 - self.degrees2radians(wind_direction) # radians
        wind_dir_xAxis = wind_speed*math.cos(wind_direction)
        wind_dir_yAxis = wind_speed*math.sin(wind_direction)
        
        Vx_air = [vx + wind_dir_xAxis for vx in Vx_groundspeed]        
        Vy_air = [vy + wind_dir_yAxis for vy in Vy_groundspeed]
        
        V_air_mag = [math.sqrt(Vx_air[i]**2 + Vy_air[i]**2) for i in range(len(Vx_air))]
        
        R_ground = [math.sqrt(X[i]**2 + Y[i]**2) for i in range(len(X))]
        R_airspeed = [R_ground[i] * (V_air_mag[i] / speed) for i in range(len(X))]
        
        # find the angle between v ground speed and w wind speed
        # law of cosines
        
        Angle_VW = [math.acos(-(V_air_mag[i]**2 - (speed**2 + wind_speed**2)) / (2*speed*wind_speed)) for i in range(len(X))]
        Angle_Alt = [math.acos(-(wind_speed**2 - (speed**2 + V_air_mag[i]**2)) / (2*speed*V_air_mag[i])) for i in range(len(X))]
        
        delTA = []
        for i in range(len(X)):
            if Angle_VW[i] > Gmma[i]:
                DelTa = Gmma[i] - Angle_Alt[i]
            elif Angle_VW[i] < Gmma[i]:
                DelTa = Gmma[i] + Angle_Alt[i]
            else:
                DelTa = Gmma[i]
            
            delTA.append(DelTa)
        
        # another version
        X_new = [X[i] + X[i]*((Vx_air[i] - Vx_groundspeed[i])/Vx_groundspeed[i]) for i in range(len(X))]
        Y_new = [Y[i] + Y[i]*((Vy_air[i] - Vy_groundspeed[i])/Vy_groundspeed[i]) for i in range(len(Y))]
        
        return (X_new,Y_new)
        
wind_speed = [5, 10, 15, 20]
wind_direction = [0.01, 90, 179, -90]

cruiseAlt = 1500 # cruising altitude in feet
POV = 1 # percentage of velocity
velty_Joby = 0.44704*165*POV # m/s
JobyS4 = Aircraft("Joby", 4, 165, 150, 13.8, 45, 2177, 254.4, S=10.7*1.7)
JobyS4.Characteristics()

for d in wind_direction:
    for s in wind_speed:
        X_JobyS4, Y_JobyS4, Radial_JobyS4, Distance_JobyS4 = JobyS4.ReachableGroundFootprint(cruiseAlt,velty_Joby, s, d)
        RGF_Area_Ref_JobyS4 = Polygon(zip(X_JobyS4, Y_JobyS4)) # Assuming the OP's x,y coordinates
        RGF_Area_Ref_JobyS4 = (RGF_Area_Ref_JobyS4.area/(1000**2)) * (0.621371**2) # in mi^2
        linewidth=2.5
        fig, ax = plt.subplots(subplot_kw=dict(polar=True), dpi=600, figsize=(8,6))
        plt.plot(Radial_JobyS4, Distance_JobyS4*0.621371, 'b', linewidth=linewidth, label='Joby-like: '+ str(round(RGF_Area_Ref_JobyS4,2)) + ' sq. mi')
        ax.set_theta_direction(-1) # CW direction 
        ax.set_theta_zero_location('N')
        ax.set_title("Cruising Altitude: " + str(cruiseAlt) +" feet \nReachable Ground Footprint (mi) and its Footprint Area (sq. mi) \nComparison of eVTOL Vehicles under Gliding Conditions")
        ax.legend(loc='lower left',bbox_to_anchor=(1, 0.6))
        ax.set_rticks([0,1, 2,3, 4,5])
    plt.tight_layout()
    plt.show()

# PLOT ALL ON THE SAME POLAR PLOT
linewidth=2.5
fig, ax = plt.subplots(subplot_kw=dict(polar=True), dpi=600, figsize=(8,6))
ax.plot(Radial_JobyS4, Distance_JobyS4*0.621371, 'b', linewidth=linewidth, label='Joby-like: '+ str(round(RGF_Area_Ref_JobyS4,2)) + ' sq. mi')
ax.plot(Radial_Lilium7, Distance_Lilium7*0.621371, 'r', linewidth=linewidth,label='Lilium-like: ' + str(round(RGF_Area_Ref_Lilium7,2)) + ' sq. mi')
ax.plot(Radial_Archer5, Distance_Archer5*0.621371, 'g', linewidth=linewidth,label='Archer-like: ' + str(round(RGF_Area_Ref_Archer,2)) + ' sq. mi')
ax.plot(Radial_Volocopter1, Distance_Volocopter1*0.621371, 'm', linewidth=linewidth,label='VoloCity-like: ' + str(round(RGF_Area_Ref_Volo,2)) + ' sq. mi')
ax.plot(Radial_EHang1, Distance_EHang1*0.621371, 'k', linewidth=linewidth,label='EHang-like: '+ str(round(RGF_Area_Ref_Ehang,2)) + ' sq. mi')
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
plt.savefig('C:/Users/saimu/Documents/AAE_MS_Thesis_Documentation_v2/Python_Code/Results/Miscellaneous/ComparisonOfReachableFootprint1500FT_NormalTurn_Wind_20.png', dpi=600)
plt.show()