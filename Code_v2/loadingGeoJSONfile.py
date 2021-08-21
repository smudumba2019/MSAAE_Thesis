# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 11:21:09 2021

@author: Sai Mudumba
"""

# https://gis.stackexchange.com/questions/90326/how-to-plot-geojson-using-python


path = "C:/Users/Sai Mudumba/Documents/MSAAE_Thesis_Code/Code_v2/RiskMapGeneration/ohare.geojson"

import json
from shapely.geometry import mapping, shape
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.geometry import LineString

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
    print(multi2.area, ObjCoords)
    ax.add_patch(patch)

#https://wiki.openstreetmap.org/wiki/Map_features#Natural

    
ObjectCoords = []
ObjectType = []
ObjectColor = []
ObjectClassification = []

fig, ax = plt.subplots(figsize=(1*20,20),dpi=300)
for feature in data['features']:
    ObjCoords = feature['geometry']['coordinates']
    ObjectCoords.append(ObjCoords)
    
    ObjType = feature['geometry']['type']
    ObjectType.append(ObjType)
    
    ObjClassification = feature['properties']
    
    Natural_WaterRelated = ("basin","salt_pond","reservoir","water","wetland","glacier","bay","strait","cape","beach","coastline","reef","spring","hot_spring","geyser","blowhole")
    Natural_LandFeatures = ("wood","tree_row","tree","scrub","heath","moor","grassland","fell","bare_rock","scree","shingle","sand","mud")
    Leisure_Facilities = ("golf_course","dog_park","firepit","fishing","garden","horse_riding","ice_rink","marina","nature_reserve","park","picnic_table","pitch","playground","slipway","sports_centre","stadium","summer_camp","track","water_park")    
    HighwayTypesA = ("residential","footway","living_street")
    HighwayTypesB = ("secondary","tertiary","primary","motorway","motorway_link")
    BuildingsAccommodation = ("yes","apartments","bungalow", "cabin", "detached", "dormitory", "farm", "ger", "hotel", "house", "houseboat", "residential", "semidetached_house", "static_caravan", "terrace")
    BuildingsCommercial = ("railway","construction","parking","commercial","industrial", "kiosk", "office", "retail", "supermarket", "warehouse","garage")
    ManMade = ("adit","beacon","breakwater","bridge","bunker_silo","carpet_hanger","chimney","communications_tower","crane","cross","cutline","clearcut","dovecote","dyke","embankment","flagpole","gasometer","goods_conveyor","groyne","guard_stone","kiln","lighthouse","mast","mineshaft","monitoring_station","obelisk","observatory","offshore_platform","petroleum_well","pier","pipeline","pump","pumping_station","reservoir_covered","silo","snow_fence","snow_net","storage_tank","street_cabinet","stupa","surveillance","survey_point","tailings_pond","telescope","tower","wastewater_plant","watermill","water_tower","water_well","water_tap","water_works","wildlife_crossing","windmill","works","yes")    
    LandUse = ("farmland","	farmyard","forest","meadow","vineyard","grass","greenfield","recreation_ground",)
    Amenities = ("parking","p")
    
    if ObjType == "MultiPolygon":            
        # if "natural" in ObjClassification: # if "natural" is a tag in properties, do this
        #     DoesItContainNatural_WaterRelated = [ObjClassification["natural"] == i for i in Natural_WaterRelated]    
        #     DoesItContain_Natural_LandFeatures = [ObjClassification["natural"] == i for i in Natural_LandFeatures]
        #     if True in DoesItContainNatural_WaterRelated:
        #         color = "blue"
        #         opacity = 1                
        #     elif True in DoesItContain_Natural_LandFeatures:
        #         color = "brown"
        #         opacity = 1
        #     else:
        #         color = "black"
        #         opacity = 0.5
        if "leisure" in ObjClassification: # if "leisure" is a tag in properties, do this
            DoesItContain_LeisureFacilities = [ObjClassification["leisure"] == i for i in Leisure_Facilities]    
            if True in DoesItContain_LeisureFacilities:
                color = "green"
                opacity = 0.5
            else:
                color = "green"
                opacity = 0.5
        elif "highway" in ObjClassification:
            DoesItContain_HighwayTypesA = [ObjClassification["highway"] == i for i in HighwayTypesA]
            DoesItContain_HighwayTypesB = [ObjClassification["highway"] == i for i in HighwayTypesB]
            if True in DoesItContain_HighwayTypesA:
                color = "red"
                opacity = 0.5
            elif True in DoesItContain_HighwayTypesB:
                color = "red"
                opacity = 0.5
            else:
                color = "red"
                opacity = 0.5
        # elif "building" in ObjClassification:
        #     DoesItContain_BuildingsAccommodation = [ObjClassification["building"] == i for i in BuildingsAccommodation]
        #     DoesItContain_BuildingsCommercial = [ObjClassification["building"] == i for i in BuildingsCommercial]
        #     if (True in DoesItContain_BuildingsAccommodation) or (True in DoesItContain_BuildingsCommercial):
        #         color = "red"
        #         opacity = 1
        #     else:
        #         color = "black"
        #         opacity = 1
        elif "man_made" in ObjClassification: # if "leisure" is a tag in properties, do this
            DoesItContain_ManMade = [ObjClassification["man_made"] == i for i in ManMade]    
            if True in DoesItContain_ManMade:
                color = "red"
                opacity = 1
            else:
                color = "black"
                opacity = 0.5
        elif "landuse" in ObjClassification: # if "leisure" is a tag in properties, do this
            DoesItContain_LandUse = [ObjClassification["landuse"] == i for i in LandUse]    
            if True in DoesItContain_LandUse:
                color = "green"
                opacity = 1
            else:
                color = "black"
                opacity = 0
        elif "natural" in ObjClassification: # if "natural" is a tag in properties, do this
            DoesItContainNatural_WaterRelated = [ObjClassification["natural"] == i for i in Natural_WaterRelated]    
            DoesItContain_Natural_LandFeatures = [ObjClassification["natural"] == i for i in Natural_LandFeatures]
            if True in DoesItContainNatural_WaterRelated:
                color = "blue"
                opacity = 1                
            elif True in DoesItContain_Natural_LandFeatures:
                color = "brown"
                opacity = 1
            else:
                color = "black"
                opacity = 0.5
        # elif "amenity" in ObjClassification: # if "leisure" is a tag in properties, do this
        #     DoesItContain_Amenities = [ObjClassification["amenity"] == i for i in Amenities]    
        #     if True in DoesItContain_Amenities:
        #         color = "green"
        #         opacity = 1
        #     else:
        #         color = "green"
        #         opacity = 0.5
        else:
            # print(ObjClassification,ObjType)
            color = "white"
            opacity = 0
            
        PlotMultiplePolygon(fig, ax, ObjCoords, color, opacity)        

    if ObjType == "LineString":
        linewidth = 2
        opacity = 1
        if "highway" in ObjClassification:
            DoesItContain_HighwayTypesA = [ObjClassification["highway"] == i for i in HighwayTypesA]
            DoesItContain_HighwayTypesB = [ObjClassification["highway"] == i for i in HighwayTypesB]
            if True in DoesItContain_HighwayTypesA:
                color = "blue"
            if True in DoesItContain_HighwayTypesB:
                color = "blue"
                linewidth = 3
            else:
                color = "white"
                opacity = 0
        # elif "building" in ObjClassification:
        #     DoesItContain_BuildingsAccommodation = [ObjClassification["building"] == i for i in BuildingsAccommodation]
        #     if True in DoesItContain_BuildingsAccommodation:
        #         color = "red"
        #     else:
        #         color = "black"
        # elif "natural" in ObjClassification: # if "natural" is a tag in properties, do this
        #     DoesItContainNatural_WaterRelated = [ObjClassification["natural"] == i for i in Natural_WaterRelated]    
        #     DoesItContain_Natural_LandFeatures = [ObjClassification["natural"] == i for i in Natural_LandFeatures]
        #     if True in DoesItContainNatural_WaterRelated:
        #         color = "blue"
        #     elif True in DoesItContain_Natural_LandFeatures:
        #         color = "brown"
        #     else:
        #         color = "white"
        # elif "man_made" in ObjClassification: # if "leisure" is a tag in properties, do this
        #     DoesItContain_ManMade = [ObjClassification["man_made"] == i for i in ManMade]    
        #     if True in DoesItContain_ManMade:
        #         color = "red"
        #     else:
        #         color = "white"
        else:
            color = "white"
            opacity = 0
        PlotLineString(fig, ax, ObjCoords, color, linewidth, opacity)
    
    # if ObjType == "MultiPolygon":            
    #     PlotMultiplePolygon(fig, ax, ObjCoords, color)
        
        # elif "highway":
    # elif ObjType == "Point":

plt.show()