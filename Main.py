# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 08:30:47 2021
@author: Henry
"""


"""Partie 1 : Packages Fonction et classe"""
import numpy as np
import osmium as osm
import pandas as pd
import xml.etree.ElementTree as ET
import gpxpy
import gpxpy.gpx
import math
import matplotlib.pyplot as plt
import os
import _Functions
import numpy as np
#import time

#This value need to be changed if the program work on a different area
osm_path='cartes/map2.osm'  



#OSM processing will process OSM in order to create file that serve for analysis
#can take a few minutes 
root = ET.parse(osm_path).getroot() 
_Functions.process_osm(root)

    
"""Partie 2 : CHargement des données OSM transformées  """


coordinate = _Functions.load_coordinate('dataFrame/tabSmall.tfk')
coordinate_sort_lat = _Functions.load_coordinate('dataFrame/tabLatSmall.tfk')
coordinate_sort_lon = _Functions.load_coordinate('dataFrame/tabLonSmall.tfk')


"""Partie 3 : Calcul des points OSM correspondant aux tracé GPS"""

file='gpx/Brocante-Culee-26-05-2021.gpx'
pt_gpx=_Functions.read_gpx(open(file))


street_list,node_list= _Functions.GPX_track(root,coordinate,coordinate_sort_lat,coordinate_sort_lon,file)

#save the street_list 

#all street and id
street_list.to_csv(r'impact\street_list.csv', header=None, index=None, sep=' ', mode='a',encoding="utf-8-sig")
#only distinct street name
np.savetxt(fname='impact\street_list.txt',X=street_list['name'].unique(),fmt='%s')


"""
partie test : Cette partie permet de sortir le fichier . GPX des noeuds OSM et ainsi montrer
la fidélité du tracé 
"""



#coordonnées des noeuds OSM
plt.scatter(coordinate['lat'],coordinate['lon'])
plt.axis([50.56,50.64,4.625,4.825])


#coordonnée des pt GPX
plt.scatter(pt_gpx[1],pt_gpx[0])
plt.axis([50.56,50.64,4.625,4.825])


plt.scatter(node_list['lat'],node_list['lon'])
plt.axis([50.56,50.64,4.625,4.825])




#coordonnées des noeuds OSM
plt.scatter(coordinate['lat'],coordinate['lon'])
plt.axis([50.60,50.63,4.675,4.725])


#coordonnées des noeuds OSM    newversion
plt.scatter(pd.to_numeric(node_list['lat'], downcast="float"),pd.to_numeric(node_list['lon'], downcast="float"))
plt.axis([50.60,50.63,4.675,4.725])

#coordonnée des pt GPX
plt.scatter(pt_gpx[1],pt_gpx[0])
plt.axis([50.60,50.63,4.675,4.725])


plt.scatter(node_list['lat'],node_list['lon'])
plt.axis([50.60,50.63,4.675,4.725])


