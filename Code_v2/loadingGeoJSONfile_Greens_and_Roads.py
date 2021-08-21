# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 11:21:09 2021

@author: Sai Mudumba
"""

# https://gis.stackexchange.com/questions/90326/how-to-plot-geojson-using-python


path = "C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Code_v2/RiskMapGeneration/chicago_total.geojson"

import json
from shapely.geometry import mapping, shape
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.geometry import LineString
import pandas as pd
from descartes.patch import PolygonPatch

import matplotlib.pyplot as plt
from matplotlib import pyplot
# from figures import BLUE, SIZE, set_limits, plot_coords, color_isvalid

import geopandas as gpd

with open(path, encoding="utf-8") as f:
    data = json.load(f)
    

#https://shapely.readthedocs.io/en/stable/manual.html
#https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
def PlotLineString(fig, ax, ObjCoords, color, linewidth = 2, opacity = 1):
    line = LineString(ObjCoords)
    lon, lat = line.xy
    ax.plot(lon, lat, '-', color=color, linewidth=linewidth, alpha=opacity)

def PlotMultiplePolygon(fig, ax, ObjCoords, color, opacity = 0.5):
    c = ObjCoords[0][0]
    multi2 = MultiPolygon([[c, []]])
    # plot_coords(ax, multi2.exterior)
    patch = PolygonPatch(multi2,facecolor=color, edgecolor=color, alpha=opacity)
    # print(multi2.area, ObjCoords)
    ax.add_patch(patch)

# def PlotPoints(fig, ax, ObjCoords, color):
#     ax.plot(ObjCoords,'o',color=color)
#     print(ObjCoords)
#https://wiki.openstreetmap.org/wiki/Map_features#Natural

    
ObjectCoords = []
ObjectType = []
ObjectColor = []
ObjectClassification = []

ObjectCoords_GolfCourses = []
ObjectType_GolfCourses = []
ObjectColor_GolfCourses = []
ObjectClassification_GolfCourses = []


fig, ax = plt.subplots(figsize=(1*10,10),dpi=300)
for feature in data['features']:
    ObjCoords = feature['geometry']['coordinates']
    ObjectCoords.append(ObjCoords)
    
    ObjType = feature['geometry']['type']
    ObjectType.append(ObjType)
    
    ObjClassification = feature['properties']
    
    Natural_WaterRelated = ("basin","salt_pond","reservoir","water","wetland","glacier","bay","strait","cape","beach","coastline","reef","spring","hot_spring","geyser","blowhole")
    Natural_LandFeaturesA = ("wood","tree_row","tree","scrub","heath","moor","fell","bare_rock","scree","shingle","sand","mud")
    Natural_LandFeaturesB = ("grassland")

    Leisure_FacilitiesA = ("common","golf_course","dog_park","garden","horse_riding","nature_reserve","park","pitch","sports_centre","stadium","track")    
    Leisure_FacilitiesB = ("firepit","fishing","ice_rink","marina","picnic_table","playground","slipway","summer_camp","water_park")    

    HighwayTypesA = ("residential","footway","living_street")
    HighwayTypesB = ("secondary","tertiary","primary","motorway","motorway_link")
    BuildingsAccommodation = ("yes","apartments","bungalow", "cabin", "detached", "dormitory", "farm", "ger", "hotel", "house", "houseboat", "residential", "semidetached_house", "static_caravan", "terrace")
    BuildingsCommercial = ("railway","construction","parking","commercial","industrial", "kiosk", "office", "retail", "supermarket", "warehouse","garage")
    ManMade = ("adit","beacon","breakwater","bridge","bunker_silo","carpet_hanger","chimney","communications_tower","crane","cross","cutline","clearcut","dovecote","dyke","embankment","flagpole","gasometer","goods_conveyor","groyne","guard_stone","kiln","lighthouse","mast","mineshaft","monitoring_station","obelisk","observatory","offshore_platform","petroleum_well","pier","pipeline","pump","pumping_station","reservoir_covered","silo","snow_fence","snow_net","storage_tank","street_cabinet","stupa","surveillance","survey_point","tailings_pond","telescope","tower","wastewater_plant","watermill","water_tower","water_well","water_tap","water_works","wildlife_crossing","windmill","works","yes")    
    
    LandUseA = ("farmland","farmyard","meadow","vineyard","grass","greenfield","recreation_ground")
    LandUseB = ("forest")
    
    Aerodrome = ("runway","taxiway")
    
    Power = ("minor_line","line","tower")
    Amenities = ("parking","p")
    
    if ObjType == "MultiPolygon":            
        if "leisure" in ObjClassification: # if "leisure" is a tag in properties, do this
            DoesItContain_LeisureFacilitiesA = [ObjClassification["leisure"] == i for i in Leisure_FacilitiesA]    
            DoesItContain_LeisureFacilitiesB = [ObjClassification["leisure"] == i for i in Leisure_FacilitiesB]    
            if True in DoesItContain_LeisureFacilitiesA:
                color = "green"
                opacity = 1
                if ObjClassification["leisure"] == "golf_course":
                    ObjectCoords_GolfCourses.append(ObjCoords)
                    ObjectType_GolfCourses.append(ObjType)
                    ObjectColor_GolfCourses.append(color)
                    ObjectClassification_GolfCourses.append(ObjClassification)
                    
            elif True in DoesItContain_LeisureFacilitiesB:
                color = "limegreen"
                opacity = 1
            else:
                color = "limegreen"
                opacity = 1
        elif "landuse" in ObjClassification: # if "leisure" is a tag in properties, do this
            DoesItContain_LandUseA = [ObjClassification["landuse"] == i for i in LandUseA]    
            DoesItContain_LandUseB = [ObjClassification["landuse"] == i for i in LandUseB]    
            if True in DoesItContain_LandUseA:
                color = "limegreen"
                opacity = 1
            elif True in DoesItContain_LandUseB:
                color = "black"
                opacity = 1
            else:
                color = "black"
                opacity = 0
        elif "natural" in ObjClassification: # if "natural" is a tag in properties, do this
            DoesItContainNatural_WaterRelated = [ObjClassification["natural"] == i for i in Natural_WaterRelated]    
            DoesItContain_Natural_LandFeaturesA = [ObjClassification["natural"] == i for i in Natural_LandFeaturesA]
            DoesItContain_Natural_LandFeaturesB = [ObjClassification["natural"] == i for i in Natural_LandFeaturesB]
            if True in DoesItContain_Natural_LandFeaturesA:
                color = "brown"
                opacity = 1
            elif True in DoesItContain_Natural_LandFeaturesB:
                color = "yellow"
                opacity = 1
            elif True in DoesItContainNatural_WaterRelated:
                color = "blue"
                opacity = 1
            else:
                color = "black"
                opacity = 1
        elif "power" in ObjClassification: # if "leisure" is a tag in properties, do this
            DoesItContain_Power = [ObjClassification["power"] == i for i in Power]    
            if True in DoesItContain_Power:
                color = "red"
                opacity = 1
            else:
                color = "black"
                opacity = 0.5
        elif "aerialway" in ObjClassification: # if "leisure" is a tag in properties, do this
            DoesItContain_Aerodrome = [ObjClassification["aerialway"] == i for i in Aerodrome]    
            if True in DoesItContain_Aerodrome:
                color = "red"
                opacity = 1
            else:
                color = "black"
                opacity = 0.5
        else:
            # print(ObjClassification,ObjType)
            color = "lightyellow"
            opacity = 0
            
        PlotMultiplePolygon(fig, ax, ObjCoords, color, opacity)        

    if ObjType == "LineString":
        linewidth = 3
        opacity = 1
        if "highway" in ObjClassification:
            DoesItContain_HighwayTypesA = [ObjClassification["highway"] == i for i in HighwayTypesA]
            DoesItContain_HighwayTypesB = [ObjClassification["highway"] == i for i in HighwayTypesB]
            if True in DoesItContain_HighwayTypesA:
                color = "black"
            if True in DoesItContain_HighwayTypesB:
                color = "black"
                linewidth = 3
            else:
                color = "white"
                opacity = 0
        elif "power" in ObjClassification: # if "leisure" is a tag in properties, do this
            DoesItContain_Power = [ObjClassification["power"] == i for i in Power]    
            if True in DoesItContain_Power:
                color = "red"
                opacity = 1
            else:
                color = "red"
                opacity = 1
        elif "aerialway" in ObjClassification: # if "leisure" is a tag in properties, do this
            DoesItContain_Aerodrome = [ObjClassification["aerialway"] == i for i in Aerodrome]    
            if True in DoesItContain_Aerodrome:
                color = "red"
                opacity = 1
            else:
                color = "black"
                opacity = 0.5
        else:
            color = "lightyellow"
            opacity = 0
        PlotLineString(fig, ax, ObjCoords, color, linewidth, opacity)

# fig.savefig('WholeMap.png', dpi=600)
plt.show()

# POST-PROCESSING
LatD_GolfCourses = []
LonD_GolfCourses = []
for i in range(0,len(ObjectCoords_GolfCourses)):
    LatD = ObjectCoords_GolfCourses[i][0][0][0][1]
    LonD = ObjectCoords_GolfCourses[i][0][0][0][0]
    LatD_GolfCourses.append(LatD)
    LonD_GolfCourses.append(LonD)
    print(LatD,LonD)
df2 = pd.DataFrame(
    {
     "LatD": LatD_GolfCourses,
     "LonD": LonD_GolfCourses
     }
    ) 

FilePath = "C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Datasets/" + "Chicago" + "/" + "Chicago" + ".xlsx"

with pd.ExcelWriter(FilePath,
                    mode='a',engine="openpyxl") as writer:  
    df2.to_excel(writer, sheet_name='GolfCourses')