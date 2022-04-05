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
import matplotlib.cm as cm
import matplotlib.ticker as mtick

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
        
wind_speed = [0.001, 5, 10, 10, 10]# 15, 20]
wind_direction = [0.01, 90, 179, -90]
d = 2
cruiseAlt = 1500 # cruising altitude in feet
POV = 1 # percentage of velocity

velty_Joby = 0.44704*165*POV # m/s
JobyS4 = Aircraft("Joby", 4, 165, 150, 13.8, 45, 2177, 254.4, S=10.7*1.7)
JobyS4.Characteristics()

# velty_Joby = 0.44704*175*POV # m/s
# JobyS4 = Aircraft("Joby", 7, 175, 124, 16.3, 53, 3175, 305, S=11*1.1)

# velty_Joby = 0.44704*150*POV # m/s
# JobyS4 = Aircraft("Joby", 5, 150, 60, 11.3, 24, 3175, 160, S=13*1.1)

# velty_Joby = 0.44704*56*POV 
# JobyS4 = Aircraft("Joby", 1, 56, 22, 2.5, 19, 900, 83.3, S=1**2)

# velty_Joby = 0.44704*62*POV # m/s
# JobyS4 = Aircraft("Joby", 1, 62, 22, 1.5, 21, 1322, 206.2, S=1**2)

X0, Y0, Radial0, Distance0 = JobyS4.ReachableGroundFootprint(cruiseAlt,velty_Joby, wind_speed[0], wind_direction[d])
RGF_Area_Ref_0 = Polygon(zip(X0, Y0)) # Assuming the OP's x,y coordinates
RGF_Area_Ref_0 = (RGF_Area_Ref_0.area/(1000**2)) * (0.621371**2) # in mi^2

X5, Y5, Radial5, Distance5 = JobyS4.ReachableGroundFootprint(cruiseAlt,velty_Joby, wind_speed[1], wind_direction[d])
RGF_Area_Ref_5 = Polygon(zip(X5, Y5)) # Assuming the OP's x,y coordinates
RGF_Area_Ref_5 = (RGF_Area_Ref_5.area/(1000**2)) * (0.621371**2) # in mi^2

X10, Y10, Radial10, Distance10 = JobyS4.ReachableGroundFootprint(cruiseAlt,velty_Joby, wind_speed[2], wind_direction[d])
RGF_Area_Ref_10 = Polygon(zip(X10, Y10)) # Assuming the OP's x,y coordinates
RGF_Area_Ref_10 = (RGF_Area_Ref_10.area/(1000**2)) * (0.621371**2) # in mi^2

X15, Y15, Radial15, Distance15 = JobyS4.ReachableGroundFootprint(cruiseAlt,velty_Joby, wind_speed[3], wind_direction[d])
RGF_Area_Ref_15 = Polygon(zip(X15, Y15)) # Assuming the OP's x,y coordinates
RGF_Area_Ref_15 = (RGF_Area_Ref_15.area/(1000**2)) * (0.621371**2) # in mi^2

X20, Y20, Radial20, Distance20 = JobyS4.ReachableGroundFootprint(cruiseAlt,velty_Joby, wind_speed[4], wind_direction[d])
RGF_Area_Ref_20 = Polygon(zip(X20, Y20)) # Assuming the OP's x,y coordinates
RGF_Area_Ref_20 = (RGF_Area_Ref_20.area/(1000**2)) * (0.621371**2) # in mi^2

# PLOT ALL ON THE SAME POLAR PLOT
linewidth=2
fig, ax = plt.subplots(subplot_kw=dict(polar=True), dpi=600, figsize=(9,6))
ax.plot(Radial0, Distance0*0.621371, 'k', linewidth=linewidth, label='Wind: 0 m/s | Area: '+ str(round(RGF_Area_Ref_0,2)) + ' sq. mi')
ax.plot(Radial5, Distance5*0.621371, 'b', linewidth=linewidth, label='Wind: 5 m/s | Area: '+ str(round(RGF_Area_Ref_5,2)) + ' sq. mi')
ax.plot(Radial10, Distance10*0.621371, 'r--', linewidth=linewidth,label='Wind: 10 m/s | Area: ' + str(round(RGF_Area_Ref_10,2)) + ' sq. mi')
ax.plot(Radial15, Distance15*0.621371, 'g-.', linewidth=linewidth,label='Wind: 15 m/s | Area: ' + str(round(RGF_Area_Ref_15,2)) + ' sq. mi')
ax.plot(Radial20, Distance20*0.621371, 'm.', linewidth=linewidth,label='Wind: 20 m/s | Area: ' + str(round(RGF_Area_Ref_20,2)) + ' sq. mi')
ax.set_theta_direction(-1) # CW direction 
ax.set_theta_zero_location('N')
ax.set_title("Cruising Altitude: " + str(cruiseAlt) +" feet \nReachable Ground Footprint (mi) and its Footprint Area (sq. mi) \nComparison of eVTOL Vehicles under Gliding Conditions \nCross Wind Due West Scenario")
ax.legend(loc='lower left',bbox_to_anchor=(1, 0.6))
# ax.set_rticks([0,1, 2,3,4])
ax.set_rticks([0,1, 2,3, 4,5])
# ax.set_rticks([0,1, 2,3, 4,5,6,7,8])
# ax.set_rticks([0, 2, 4, 6, 8, 10, 12, 14, 16])
# ax.set_rticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])
plt.tight_layout()
#plt.savefig('C:/Users/saimu/Documents/AAE_MS_Thesis_Documentation_v2/Python_Code/Results/Miscellaneous/Wind_Footprints/LiliumLike/NormalTurn_WestWind.png', dpi=600)
plt.show()

#######################################################################
"""
Plot the Reachable Ground Footprint Area for Various Wind Speeds (rainbow spectrum)
Where Red means high speed, Blue means low wind speed.
The direction refers to wind direction relative to north pole
E.g., 0 deg means wind is blowing directly north
"""

wind_speed = np.linspace(0.01,30,150)
wind_direction1 = np.linspace(0.01,90,50)
wind_direction2 = np.linspace(90.01, 179,50)
wind_direction3 = np.linspace(-179,-0.01,50)
wind_direction = wind_direction1 + wind_direction2 + wind_direction3

colors = cm.rainbow(np.linspace(0, 1, len(wind_speed)))

RGF_0 = 492.05 # no wind case reachable area in sq. mi
# RGF_0 = 35.4
# RGF_0 = 50.2
# RGF_0 = 7.45
RGF_0 = 23.68
RGF_0 = 1.34
RGF_0 = 0.43

fig, ax = plt.subplots(subplot_kw=dict(polar=True), dpi=600, figsize=(7,9))
for s, c in zip(wind_speed, colors):
    RGF_Area = []
    for d in wind_direction:
        X, Y, Radial, Distance = JobyS4.ReachableGroundFootprint(cruiseAlt,velty_Joby, s, d)
        RGF_Area_Ref = Polygon(zip(X, Y)) # Assuming the OP's x,y coordinates
        RGF_Area_Ref = (RGF_Area_Ref.area/(1000**2)) * (0.621371**2) # in mi^2
        RGF_Area.append(100*(RGF_Area_Ref-RGF_0)/RGF_0)
        # RGF_Area.append(RGF_Area_Ref)
    ax.plot(np.multiply(wind_direction,math.pi/180), RGF_Area, color=c, alpha=0.5)
ax.set_theta_direction(-1) # CW direction 
ax.set_theta_zero_location('N')
ax.yaxis.set_major_formatter(mtick.PercentFormatter())

ax.set_title("EHang-like Vehicle, Cruising Altitude: " + str(cruiseAlt) +" feet \n% Change in Reachable Ground Footprint Area Due to Wind\nRelative to No Wind Case Footprint Area [0.43 sq. mi] \n Wind Speed Range: 0m/s [Blue], 30m/s [Red] \n")
#plt.savefig('C:/Users/saimu/OneDrive - purdue.edu/Purdue Graduate School/MS_Aeronautical_Astronautical_Engineering/MS Thesis Research/Spring 2022/Python_Code/Results/Miscellaneous/Wind/wind_ex1.png', dpi=600)
#plt.show()        

# ###############################################################################################
# wind_speed = np.linspace(0.01,30,100)
# wind_direction1 = np.linspace(0.01,90,5)
# wind_direction2 = np.linspace(90.01, 179,5)
# wind_direction3 = np.linspace(-179,-0.01,5)
# wind_direction = wind_direction1 + wind_direction2 + wind_direction3

# colors = cm.rainbow(np.linspace(0, 1, len(wind_speed)))

# fig, ax = plt.subplots(subplot_kw=dict(polar=True), dpi=600, figsize=(7,9))
# for s, c in zip(wind_speed, colors):
#     RGF_Area = []
#     for d in wind_direction:
#         X, Y, Radial, Distance = JobyS4.ReachableGroundFootprint(cruiseAlt,velty_Joby, s, d)
#         RGF_Area_Ref = Polygon(zip(X, Y)) # Assuming the OP's x,y coordinates
#         RGF_Area_Ref = (RGF_Area_Ref.area/(1000**2)) * (0.621371**2) # in mi^2
#         RGF_Area.append(100*(RGF_Area_Ref-RGF_0)/RGF_0)
#         # RGF_Area.append(RGF_Area_Ref)
#         ax.plot(Radial, Distance, color=c, alpha=0.30)
# ax.set_theta_direction(-1) # CW direction 
# ax.set_theta_zero_location('N')

# ax.set_title("Cruising Altitude: " + str(cruiseAlt) +" feet \nReachable Ground Footprint (mi) and its Footprint Area (sq. mi) \nComparison of eVTOL Vehicles under Gliding Conditions \nAll Wind Scenarios")
# plt.savefig('C:/Users/saimu/Documents/AAE_MS_Thesis_Documentation_v2/Python_Code/Results/Miscellaneous/Wind_Footprints/JobyLike/NormalTurn_AllWindSummaryft.png', dpi=600)
# plt.show()        

