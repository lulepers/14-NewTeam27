# 14-NewTime27
Hackathon Hack your City février 2021


#Introduction
The following code allow you to map to OSM data any kind of GPS tracing record in .GPX format. This code will be usefull if used to connect an events DataBase with .GPX file
to a local OSM DataBase.

You have to use map.osm data from OpenStreetMap on a local machine. NO OSM API are used in that code.

With the code you will be able to input a .GPX file and find the OSM.nodes that correspond to the GPX.file .

Actually the program will give you the name of the street impacted by your GPX tracing in impact/street_name.txt and the segments name and OSM identifiers in impact/street_name.csv . 



#Explaination
The code work in that way

There is a _Functions.py that containt all classes and functions used by the code. 

There is a main.py were the most important functions and paramaters are used. 
	For modify the data
	at line 23 : osm_path='cartes/map2.osm'  : you can change the name of the map.osm you're using for your server
	at line 26 : file='gpx/Brocante-Culee-26-05-2021.gpx' : you can modify the name of the .GPX file you want to analyse 
	

The main functions allow different thing
	In Part1 you will be able to process map.osm in order to create file that will be used later for GPX analysis. It must be run only once. 
	It is done by the function process.osm(root)

	In part2 you will load in memory the data created by part 1 to initialize the program 

	In part 3 you will be able to compute for a GPX.file the corresponding OSM nodes and retrieving the name of the street that are concerned by the GPX tracing.
		Two files are created 
			-Street_name.txt that contain all unique street name imapcted by the gpx tracing
			-street_name.csv that contain all OSM segments names and ID imapcted by the gpx tracing

	Finally in part test you can plot easily on a windows focus on walhain your GPX data and the OSM Nodes in order to verify the correspondance between datas.
