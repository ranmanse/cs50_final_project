function showImage(feature) {
    // Update image append code (Co-Pilot)
    const imageContainer = document.getElementById('image-container');
        
    // 1) Create div element / subgrid per image
    var d = document.createElement('div');
    d.className += ("image_subgrid");
    imageContainer.appendChild(d);


    // 2) Append title to subgrid
    //https://stackoverflow.com/questions/4772774/how-do-i-create-a-link-using-javascript
    var a = document.createElement('a');
    a.className += ("link_text");

    var linkText = document.createTextNode(`${feature.properties.title} by ${feature.properties.ownername}`);
    a.appendChild(linkText);
    a.href = `https://www.flickr.com/photos/${feature.properties.owner}/${feature.properties.id}`, 'target =_blank';

    // In neuem Tab öffnen: https://www.dhiwise.com/post/html-open-link-in-new-tab-improve-user-navigation
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener noreferrer');

    d.appendChild(a);
    
    // 3) Append image to subgrid	
    const myImage = new Image();
    myImage.src = `https://live.staticflickr.com/${feature.properties.server}/${feature.properties.id}_${feature.properties.secret}_c.jpg`;
    myImage.className += ("image");
    d.appendChild(myImage);
}


function getBoundingBox() {
    // Get bounds from map: https://runebook.dev/en/articles/leaflet/index/map-getbounds
			var bounds = map.getBounds();
			bound_miny = bounds.getSouthWest().lat;
			bound_minx = bounds.getSouthWest().lng;
			bound_maxy = bounds.getNorthEast().lat;
			bound_maxx = bounds.getNorthEast().lng;
            bbox = [bound_minx, bound_miny, bound_maxx, bound_maxy];

            return bbox;
}


function calculatePages(photosWithin, current_page) {
    var feature_length = photosWithin.features.length;
	//console.log('feature_length:' + feature_length);

    var current_page = current_page;
	var page_start = 1;
	var page_end;
		
    if (Math.trunc(photosWithin.features.length/30) == 0) {
        page_end = 1;
    } else if (Math.trunc(photosWithin.features.length/30) > 0) {
        page_end = Math.trunc(photosWithin.features.length/30) + 1;
    }


    var array_start = (30 * current_page) - 30;
	var array_end = (30 * current_page);

    let pagination = {
        page_start: page_start,
        page_end: page_end,
        array_start: array_start,
        array_end: array_end
    };

    return pagination;
}


function addPaginationButtons(page_start, page_end) {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = ''; // Clear existing buttons
    
    var d = document.createElement('div');
    d.className += ("button_subgrid");
    pagination.appendChild(d);
        
    // Add pagination
    for (page_start; page_start <= page_end; page_start++) {
        var button = document.createElement('button');
        button.innerHTML = page_start;
        button.className += ("button_subgrid");
        d.appendChild(button);
    }

}


function fillGallery(current_page){
    // 1 Clear existing images/Container			
			const imageContainer = document.getElementById('image-container');
			imageContainer.innerHTML = ''; // Clear existing images
			imageContainer.scrollTop;

			// 2 Get Bounding Box
			bbox_coordinates = getBoundingBox();

			// 3 Intersect Flickr-GeoJSON with Bounding Box
			var polygon_bbox = turf.bboxPolygon(bbox_coordinates);
			var photosWithin = turf.pointsWithinPolygon(flickr_data, polygon_bbox);
			//console.log(photosWithin);

			// 4) Prepare pagination in order to display 30 images per page			     
            let pages = calculatePages(photosWithin, current_page);
			           
			let page_start = pages.page_start;
			let page_end = pages.page_end;
			let array_start = pages.array_start;
			let array_end = pages.array_end;
					
			// 5) Slice Flickr-Data according the page
			var features_slice = photosWithin.features.slice(array_start, array_end)
			
			// 6) Loop through each feature of the slice and create an image element
			features_slice.forEach(feature => {
				showImage(feature);							
			});
		        
			// 7) Create div element / subgrid per button
			addPaginationButtons(page_start, page_end)
			// Aktuelle Seite als Parameter übergeben

            // 8) Add event listener to each button
}