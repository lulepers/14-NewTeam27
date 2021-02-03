# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 08:30:47 2021

@author: Henry
"""


"""Partie 1 : Récupération des coordonnées des noeuds à partir d'un fichier OSM"""
import numpy as np
import osmium as osm
import pandas as pd

class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []

    def tag_inventory(self, elem, elem_type):
        for tag in elem.tags:
            self.osm_data.append([ elem.id, 
                                   elem.location,
                                   ])

    def node(self, n):
        self.tag_inventory(n, "node")

#Récupération des coordonnées des noeuds du fichier .OSM et sortie sous coordiantes 
        # qui est DF (id,lat,lon) à partir du fichier "map.osm"

osmhandler = OSMHandler()
osmhandler.apply_file("map.osm")
data_colnames = ['id', 'location']
df_osm = pd.DataFrame(osmhandler.osm_data, columns=data_colnames)
coordinate_colnames = ['id','lat','lon']
coordinate=pd.DataFrame(0.1,index=np.arange(len(df_osm)),columns=coordinate_colnames)

#on retransforme un peu les coordonées
for i in range(len(df_osm)):
    coordinate.loc[i]['id']=int(df_osm.loc[i]['id'])    
    coordinate.loc[i]['lat']=df_osm.loc[i]['location'].y/10000000
    coordinate.loc[i]['lon']=df_osm.loc[i]['location'].x/10000000
    
    
"""Partie 2 : Fonction pour identifier les segments """

#Définition de la classe de chemin


class ways:
    def __init__(self):
        self.name=''
        self.id=''
        self.nodes=list()
    
test=ways()
ways.name='paul'    



#exemple de point 
test=int(coordinate.loc[1]['id'])

def check_way_from_point(node_id) :
    output=list()
    for type_tag in root.iter('way'):
        way=ways()
        idi = type_tag.get('id')
        way.id=idi
        for child in type_tag.getchildren() :
            valuend = child.get('ref')
            way.nodes.append(valuend)
            if child.get('k')=='name':
                way.name=child.get('v')
            
                #print(way.name)        
                #regarde si le point existe dans la liste
        try:
            way.nodes.index(str(node_id))       
        except ValueError:
            "Do nothing"
        else: 
            print(way.id,way.name)
            output.append([way.id,way.name])    
    return(output)





"""
pour test 

node_id=284161125 

correspond à un point d'intersection


"""











