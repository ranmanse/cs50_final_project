import os

from flask import Flask, render_template, request, jsonify
import geopandas as gpd
from requests import Request
import geojson
from pyproj import CRS
import pandas as pd
from owslib.wfs import WebFeatureService

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


        return render_template('index.html', geometry = data_json)
    


if __name__ == '__main__':
    app.run(debug=True)