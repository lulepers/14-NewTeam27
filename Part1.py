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
import matplotlib as plt
import time




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
    if tab.iloc[low,:][name_col] >= val:
        return low
    
    elif tab.iloc[len(tab)-1,:][name_col] <= val:
        return len(tab)-1
        
    return binaryNearestHelper(tab, val,0, len(tab)-2, name_col)
    
    
    
    
    
    
def binaryNearestHelper(tab, val, low, high, name_col):  
    mid = (high + low)//2   
    if tab.iloc[mid,:][name_col] <= val and tab.iloc[mid+1,:][name_col] > val or high == low:
        return mid
   
    else:
        if tab.iloc[mid,:][name_col]<val:
            return binaryNearestHelper(tab, val, mid, high, name_col)
        else:
            return binaryNearestHelper(tab, val, low, mid, name_col)
        
    
#
            
        
def distance(x1, y1, x2,y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))


def distanceSQ(x1, y1, x2,y2):
    return (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
        
def findNearestPoint(pt_gps, coordinate_sort_lon, coordinate_sort_lat):
    t1 = time.clock()
    nearest_by_lon = coordinate_sort_lon.iloc[binaryNearest(coordinate_sort_lon, pt_gps[0],'lon'),:]
    distMax = distance(pt_gps[0], pt_gps[1], nearest_by_lon['lon'], nearest_by_lon['lat'])
    
    #on prends les bornes min et max de recherche
    id_min_lat = binaryNearest(coordinate_sort_lat, pt_gps[1]-distMax,'lat')
    id_max_lat = binaryNearest(coordinate_sort_lat, pt_gps[1]+distMax,'lat')
    
    
    # id_min_lon = binaryNearest(coordinate_sort_lat, pt_gps[0]-distMax,'lon')
    # id_max_lon = binaryNearest(coordinate_sort_lat, pt_gps[0]+distMax,'lon')
    
    # id_min_lat = coordinate_sort_lat.iloc[binaryNearest(coordinate_sort_lat, pt_gps[1]-distMax,'lat'),:]['id']
    # id_max_lat = coordinate_sort_lat.iloc[binaryNearest(coordinate_sort_lat, pt_gps[1]+distMax,'lat'),:]['id']

    
    t1 = time.clock()
    l = (id_min_lat+id_max_lat)//2
    r = l+1
    nearest = r
    l_out = False
    r_out = False
    distMin = 360
    while not l_out or not r_out:
        #print(str(l)+"   "+str(r)+"     "+str(distMin)+"   "+str((coordinate_sort_lat.iloc[r,:]['lat']-pt_gps[1])*(coordinate_sort_lat.iloc[r,:]['lat']-pt_gps[1])))
        
        if not l_out:
            d = distanceSQ(pt_gps[0],pt_gps[1],coordinate_sort_lat.iloc[l,:]['lon'],coordinate_sort_lat.iloc[l,:]['lat'])    
            if d < distMin:
                distMin=d
                nearest = l

            l = l-1
            if l<id_min_lat or (coordinate_sort_lat.iloc[l,:]['lat']-pt_gps[1])*(coordinate_sort_lat.iloc[l,:]['lat']-pt_gps[1]) > distMin:
                l_out = True  
                
        
        if not r_out:
            d = distanceSQ(pt_gps[0],pt_gps[1],coordinate_sort_lat.iloc[r,:]['lon'],coordinate_sort_lat.iloc[r,:]['lat'])    
            if d < distMin:
                distMin=d
                nearest = r

            r = r+1
            if r>id_max_lat or (coordinate_sort_lat.iloc[r,:]['lat']-pt_gps[1])*(coordinate_sort_lat.iloc[r,:]['lat']-pt_gps[1]) > distMin:
                r_out = True
                
    
    
    
    
    
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

#Définition de la classe de chemin


class ways:
    def __init__(self):
        self.name=''
        self.id=''
        self.nodes=list()
    
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


 

def save_coordinate(tab, filename):
    tab.to_pickle(filename)

def load_coordinate(filename):
    return pd.read_pickle(filename)

<<<<<<< HEAD
root = ET.parse('cartes/map2.osm').getroot() 


#pour charger une nouvelle carte
# coordinate = get_OSM_nodes(root)  
# coordinate=coordinate.reset_index(drop=True)
# save_coordinate(coordinate, 'dataFrame/tabSmall.tfk')
#coordinate['lat']=pd.to_numeric(coordinate['lat'])
#coordinate['lon']=pd.to_numeric(coordinate['lon'])

=======
    
"""Partie 2 : Traitement unique des données OSM  """
>>>>>>> 8bc87c29990668cb03bfe3db45272597a6c8c094

coordinate = load_coordinate('dataFrame/tabSmall.tfk')

#lecture du .OSM
root = ET.parse('map2.osm').getroot() 
coordinate = get_OSM_nodes(root)  
coordinate=coordinate.reset_index(drop=True)

<<<<<<< HEAD

    
# coordinate_sort_lat =  coordinate.copy()
# coordinate_sort_lon =  coordinate.copy()
=======
coordinate['lat']=pd.to_numeric(coordinate['lat'])
coordinate['lon']=pd.to_numeric(coordinate['lon'])
>>>>>>> 8bc87c29990668cb03bfe3db45272597a6c8c094

#classement des données        
coordinate_sort_lat =  coordinate.copy()
coordinate_sort_lon =  coordinate.copy()

# coordinate_sort_lat.sort_values(by=['lat'], inplace=True)
# coordinate_sort_lon.sort_values(by=['lon'], inplace=True)


# save_coordinate(coordinate_sort_lat, 'dataFrame/tabLatSmall.tfk')
# save_coordinate(coordinate_sort_lon, 'dataFrame/tabLonSmall.tfk')


coordinate_sort_lat = load_coordinate('dataFrame/tabLatSmall.tfk')
coordinate_sort_lon = load_coordinate('dataFrame/tabLonSmall.tfk')


"""Partie 3 : Calcul des points OSM correspondant aux tracé GPS"""

#lecture du .GPX
pt_gpx = read_gpx(open('gpx/Balade-saisonniere-06-03-2021.gpx', 'r'))

<<<<<<< HEAD
node_list=pd.DataFrame(0.1,index=np.arange(len(pt_gpx)),columns=['id', 'lat', 'lon'])

=======
#creation des sorties
node_list=pd.DataFrame(columns=['id', 'lat', 'lon'])
street_list=node_list=pd.DataFrame(columns=['id', 'lat', 'lon'])
>>>>>>> 8bc87c29990668cb03bfe3db45272597a6c8c094

#Analyse pour chacun des points GPS le noeud OSM le plus proche
#node_list contient tout les identifiants des points imapactés par le tracé 
#street_list contient les informations des rues imapctés
for i in range(len(pt_gpx)):

    
    ret = findNearestPoint(pt_gpx.iloc[i,:], coordinate_sort_lon , coordinate_sort_lat)
    #print("ID : "+str(ret['id']))
    #print("lon : "+str(ret['lon'])+"  "+str(pt_gpx.iloc[i,0]))
    # print("lat : "+str(ret['lat'])+"  "+str(pt_gpx.iloc[i,1]))
    temp=check_way_from_point(int(ret['id']),root)
    try : 
        street_list.append(temp)
        except IndexError:
            "Do nothing"
        
    node_list=node_list.append(ret)
    street_list=street_list.append(pd.DataFrame({'name':[temp[0][1]],'id':[temp[0][0]]}))


#afficher les rues uniques impacté par le tracé 
print(street_list['name'].unique())


"""
partie test : Cette partie permet de sortir le fichier . GPX des noeuds OSM et ainsi montrer
la fidélité du tracé 
"""



# Creating a new file:
# --------------------

gpx = gpxpy.gpx.GPX()

# Create first track in our GPX:
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)

# Create first segment in our GPX track:
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

# Create points:
for elem in node_list.iterrows():
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(elem[1][1],elem[1][2], elevation=0))
    print(elem)
    

# You can add routes and waypoints, too...



file = open('gpx2.gpx','w')
file.write( gpx.to_xml())
file.close

print('Created GPX:', gpx.to_xml())


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

#test find enarest point
point=[pt_gpx[1][0],pt_gpx[0][0]]

a=coordinate[coordinate['lat']>point[0]-0.00001]
a[coordinate['lat']<point[0]+0.00001]

b=a[coordinate['lon']>point[1]-0.00001]
b[coordinate['lon']<point[1]+0.00001]



#lecture du .GPX
pt_gpx = read_gpx(open('gpx/Balade-saisonniere-06-03-2021.gpx', 'r'))

#creation des sorties
node_list=pd.DataFrame(columns=['id', 'lat', 'lon'])
street_list=node_list=pd.DataFrame(columns=['id', 'lat', 'lon'])

#Analyse pour chacun des points GPS le noeud OSM le plus proche
#node_list contient tout les identifiants des points imapactés par le tracé 
#street_list contient les informations des rues imapctés


for i in range(len(pt_gpx)):

    #reduction du champs des possibles
    pt_gpx.iloc[i,:]
    a=coordinate[coordinate['lat']>pt_gpx.iloc[i,:][1]-0.00001]
    lat_reduce=coordinate[coordinate['lat']<pt_gpx.iloc[i,:][1]+0.00001]    
    b=lat_reduce[coordinate['lon']>pt_gpx.iloc[i,:][0]-0.00001]
    reduce=b[coordinate['lon']<pt_gpx.iloc[i,:][0]+0.00001]
    
    #renvoi du champs des possibles vers coordinate
    m=coordinate.id.isin(reduce.id)
    
    
    ret = findNearestPoint(pt_gpx.iloc[i,:], coordinate_sort_lon[m].reset_index(drop=True) , coordinate_sort_lat[m].reset_index(drop=True))
    #print("ID : "+str(ret['id']))
    #print("lon : "+str(ret['lon'])+"  "+str(pt_gpx.iloc[i,0]))
    # print("lat : "+str(ret['lat'])+"  "+str(pt_gpx.iloc[i,1]))
    temp=check_way_from_point(int(ret['id']),root)
    try : 
        street_list.append(temp)
    except IndexError:
            "Do nothing"
        
    node_list=node_list.append(ret)
    street_list=street_list.append(pd.DataFrame({'name':[temp[0][1]],'id':[temp[0][0]]}))


#afficher les rues uniques impacté par le tracé 
print(street_list['name'].unique())