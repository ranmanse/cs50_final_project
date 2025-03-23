function showImage(feature) {
    // Update image append code (Co-Pilot)
    const imageContainer = document.getElementById('image-container');
        
    // 1) Create div element / subgrid per image
    var d = document.createElement('div');
    d.className += ("image_subgrid");
    imageContainer.appendChild(d);


    // 3) Append title to subgrid
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
    
    // 2) Append image to subgrid	
    const myImage = new Image();
    myImage.src = `https://live.staticflickr.com/${feature.properties.server}/${feature.properties.id}_${feature.properties.secret}_c.jpg`;
    myImage.className += ("image");
    d.appendChild(myImage);
}
