# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 12:29:34 2021

@author: Sai Mudumba
"""
from Aircraft import *

cruiseAltitude = 1500 # in feet - where does the 100% power failure happen?
simTime = 7 # seconds - how long do we want to simulate?

def StartleResponseAnalysis(AC, cruiseAltitude, velty):
    """
    Goal: The objective of this function is to analyze how a delay in responding to a 100% power failure case for an eVTOL aircraft decreases the reachable ground footprint area of the aircraft

    Parameters
    ----------
    AC : TYPE : Object
        DESCRIPTION: AC is short for Aircraft. It is an object that contains aircraft specifications
    cruiseAltitude : TYPE : Positive Real Number (Float)
        DESCRIPTION: cruiseAltitude (ft) is the cruising altitude at which aircraft experiences 100% power failure conditions and glides at a steady-state
    velty : TYPE : Positive Real Number (Float)
        DESCRIPTION: velty is short for velocity (m/s)
    Returns
    -------
    timeDelay : TYPE : a list
        DESCRIPTION: time delay (seconds) in response to 100% power failure condition
    AltitudeLoss : TYPE : a list
        DESCRIPTION: altitude loss (ft) for each time delay for 100% power failure condition
    Loss_RGF_Area : TYPE : a list
        DESCRIPTION: loss of reachable ground footprint area for each time delay for 100% power failure condition
    PercentLoss_RGF_Area : TYPE : a list
        DESCRIPTION: percentage loss of reachable ground footprint area to the 0-sec time delay area for each time delay for 100% power failure condition

    """
    
    # Determine the Reachable Ground Footprint and Estimate its Footprint Area
    X, Y, ETA, DistanceRadial = AC.ReachableGroundFootprint(cruiseAltitude,velty,35,0) # X, Y are in meters, ETA and DistanceRadial are the equivalent polar coordinates angle and radius
    RGF_Area_Ref = Polygon(zip(X, Y)) # Assuming the OP's x,y coordinates
    RGF_Area_Ref = RGF_Area_Ref.area/(1000**2) * (0.621371**2)# in mi^2
    print(f"The Reachable Ground Footprint (RGF) Area for {cruiseAltitude} ft cruising altitude is: {RGF_Area_Ref} mi^2")
    
    # Estimate the altitude loss in the case of a delayed response to a 100% power failure emergency scenario.
    AltitudeLoss = [] # initialize the list where we keep track of altitude loss (ft) for each delay in response time (sec)
    Loss_RGF_Area = [] # initialize the list where we keep track of the reachable ground footprint area (km^2) for each delay in response time (sec)
    PercentLoss_RGF_Area = [] # initialize the list where we keep track of the percentage loss of the reachable ground footprint area (%) for each delay in response time (sec)
    timeDelay = range(0,simTime,1) # initialize the response time delay (sec)
    
    # For each response time delay, find the altitude drop, loss of reachable ground footprint, and its percentage loss during that delay
    for t in timeDelay:
        AltitudeDrop = AC.EstimateAltitudeDropInGlide(cruiseAltitude,t) # the altitude (ft) after the response time delay (sec)
        if AltitudeDrop <= 0:
            AltitudeDrop = 0
        AltitudeLoss.append(AltitudeDrop - cruiseAltitude) # altitude loss (ft) duing the response time delay (sec)
        
        # find the reachable ground footprint and its area at the altitude drop, and subsequently its area (km^2)
        X, Y, ETA, DistanceRadial = AC.ReachableGroundFootprint(AltitudeDrop,velty,35,0)
        RGF_Area = Polygon(zip(X, Y)) # Assuming the OP's x,y coordinates
        RGF_Area = RGF_Area.area/(1000**2) * (0.621371**2)
        Loss_RGF_Area.append(RGF_Area)
        
        Percent_Loss_Of_RGB_Area = -100 * (RGF_Area - RGF_Area_Ref) / RGF_Area_Ref
        PercentLoss_RGF_Area.append(Percent_Loss_Of_RGB_Area)    
    
    return timeDelay, AltitudeLoss, Loss_RGF_Area, PercentLoss_RGF_Area

"""
DEFINING VEHICLE AND INITIALIZING STARTLING RESPONSE ANALYSIS
"""
POV = 1

JobyS4 = Aircraft("Joby", 4, 200, 150, 13.8, 45, 2177, 254.4, S=10.7*1.7)
velty_Joby = 74*POV # m/s
timeDelay_JobyS4, AltitudeLoss_JobyS4, Loss_RGF_Area_JobyS4, PercentLoss_RGF_Area_JobyS4 = StartleResponseAnalysis(JobyS4, cruiseAltitude, velty_Joby)

Lilium7 = Aircraft("Lilium", 7, 186, 186, 16.3, 60, 1700, 187.8, S=10.7*1.7)
velty_Lilium = 78*POV # m/s
timeDelay_Lilium7, AltitudeLoss_Lilium7, Loss_RGF_Area_Lilium7, PercentLoss_RGF_Area_Lilium7 = StartleResponseAnalysis(Lilium7, cruiseAltitude, velty_Lilium)

Archer5 = Aircraft("Archer", 5, 175, 60, 11.3, 24, 3175, 160, S=10.7*1.7)
velty_Archer = 67*POV # m/s
timeDelay_Archer5, AltitudeLoss_Archer5, Loss_RGF_Area_Archer5, PercentLoss_RGF_Area_Archer5 = StartleResponseAnalysis(Archer5, cruiseAltitude, velty_Archer)

Volocopter1 = Aircraft("Volocopter", 1, 70.6, 22, 2.5, 19, 900, 83.3, S=1.7*1.7)
velty_Volo = 25*POV # m/s
timeDelay_Volocopter1, AltitudeLoss_Volocopter1, Loss_RGF_Area_Volocopter1, PercentLoss_RGF_Area_Volocopter1 = StartleResponseAnalysis(Volocopter1, cruiseAltitude, velty_Volo)

EHang1 = Aircraft("Joby", 1, 62, 22, 1.5, 21, 1322, 206.2, S=10.7*1.7)
velty_Ehang = 28*POV # m/s
timeDelay_EHang1, AltitudeLoss_EHang1, Loss_RGF_Area_EHang1, PercentLoss_RGF_Area_EHang1 = StartleResponseAnalysis(EHang1, cruiseAltitude, velty_Ehang)



"""
PLOTTING
"""
# Figure 1
fig, ax = plt.subplots(2, 1, figsize=(8,8), dpi=300)
ax[1].plot(timeDelay_JobyS4, PercentLoss_RGF_Area_JobyS4, linewidth='3',color='blue',label='Joby S4')
ax[1].plot(timeDelay_Lilium7, PercentLoss_RGF_Area_Lilium7, linewidth='3',color='red',label='Lilium S7')
ax[1].plot(timeDelay_Archer5, PercentLoss_RGF_Area_Archer5, linewidth='3',color='green',label='Archer S5')
ax[1].plot(timeDelay_Volocopter1, PercentLoss_RGF_Area_Volocopter1, linewidth='3',color='magenta',label='Volocopter S1')
ax[1].plot(timeDelay_EHang1, PercentLoss_RGF_Area_EHang1, linewidth='3',color='black',label='EHang S1')
ax[1].set_title(f"Cruise Altitude = {cruiseAltitude} feet (Gliding during Power Failure) \n Percentage Loss of Reachable Ground Footprint (RGF) with Response Time Delay")
ax[1].set_xlabel('Response Time Delay (seconds)')
ax[1].set_xticks(np.arange(0,simTime,1))
ax[1].set_ylabel('% Loss of Reachable Ground Footprint Area')
ax[1].grid(which='major', linestyle='-', linewidth='0.25', color='black')
ax[1].set_ylim([0, 55])


ax[0].plot(timeDelay_JobyS4, Loss_RGF_Area_JobyS4, linestyle="-", linewidth='3',color='blue',label='Joby S4')
ax[0].plot(timeDelay_Lilium7, Loss_RGF_Area_Lilium7, linestyle="-", linewidth='3',color='red',label='Lilium S7')
ax[0].plot(timeDelay_Archer5, Loss_RGF_Area_Archer5, linestyle="-", linewidth='3',color='green',label='Archer S5')
ax[0].plot(timeDelay_Volocopter1, Loss_RGF_Area_Volocopter1, linestyle="-", linewidth='3',color='magenta',label='Volocopter S1')
ax[0].plot(timeDelay_EHang1, Loss_RGF_Area_EHang1, linestyle="-", linewidth='3',color='black',label='EHang S1')
ax[0].set_xlabel('Response Time Delay (seconds)')
ax[0].set_xticks(np.arange(0,simTime,1))
ax[0].set_yticks(np.arange(0,110,10))
ax[0].set_ylabel('Reachable Ground Footprint Area (sq. km)')
ax[0].set_title(f"Cruise Altitude = {cruiseAltitude} feet (Gliding during Power Failure) \n Decrease in Reachable Ground Footprint (RGF) Area with Response Time Delay")
ax[0].grid(which='major', linestyle='-', linewidth='0.25', color='black')
ax[0].set_ylim([0, 100])

fig.tight_layout(pad=3.0) # increases spacing between subplots so graph titles don't overlap
ax[0].legend()
ax[1].legend()
plt.savefig('C:/Users/saimu/Documents/AAE_MS_Thesis_Documentation_v2/Python_Code/Results/Miscellaneous/StartleResponseAnalysis_AreaLoss1500ft.png', dpi=600)
plt.show()

# Figure 2
fig, ax = plt.subplots(1, 1, figsize=(4,6), dpi=300)
ax.plot(timeDelay_JobyS4, [AltitudeLoss_JobyS4 + cruiseAltitude for AltitudeLoss_JobyS4 in AltitudeLoss_JobyS4], linewidth='3',color='blue',label='Joby S4')
ax.plot(timeDelay_JobyS4, [AltitudeLoss_Lilium7 + cruiseAltitude for AltitudeLoss_Lilium7 in AltitudeLoss_Lilium7], linewidth='3',color='red',label='Lilium S7')
ax.plot(timeDelay_JobyS4, [AltitudeLoss_Archer5 + cruiseAltitude for AltitudeLoss_Archer5 in AltitudeLoss_Archer5], linewidth='3',color='green',label='Archer S5')
ax.plot(timeDelay_JobyS4, [AltitudeLoss_Volocopter1 + cruiseAltitude for AltitudeLoss_Volocopter1 in AltitudeLoss_Volocopter1], linewidth='3',color='magenta',label='Volocopter S1')
ax.plot(timeDelay_JobyS4, [AltitudeLoss_EHang1 + cruiseAltitude for AltitudeLoss_EHang1 in AltitudeLoss_EHang1], linewidth='3',color='black',label='EHang S1')
ax.set_title(f"Cruise Altitude = {cruiseAltitude} feet (Gliding during Power Failure) \n Altitude Loss with Response Time Delay")
ax.set_xlabel('Response Time Delay (seconds)')
ax.set_xticks(np.arange(0, simTime, 5))
ax.set_ylabel('Altitude Loss (ft)')
ax.set_yticks(np.arange(0, cruiseAltitude+200, 100))
ax.grid(which='major', linestyle='-', linewidth='0.25', color='black')
plt.show()

# Figure 3
fig, ax = plt.subplots(1, 1, figsize=(6,4), dpi=300)
ax.plot(timeDelay_JobyS4, AltitudeLoss_JobyS4, linewidth='3',color='blue',label='Joby S4')
ax.plot(timeDelay_JobyS4, AltitudeLoss_Lilium7, linewidth='3',color='red',label='Lilium S7')
ax.plot(timeDelay_JobyS4, AltitudeLoss_Archer5, linewidth='3',color='green',label='Archer S5')
ax.plot(timeDelay_JobyS4, AltitudeLoss_Volocopter1, linewidth='3',color='magenta',label='Volocopter S1')
ax.plot(timeDelay_JobyS4, AltitudeLoss_EHang1, linewidth='3',color='black',label='EHang S1')
ax.set_title(f"Cruise Altitude = {cruiseAltitude} feet (Gliding during Power Failure) \n Altitude Loss with Response Time Delay")
ax.set_xlabel('Response Time Delay (seconds)')
ax.set_xticks(np.arange(0, simTime, 1))
ax.set_ylabel('Altitude Loss (ft)')
ax.set_yticks(np.arange(-500, 200, 50))
ax.grid(which='major', linestyle='-', linewidth='0.25', color='black')
ax.legend()
plt.savefig('C:/Users/saimu/Documents/AAE_MS_Thesis_Documentation_v2/Python_Code/Results/Miscellaneous/StartleResponseAnalysis_AltitudeLoss1500ft.png', dpi=600)
plt.show()
