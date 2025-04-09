# Flickr-Mauer-Photos

#### Video Demo:  <https://youtu.be/_w3hMgwzLG8>

#### Description:

#### Demo: <https://cs50-final-project-1.onrender.com/>

#### GitHub: <https://github.com/ranmanse/cs50_final_project>

Flickr-Mauer-Photos is a web-**map-application** that allows querying historic photos from the **Berlin Wall** on a map. These photos are hosted on <www.flickr.com> and are accessed by the **flickr-API**. The map includes historic (1989) and recent areal images, the course of the Berlin Wall and a OpenStreetMap basemap. 

**Users can easily query the photos by moving the map. Flickr-Mauer-Photos then responds all pictures inside the current map extend**. A working demo is hosted on *render.com* (see link above).

Server side the application is based on the web framework **Flask** and client side the application is implemented mainly in plain 
**JavaScript**, the web mapping library **Leaflet** (<https://leafletjs.com/>) and the geospatial toolkit **Turf.js** (<https://turfjs.org/>). 

The server-side code is found in *'app.py'*. There you find the function index() which serves the application to the browser. 

Before serving it prepares and preprocesses the data. This is performed by requests to the flickr-API and by requesting a Web Feature Service (WFS) which contains the course of the Berlin Wall. 

As the flickr-API only accepts 3600 requests per day users do not request the pictures directly from the API. The function regularly performs API-requests and saves the responses to a GeoJSON file locally in *'static/data/flickr_api.geojson’*. The file-based approach was chosen because of the simplicity over a database solution. This means there is no need to serve it via POST-methods to the client. It can be accessed via AJAX. Performance wise, this solution also works decently because the amount of data is not too big. 

The data inside ‘flickr_api.geojson’ is not the result of one API request but of many. This is due to the fact that the flickr-API lacks inconsistencies and is not well documented when requesting geolocated photos by a bounding box. To override these issues each request only uses a small bound box. These bounding boxes are derived from a grid (1000 m * 1000m) that touches the course of the berlin wall. The function iterates through each grid cell / bounding box and appends the response to the local GeoJSON file (*flickr_api.geojson*). As the source information can change over time the GeoJSON is updated time by time. When calling the function it checks the creation time of the file. If it is older than 7 days the function to request the data is executed again.

The client-side code is found in *'templates/index.html'*, *'static/script.js'* and *'static/style.css'*. The browser renders *index.html*, while *script.js* controls the interactive features and *style.css* defines basically the layout. 

The layout consists of to main parts: The map on the left and the gallery on the right. These parts are enclosed by the header and the footer. Each part is defined as a *<div>*/divisions. The behavior of all divisions is controlled by a **CSS-Grid**. 

The map-div uses Leaflet to display:
- Point markers which correspond to each coordinate of *flickr_api.geojson*. In other words, each marker represents a photo
- the course of the Berlin Wall (served by *app.py*)
- an OpenStreetMap base layer
- recent and historic areal images

When panning or zooming the map or clicking on a marker each photo inside the current map view is displayed by the gallery. This algorithm triggered by a **event listener** is implemented in the function fillGallery() which mainly uses Leaflet's method *getBoundingBox()* to get the coordinates of the map view and Turfs's *pointsWithinPolygon* to intersect the map view with the markers. As mentioned before the geospatial processing is accomplished in the browser. As Turf offers enough performance there is no need to to it server-side. 
The gallery is a **subgrid** of the overall CSS-Grid. For each photo (including its title and author) the application creates dynamically a new subgrid-cell. After triggering another event the gallery is cleared.

There is also a event listeners which realizes the initialization of the gallery after loading the application. 
Another event listener is added to implement infinite scroll in the gallery. Due to flickr terms of use, it is only allowed to display 30 photos at once. If the number exceeds the user needs to scroll to the gallery's bottom. That's where the event lister is fired in order to load more photos.

In general, this approach could easily adopted to other regions and to other flickr tags. In order to implement the application your own you need to set your own flickr API Key as environment variable. 
E.g. in a Linux-terminal:

venv/bin/activate:
export FLICKR_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXX"

