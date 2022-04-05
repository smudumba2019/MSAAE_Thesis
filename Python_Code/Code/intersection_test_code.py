# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 11:11:48 2021

@author: saimu
"""

from shapely.geometry import Polygon, LineString, Point
import geopandas

s = geopandas.GeoSeries(
    [
        Polygon([(-1, -1), (2, 2), (2, -1)]),
        LineString([(0, 0), (2, 2)]),
        LineString([(2, 0), (0, 2)]),
        Point(0, 1),
    ],
)

from shapely.geometry import Polygon, LineString, Point
s = geopandas.GeoSeries(
    [
        Polygon([(0, 0), (2, 2), (0, 2)]),
        Polygon([(0, 0), (2, 2), (0, 2)]),
        LineString([(0, 0), (2, 2)]),
        LineString([(2, 0), (0, 2)]),
        Point(0, 1),
    ],
)


s.intersection(Polygon([(0, 0), (1, 1), (0, 1)]))

line = LineString([(-1, 1), (3, 1)])
point = Point(0, 1)
s.intersects(point)

print(s.intersects(point))
