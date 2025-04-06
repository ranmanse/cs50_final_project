# Flickr-Mauer-Photos

#### Video Demo:  <URL HERE>

#### Description:

#### GitHub: <https://github.com/ranmanse/cs50_final_project>

Flickr-Mauer-Photos is a web-**map-application** that allows querying historic photos from the **Berlin Wall** on a map. These photos are hosted on flickr.com and are accessed by **flickr-API**. The map includes historic (1989) and recent areal images, the course of the Berlin Wal and a OpenStreetMap basemap.  

**Users can easily query the photos by moving the map. Flickr-Mauer-Photos then responds all pictures inside the current map extend**.  

Server side the application is based on the web framework **Flask** and client side the application is implemented in mainly in plain 
**JavaScript** and the web mapping library **Leaflet**. 

The server-side code is found in *'app.py'*. In general, it is the because the function index() serves the application to the browser.  

Before serving it prepares the data. This is performed by requests to the flickr-API and by requesting a Web Feature Service (WFS) which contains the course of the Berlin Wall. 

As the flickr-API only accepts 3600 requests per day users do not request the pictures directly from the API. The function regularly performs API-requests and saves the responses in a GeoJSON file locally in *'static/data/flickr_api.geojson’*. The file-based approach was chosen because of the simplicity over a database solution. This means there is no need to serve it via POST-methods to the client. It can be accessed via AJAX. Performance wise, this solution also works decently because the amount of data is not too big.  

The data inside ‘flickr_api.geojson’ is not the result of one API request but of many. This is due to the fact that the flickr-API lacks inconsistencies and is not well documented when requesting geolocated photos by bounding box. To override these issues each request only uses a small bound box. These bounding boxes are derived from a grid (1000 m * 1000m) that touch the course of the berlin wall. The function iterates through each grid cell / bounding box and appends the response to flickr_api.geojson’. As the source information can change over time the geojson is updated time by time. At the moment this step is done manually. That's why the corresponding code is commented.  

The client-side code is found in *'templates/index.html'*, *'static/script.js'* and *'static/style.css'*. The browser renders *index.html*, while *script.js* controls the interactive features and *style.css* defines basicly the layout.  

The layout consists of to main parts: The map on the left and the gallery on the right. These parts are enclosed by the header and the footer. Each part is defined as a *<div>*/divisions. The behaviour of all divisions is controlled by a **CSS-Grid**.  

The map-div uses Leaflet to display:
- Point markers which correspond to each coordinate of *flickr_api.geojson*. In other words, each marker represents a photo
- the course of the Berlin Wall (served by *app.py*)
- an OpenStreetMap base layer
- recent and historic areal images

When panning or zooming the map or clicking on a marker each photo inside the current map view is displayed in the gallery. This behaviour is realised by a **event listeners**. 

There are more event listeners which realize: 

- Initialisation of the gallery after loading the application
- Infinite scroll in the gallery
 


In order to implent the application your own you need to set your own Flickr API Key as environment variable. 
E.g. in a Linux-terminal:

    venv/bin/activate:
    export FLICKR_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXX"


