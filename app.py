import os

from flask import Flask, json, render_template, request, jsonify
import geopandas as gpd
from requests import Request
import geojson
from pyproj import CRS
import pandas as pd
from owslib.wfs import WebFeatureService
import requests
from datetime import timedelta
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":

        
    ## 1) Request data from WFS
        
        url = "https://gdi.berlin.de/services/wfs/berlinermauer"

        params = {
            "SERVICE": "WFS",
            "VERSION": "2.0.0",
            "REQUEST": "GetFeature",
            "TYPENAMES": "berlinermauer:a_grenzmauer",
            "OUTPUTFORMAT": "application/json"
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=30
            )


            print("Status:", response.status_code)
            print("Content-Type:", response.headers.get("Content-Type"))
            print("URL:", response.url)
            print("Antwort:", response.text[:500])

            response.raise_for_status()

            data_json = json.dumps(response.json())

        except Exception as e:
            app.logger.warning("WFS konnte nicht geladen werden: %s", e)
            data_json = '{"type": "FeatureCollection", "features": []}'

                       
     ## 2) Request data from Flickr API
        '''       
        # a) Load grid for API request (made in QGIS)
        grid = gpd.read_file('static/data/grid_1000.geojson')
        bounding_boxes = grid.geometry.bounds   

        # b) Create empty list to savi API request into
        photos = []

       
        
        

        # d) Check if last API-Request is older than 1 week

        now = datetime.now()
        flickr_geojson_path = 'static/data/flickr_api.geojson'
        limit = timedelta(days=7)

        if os.path.exists(flickr_geojson_path):
            last_request = datetime.fromtimestamp(os.path.getmtime(flickr_geojson_path))
            diff = now - last_request
        else:
            diff = limit + timedelta(seconds=1)

        if diff > limit:
            print('last request older than 1 week')

            # d) Loop through bounding boxes and make API request
            for box in bounding_boxes.values.tolist():
                
                minx = box[0]
                miny = box[1]
                maxx = box[2]
                maxy = box[3]
                bbox = f"{minx},{miny},{maxx},{maxy}"
                print(bbox)             

            # e) Params for Flickr API request
                url = "https://api.flickr.com/services/rest/" 
                flickr_api_key = os.environ.get('FLICKR_API_KEY')



                # c) Create function to make API request
                def api_request_per_page(page, bbox):
                    response = requests.get(url, 
                            params = {
                                        "method": "flickr.photos.search",
                                        "api_key": flickr_api_key,
                                        #"lon": 13.45928192138672,
                                        #"lat": 52.485498223625996,
                                        #"bbox": "13.077850,52.374342,13.564682,52.685956",
                                        #"bbox": "13.412504,52.468456,13.499966,52.509274",
                                        "bbox": bbox,
                                        #"license": "1,2,3,4,5,6,7,8,9,10",
                                        #"radius": 1,
                                        #"accuracy": 11,
                                        "max_taken_date": "1960-01-01",
                                        "max_taken_date": "1990-12-31",
                                        "tag": "berlin wall, berliner mauer, wall, mauer, Sektorengrenze, Die Mauer, The Wall, Deutsche Teilung, Checkpoint, Antifaschistischer Schutzwall",
                                        "page": page,
                                        "per_page" : 500,
                                        "format": "json",
                                        "nojsoncallback": 1,
                                        "extras": "geo, licence, date_taken, owner_name, url_o, tags"
                                    }
                            ).json()
                    return response
                
                print('api_request_per_page', api_request_per_page(1,bbox))                                
                # Acces response as dictionary - From Co-Pilot: https://www.copilotsearch.com/posts/how-to-use-the-flickr-api 
                photos += api_request_per_page(1,bbox)['photos']['photo']   
                print(photos)
                pages = api_request_per_page(1,bbox)['photos']['pages']
                print('pages: ', pages)
                # Loop through all pages and append to photos (Autocomplete: https://www.copilotsearch.com/posts/how-to-use-the-flickr-api)
                # Request could have more than one page       
                for page in range(1, pages):
                    print("append page", page)
                    photos += api_request_per_page(page, bbox)['photos']['photo']

            # f) Create geodataframe from API request/ photos list
            gdf = gpd.GeoDataFrame(photos)
            print(gdf.size)
            print(gdf.head)
            
            # g) Convert latitude and longitude to geoemtry (https://geopandas.org/docs/user_guide/geocoding.html)
            if gdf.size > 0:
                gdf.set_geometry(gpd.points_from_xy(gdf.longitude, gdf.latitude), inplace=True)


                print(gdf.head)
                print(gdf.size)

            # h) Save geodataframe as geojson   
                with open('static/data/flickr_api.geojson', 'w') as f:
                    #json.dump(photos, f)
                    geojson.dump(gdf, f)
        '''
            
        return render_template('index.html', wall_geometry = data_json)
    


if __name__ == '__main__':
    app.run(debug=True)