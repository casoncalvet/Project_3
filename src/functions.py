# Import All 
import pymongo
import requests
from pymongo import MongoClient
from pymongo import GEOSPHERE
import pandas as pd
import json
import os
from dotenv import load_dotenv
import pandas as pd
import geopandas as gpd
from cartoframes.viz import Map, Layer, popup_element

# Connect w/ Foursquare API 
load_dotenv()
token_fsq = os.getenv("token3")

def get_query(query, coords, limit= 1,radius= 1000):
    """
    Query foursquare around coordinates using outputs from get_coordinates
    """
    lat= coords[0]
    lon= coords[1]
    url = f"https://api.foursquare.com/v3/places/search?query={query}&ll={lat}%2C{lon}&radius={str(radius)}&limit={str(limit)}"
    headers = {
        "accept": "application/json",
        "Authorization": token_fsq}
    response = requests.get(url, headers=headers).json()
    return response

def get_coordinates (where):
    """
    get coordinates from foursquare API
    """
    url_geocode = f"https://geocode.xyz/{where}?json=1"

    try:
        res = requests.get(url_geocode).json()
        return res["latt"], res["longt"]
    except:
        print(f"Sorry, no matches found for {where}")
    get_coordinates (where)

def get_all(output_get_query): 
    """
    Get name, address, category, and geopoints from each city
    """
    new_list= []
    for i in output_get_query["results"]:
        name = i["name"]
        address =  i["location"]["formatted_address"]
        lat = i["geocodes"]["main"]["latitude"]
        lon = i["geocodes"]["main"]["longitude"]
        category= i['categories'][0]['name']

        type_ = {"typepoint": 
                                {"type": "Point", 
                                "coordinates": [lat, lon]}}
        new_list.append({"name":name, "lat":lat, "lon":lon, "category": category, "type":type_})
    df = pd.DataFrame(new_list)
    return df    

def save_df (df, name):
    """
    save output API queries to csv
    """
    df.to_csv(f"{name}.csv")

Singapore= get_coordinates ('Singapore, Singapore')

Zurich= get_coordinates ('Zurich, Switzerland')

Atlanta = get_coordinates ('Atlanta, United States of America')

def Sing_Map(): 
    """
    Display map of Singapore with desired conditions.
    """
    #Call variables
    GroomSing=pd.read_csv('../datasets/Singapore/GroomSing.csv')
    BarSing=pd.read_csv('../datasets/Singapore/BarSing.csv')
    CareSing=pd.read_csv('../datasets/Singapore/CareSing.csv')
    BasketSingC=pd.read_csv('../datasets/Singapore/BasketSingC.csv')
    AirSing=pd.read_csv('../datasets/Singapore/AirSing.csv')
    starbucksing=pd.read_csv('../datasets/Singapore/starbucksing.csv')
    designsing=pd.read_csv('../datasets/Singapore/designsing.csv')
    tech_singapore=pd.read_csv('../datasets/Singapore/tech_singapore.csv')
    
    # Make into GeoPandas Dataframes 
    Sing_geodf = gpd.GeoDataFrame(tech_singapore, geometry=gpd.points_from_xy(tech_singapore["lon"], tech_singapore["lat"]))
    Sing_geoStar= gpd.GeoDataFrame(starbucksing, geometry=gpd.points_from_xy(starbucksing["lon"], starbucksing["lat"]))
    Sing_geoDes= gpd.GeoDataFrame(designsing, geometry=gpd.points_from_xy(designsing["lon"], designsing["lat"]))
    Sing_geoAir= gpd.GeoDataFrame(AirSing, geometry=gpd.points_from_xy(AirSing["lon"], AirSing["lat"]))
    Sing_geoBas= gpd.GeoDataFrame(BasketSingC, geometry=gpd.points_from_xy(BasketSingC["lon"], BasketSingC["lat"]))
    Sing_geoCare= gpd.GeoDataFrame(CareSing, geometry=gpd.points_from_xy(CareSing["lon"], CareSing["lat"]))
    Sing_geoBar= gpd.GeoDataFrame(BarSing, geometry=gpd.points_from_xy(BarSing["lon"], BarSing["lat"]))
    Sing_geoGroom= gpd.GeoDataFrame(GroomSing, geometry=gpd.points_from_xy(GroomSing["lon"], GroomSing["lat"]))

    # Apply to map 
    Sing_Map= Map([
        Layer(Sing_geodf, "color:blue", popup_hover=[popup_element("name")]),
        Layer(Sing_geoStar, 'color:green', popup_hover=[popup_element("name")]),
        Layer(Sing_geoDes, 'color:purple', popup_hover=[popup_element("name")]), 
        Layer(Sing_geoAir, 'color:white', popup_hover=[popup_element("name")]), 
        Layer(Sing_geoBas, 'color:orange', popup_hover=[popup_element("name")]), 
        Layer(Sing_geoCare, 'color:pink', popup_hover=[popup_element("name")]), 
        Layer(Sing_geoBar, 'color:black', popup_hover=[popup_element("name")]), 
        Layer(Sing_geoGroom, 'color:brown', popup_hover=[popup_element("name")])
    ])
    return Sing_Map

def At_Map(): 
    """
    Returns the Map of Atlanta with desired conditions queried from Foursquare
    """
    #Reload data in case of refreshed kernel 
    atBar=pd.read_csv('../datasets/Atlanta/atBar.csv')
    AtGroom=pd.read_csv('../datasets/Atlanta/AtGroom.csv')
    TechAt=pd.read_csv('../datasets/Atlanta/TechAt.csv')
    DesAt=pd.read_csv('../datasets/Atlanta/DesAt.csv')
    StarAt=pd.read_csv('../datasets/Atlanta/StarAt.csv')
    BasAt=pd.read_csv('../datasets/Atlanta/BasAt.csv')
    AtCare=pd.read_csv('../datasets/Atlanta/AtCare.csv')
    AtAir=pd.read_csv('../datasets/Atlanta/AtAir.csv')

    # Make geodf for Atlanta map 
    At_geotech = gpd.GeoDataFrame(TechAt, geometry=gpd.points_from_xy(TechAt["lon"], TechAt["lat"]))
    At_geoDes = gpd.GeoDataFrame(DesAt, geometry=gpd.points_from_xy(DesAt["lon"], DesAt["lat"]))
    At_geoStar = gpd.GeoDataFrame(StarAt, geometry=gpd.points_from_xy(StarAt["lon"], StarAt["lat"]))
    At_geoBas = gpd.GeoDataFrame(BasAt, geometry=gpd.points_from_xy(BasAt["lon"], BasAt["lat"]))
    At_geoCare = gpd.GeoDataFrame(AtCare, geometry=gpd.points_from_xy(AtCare["lon"], AtCare["lat"]))
    At_geoAir = gpd.GeoDataFrame(AtAir, geometry=gpd.points_from_xy(AtAir["lon"], AtAir["lat"]))
    At_geoBar = gpd.GeoDataFrame(atBar, geometry=gpd.points_from_xy(atBar["lon"], atBar["lat"]))
    At_geoGroom = gpd.GeoDataFrame(AtGroom, geometry=gpd.points_from_xy(AtGroom["lon"], AtGroom["lat"]))

    # Add layers to map 
    At_map= Map([
        Layer(At_geotech, "color:blue", popup_hover=[popup_element("name")]),  
        Layer(At_geoDes, "color:purple", popup_hover=[popup_element("name")]),
        Layer(At_geoStar, "color:green", popup_hover=[popup_element("name")]), 
        Layer(At_geoBas, "color:orange", popup_hover=[popup_element("name")]), 
        Layer(At_geoCare, "color:pink", popup_hover=[popup_element("name")]), 
        Layer(At_geoAir, "color:white", popup_hover=[popup_element("name")]), 
        Layer(At_geoBar, "color:black", popup_hover=[popup_element("name")]), 
        Layer(At_geoGroom, "color:brown", popup_hover=[popup_element("name")])
    ])
    return At_map

def Map_Zurich(): 
    """
    Retruns Map of Zurich with desired conditions 
    """
    # Add data
    ZurGroom= pd.read_csv('../datasets/Zurich/ZurGroom.csv')
    Zurbar= pd.read_csv('../datasets/Zurich/Zurbar.csv')
    ZurAir= pd.read_csv('../datasets/Zurich/ZurAir.csv')
    ZurCare= pd.read_csv('../datasets/Zurich/ZurCare.csv')
    ZurBas= pd.read_csv('../datasets/Zurich/ZurBas.csv')
    StarZur= pd.read_csv('../datasets/Zurich/StarZur.csv')
    DesZur= pd.read_csv('../datasets/Zurich/DesZur.csv')
    tech_Zurich=pd.read_csv('../datasets/Zurich/tech_Zurich.csv')

    # Make geodf for each condition in Zurich 
    Zur_geotech = gpd.GeoDataFrame(tech_Zurich, geometry=gpd.points_from_xy(tech_Zurich["lon"], tech_Zurich["lat"]))
    Zur_geoDes = gpd.GeoDataFrame(DesZur, geometry=gpd.points_from_xy(DesZur["lon"], DesZur["lat"]))
    Zur_geoStar = gpd.GeoDataFrame(StarZur, geometry=gpd.points_from_xy(StarZur["lon"], StarZur["lat"]))
    Zur_geoBas = gpd.GeoDataFrame(ZurBas, geometry=gpd.points_from_xy(ZurBas["lon"], ZurBas["lat"]))
    Zur_geoCare = gpd.GeoDataFrame(ZurCare, geometry=gpd.points_from_xy(ZurCare["lon"], ZurCare["lat"]))
    Zur_geoAir = gpd.GeoDataFrame(ZurAir, geometry=gpd.points_from_xy(ZurAir["lon"], ZurAir["lat"]))
    Zur_geoBar = gpd.GeoDataFrame(Zurbar, geometry=gpd.points_from_xy(Zurbar["lon"], Zurbar["lat"]))
    Zur_geoGroom = gpd.GeoDataFrame(ZurGroom, geometry=gpd.points_from_xy(ZurGroom["lon"], ZurGroom["lat"]))

    # Add layers to map 
    Zurich_Map= Map([
        Layer(Zur_geotech, "color:blue", popup_hover=[popup_element("name")]),
        Layer(Zur_geoDes, "color:purple", popup_hover=[popup_element("name")]),
        Layer(Zur_geoStar, "color:green", popup_hover=[popup_element("name")]), 
        #Layer(Zur_geoBas, "color:orange", popup_hover=[popup_element("name")]), 
        Layer(Zur_geoCare, "color:pink", popup_hover=[popup_element("name")]), 
        Layer(Zur_geoAir, "color:white", popup_hover=[popup_element("name")]), 
        Layer(Zur_geoBar, "color:black", popup_hover=[popup_element("name")]),
        Layer(Zur_geoGroom, "color:brown", popup_hover=[popup_element("name")])
    ])
    return Zurich_Map

def connect_to_Zurich(localhost): 
    """
    Connect to Zurich information in Mongodb. 
    localhost must be input as a string.
    """
    client = pymongo.MongoClient(localhost)
    db = client.get_database("Ironhack")
    return db.get_collection("Zur_Cond")

def get_closeby_things (location, max_distance):

    """
    Find close by businesses to desired location.
    """
    
    proy_ = {"_id": 0}

    converted  = {"type": "Point", "coordinates":location}
    query = {"type.typepoint": 
             {"$near": 
              {"$geometry": converted, "$maxDistance": max_distance
}}}
    
    return list(zcond.find(query, proy_))

ZurichConditions= pd.read_csv('../datasets/Zurich/ZurichCondistions.csv')

def get_density(ZurichConditions):
    """
    Get density of nearby businesses in Zurich
    """ 
    ZurichConditions["density"] = ZurichConditions.apply(lambda x: len(get_closeby_things([x.lat, x.lon], 500)), axis=1)
    save_df(ZurichConditions, "ZurichConditions_den")
    return ZurichConditions

