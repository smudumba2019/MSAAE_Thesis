# -*- coding: utf-8 -*-
"""
Created on Sat May 15 20:40:42 2021

@author: Sai Mudumba
"""
import numpy as np
import math
import matplotlib.pyplot as plt


def PlotInPolarCoordinates(distance, direction, teta, r, arrowprops=None):
    """
    Reference: https://ocefpaf.github.io/python4oceanographers/blog/2015/02/09/compass/
    Compass draws a graph that displays the vectors with
    components `u` and `v` as arrows from the origin.

    """
    angles = np.multiply(direction, math.pi/180)
    radii = distance

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    kw = dict(arrowstyle="->", color='k')
    if arrowprops:
        kw.update(arrowprops)
    [ax.annotate("", xy=(angle, radius), xytext=(0, 0),
                 arrowprops=kw) for
     angle, radius in zip(angles, radii)]
    ax.set_ylim(0, 10)
    return (fig, ax)
