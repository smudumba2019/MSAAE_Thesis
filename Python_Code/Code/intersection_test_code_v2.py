# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 12:06:26 2021

@author: saimu
"""

from shapely.geometry import Point, Polygon

# https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html

p1 = Point(0.5, 0.5)
p2 = Point(1,1)

coords = [(0,1), (2,2), (0,-1)] 
poly = Polygon(coords)

p1.within(poly)

print(p1.within(poly))
print(poly.contains(p1))
