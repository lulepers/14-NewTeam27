# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 21:13:32 2021

@author: Henry


Affichage graphique

"""

import matplotlib.pyplot as plt
# Load longitude, latitude data
plt.hold(True)
#plot the data as a blue line with red squares on top
# Just plot longitude vs. latitude
plt.plot(longitude, latitude, 'b') # Draw blue line
plt.plot(longitude, latitude, 'rs') # Draw red squares





ax = df.plot(column='classification', colormap='accent')