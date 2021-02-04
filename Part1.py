# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 08:30:47 2021

@author: Henry
"""


"""Partie 1 : Récupération des coordonnées des noeuds à partir d'un fichier OSM"""
import numpy as np
import osmium as osm
import pandas as pd
import xml.etree.ElementTree as ET
import gpxpy
import gpxpy.gpx
import math






def read_gpx(gpx_file):
        
    gpx = gpxpy.parse(gpx_file)
    liste_point = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                liste_point.append([point.longitude,point.latitude])
                
    return pd.DataFrame(liste_point)                








#QuickSort
def quickSort(tab,name_col):
   quickSortHelper(tab,0,len(tab)-1,name_col)

def quickSortHelper(tab,first,last,name_col):
   if first<last:

       splitpoint = partition(tab,first,last,name_col)

       quickSortHelper(tab,first,splitpoint-1,name_col)
       quickSortHelper(tab,splitpoint+1,last,name_col)


def partition(tab,first,last,name_col):
   pivotvalue = tab[name_col][first]

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and tab[name_col][leftmark] <= pivotvalue:
           leftmark = leftmark + 1

       while tab[name_col][rightmark] >= pivotvalue and rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = tab.iloc[leftmark,:]
           tab.iloc[leftmark,:] = tab.iloc[rightmark,:]
           tab.iloc[rightmark,:] = temp

   temp = tab.iloc[first,:]
   tab.iloc[first,:] = tab.iloc[rightmark,:]
   tab.iloc[rightmark,:] = temp


   return rightmark




#binary search
def binaryNearest(tab, val, name_col, low = 0):

    if tab[name_col][low] >= val:
        return low
    
    elif tab[name_col][len(tab)-1] <= val:
        return len(tab)-1
        
    return binaryNearestHelper(tab, val,0, len(tab)-2, name_col)
    
    
    
    
    
    
def binaryNearestHelper(tab, val, low, high, name_col):  
    mid = (high + low)//2
    if tab[name_col][mid] <= val and tab[name_col][mid+1] > val or high == low:
        return mid
    
    else:
        if tab[name_col][mid]<val:
            return binaryNearestHelper(tab, val, mid, high, name_col)
        else:
            return binaryNearestHelper(tab, val, low, mid, name_col)
        
    
#
            
        
def distance(x1, y1, x2,y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
        
def findNearestPoint(pt_gps, coordinate_sort_lon, coordinate_sort_lat):
    nearest_by_lon = coordinate_sort_lon.iloc[binaryNearest(coordinate_sort_lon, pt_gps[0],'lon'),:]
    distMax = distance(pt_gps[0], pt_gps[1], nearest_by_lon['lon'], nearest_by_lon['lat'])
    
    #on prends les bornes min et max de recherche
    id_min_lat = binaryNearest(coordinate_sort_lat, pt_gps[1]-distMax,'lat')
    id_max_lat = binaryNearest(coordinate_sort_lat, pt_gps[1]+distMax,'lat')
    # id_min_lat = coordinate_sort_lat.iloc[binaryNearest(coordinate_sort_lat, pt_gps[1]-distMax,'lat'),:]['id']
    # id_max_lat = coordinate_sort_lat.iloc[binaryNearest(coordinate_sort_lat, pt_gps[1]+distMax,'lat'),:]['id']

    
    distMin = distMax*2
    nearest = id_min_lat

    for i in range(id_min_lat,id_max_lat+1):
        d = distance(pt_gps[0],pt_gps[1],coordinate_sort_lat.iloc[i,:]['lon'],coordinate_sort_lat.iloc[i,:]['lat'])
        if d < distMin:
            nearest = i
            distMin = d
    return coordinate_sort_lat.iloc[nearest,:]





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



def get_coordinate(file):

#Récupération des coordonnées des noeuds du fichier .OSM et sortie sous coordiantes 
        # qui est DF (id,lat,lon) à partir du fichier "map.osm" 



    osmhandler = OSMHandler()
    osmhandler.apply_file(file)
    data_colnames = ['id', 'location']
    df_osm = pd.DataFrame(osmhandler.osm_data, columns=data_colnames)
    coordinate_colnames = ['id','lat','lon']
    coordinate=pd.DataFrame(0.1,index=np.arange(len(df_osm)),columns=coordinate_colnames)

    
    #on retransforme un peu les coordonées
    for i in range(len(df_osm)):
        coordinate.loc[i]['id']=int(df_osm.loc[i]['id'])    
        coordinate.loc[i]['lat']=df_osm.loc[i]['location'].y/10000000
        coordinate.loc[i]['lon']=df_osm.loc[i]['location'].x/10000000
    return coordinate
    
  
    
    
"""Partie 2 : Fonction pour identifier les segments """

#Définition de la classe de chemin


class ways:
    def __init__(self):
        self.name=''
        self.id=''
        self.nodes=list()
    
# test=ways()
# ways.name='paul'    



#exemple de point 
#test=int(coordinate.loc[1]['id'])



#La fonction prend en entrée l'identifiant d'un point et ressort une slite de liste
# type ((identifiant,Nom),(identifiant,Nom),(identifiant,Nom))" 

def check_way_from_point(node_id, root) :            
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



class nodes:
    def __init__(self):
        self.id=''
        self.lat=''
        self.lon=''


#prend le fichier OSM en entrée et ressort un DF avec les coordonnées 
def get_OSM_nodes(root) :            
    output=pd.DataFrame(0.1,index=np.arange(1),columns=['id', 'lat', 'lon'])
    for type_tag in root.iter('node'):
        node=nodes()
        node.id=type_tag.get('id')
        node.lon=type_tag.get('lon')
        node.lat=type_tag.get('lat')
        interm={'id':node.id,'lon':node.lon,'lat':node.lat}
        output=output.append(interm,ignore_index=True)
        #print(node.id,node.lat,node.lon)
    output=output.drop(0)
    return output











root = ET.parse('cartes/map.osm').getroot() 
coordinate = get_OSM_nodes(root)  
coordinate=coordinate.reset_index(drop=True)

coordinate['id']=int(coordinate['id'])


# node_id=284161125           #  correspond à un point d'intersection

# check_way_from_point(node_id,root)

        
coordinate_sort_lat =  coordinate.copy()
coordinate_sort_lon =  coordinate.copy()

quickSort(coordinate_sort_lat, 'lat')
quickSort(coordinate_sort_lon, 'lon')



pt_gpx = read_gpx(open('gpx/Balade-saisonniere-06-03-2021.gpx', 'r'))

node_list=pd.DataFrame(0.1,index=np.arange(len(pt_gpx)),columns=coordinate_colnames)


for i in range(len(pt_gpx)):

    ret = findNearestPoint(pt_gpx.iloc[i,:], coordinate_sort_lon , coordinate_sort_lat)
    print("ID : "+str(ret['id']))
    print("lon : "+str(ret['lon'])+"  "+str(pt_gpx.iloc[i,0]))
    print("lat : "+str(ret['lat'])+"  "+str(pt_gpx.iloc[i,1]))
    check_way_from_point(int(ret['id']),root)
    
    node_list.append(ret)
    
    print()    



""""
partie test

""""










