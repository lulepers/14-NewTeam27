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


#path to the osm map of reference
osm_path='cartes/map2.osm'  

#path of gpx files
gpx_load_path = 'gpx/Brocante-Culee-26-05-2021.gpx'
gpx_save_path = 'gpx2.gpx'

#needed when a new OSM map is used
need_reload_osm = True

#radius of search around gpx Node in order to find a OSM node, if too small return
#an error because it cannot find any, bigger = slower running time
search_radius = 0.001

#if True, draw some graph with pyplot
draw_graph = True





#OSM processing will process OSM in order to create file that serve for analysis
#can take a few minutes 
root = ET.parse(osm_path).getroot() 

if need_reload_osm:
    _Functions.process_osm(root)

    
"""Partie 2 : CHargement des données OSM transformées  """


coordinate = _Functions.load_coordinate('dataFrame/tabSmall.tfk')
coordinate_sort_lat = _Functions.load_coordinate('dataFrame/tabLatSmall.tfk')
coordinate_sort_lon = _Functions.load_coordinate('dataFrame/tabLonSmall.tfk')


"""Partie 3 : Calcul des points OSM correspondant aux tracé GPS"""

pt_gpx=_Functions.read_gpx(open(gpx_load_path))


street_list,node_list= _Functions.GPX_track(root,coordinate,coordinate_sort_lat,coordinate_sort_lon,search_radius,gpx_load_path)
_Functions.OSM_to_GPX(node_list,gpx_save_path)

#save the street_list 

#all street and id
street_list.to_csv(r'impact\street_list.csv', header=None, index=None, sep=' ', mode='a',encoding="utf-8-sig")
#only distinct street name
np.savetxt(fname='impact\street_list.txt',X=street_list['name'].unique(),fmt='%s')


"""
partie test : Cette partie permet de sortir le fichier . GPX des noeuds OSM et ainsi montrer
la fidélité du tracé 
"""

if draw_graph:

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


