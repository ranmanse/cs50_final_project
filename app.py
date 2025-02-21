import os

from flask import Flask, json, render_template, request, jsonify
import geopandas as gpd
from requests import Request
import geojson
from pyproj import CRS
import pandas as pd
from owslib.wfs import WebFeatureService
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
    # https://datengraben.com/til/wfs-to-geo-dataframes/
    # URL for WFS backend
        ## WFS fromChatGP
        url = 'https://gdi.berlin.de/services/wfs/berlinermauer?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAME=berlinermauer:a_grenzmauer&OUTPUTFORMAT=application/json'
        wfs = WebFeatureService(url=url, version="2.0.0") 

        # Fetch the last available layer
        layer_name = list(wfs.contents)[-1]
        
        # Specify the parameters for fetching the data
        # Count: specificies amount of rows to return (e.g. 10000 or 100)
        # startIndex: specifies at which offset to start returning rows
        params = dict(service='WFS', version="2.0.0", request='GetFeature',
        typeNames=layer_name)

        # Parse the URL with parameters
        wfs_request_url = Request('GET', url, params=params).prepare().url

        # Read data from URL
        data = gpd.read_file(wfs_request_url).set_crs(epsg=25833, inplace=False, allow_override=True)

        data_json = data.to_json(to_wgs84=True)
        
        #print(data_json)

        # Get data from Flickr API
        #api_url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=aef635a622e9a3e2d5e2c519481331dd&lat=52.48531528648545&lon=13.458874225616457&radius=0.2&max_taken_date=1995-01-01&tag=mauer,wall&format=json&nojsoncallback=1"
        url = "https://api.flickr.com/services/rest/" #?method=flickr.photos.search&api_key=aef635a622e9a3e2d5e2c519481331dd&lat=52.48531528648545&lon=13.458874225616457&radius=0.2&max_taken_date=1995-01-01&tag=mauer,wall&format=json&nojsoncallback=1"
        
        def api_request_per_page(page):
            response = requests.get(url, 
                params = {
                    "method": "flickr.photos.search",
                    "api_key": "aef635a622e9a3e2d5e2c519481331dd",
                    "lon": 13.45928192138672,
                    "lat": 52.485498223625996,
                    #"bbox": "13.077850,52.374342,13.564682,52.685956",
                    "radius": 5,
                    "accuracy": 11,
                    "max_taken_date": "1995-01-01",
                    "tag": "mauer,wall",
                    "page": page,
                    "per_page" : 500,
                    "format": "json",
                    "nojsoncallback": 1,
                    "extras": "geo"

                }).json()
            return response
        
        # Acces response as dictionary - From Co-Pilot: https://www.copilotsearch.com/posts/how-to-use-the-flickr-api 
        photos = api_request_per_page(1)['photos']['photo']

        pages = api_request_per_page(1)['photos']['pages']
        #print('pages: ', pages)
        # Loop through all pages and append to photos (Autocomplete: https://www.copilotsearch.com/posts/how-to-use-the-flickr-api)
       
        
        for page in range(2, pages):
            print("append page", page)
            photos += api_request_per_page(page)['photos']['photo']

        gdf = gpd.GeoDataFrame(photos)
        # Convert latitude and longitude to geoemtry (https://geopandas.org/docs/user_guide/geocoding.html)
        gdf.set_geometry(gpd.points_from_xy(gdf.longitude, gdf.latitude), inplace=True)


        #print(gdf.head)

        # Append API-request to json file
        with open('static/data/flickr_api.geojson', 'w') as f:
            #json.dump(photos, f)
            geojson.dump(gdf, f)
        
        return render_template('index.html', geometry = data_json)
    


if __name__ == '__main__':
    app.run(debug=True)