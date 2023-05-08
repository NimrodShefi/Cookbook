function enlargeImage(img) {
    // Create a new "overlay" element to display the enlarged image
    var overlay = document.createElement('div');
    overlay.classList.add('overlay');
  
    // Create a new "img" element to display the enlarged image
    var enlargedImg = document.createElement('img');
    enlargedImg.src = img.src;
    enlargedImg.classList.add('enlarged-img');
  
    // Add the enlarged image to the overlay
    overlay.appendChild(enlargedImg);
  
    // Add the overlay to the page
    document.body.appendChild(overlay);
  
    // Add a click event listener to the overlay, so that clicking it will close it
    overlay.addEventListener('click', function() {
      document.body.removeChild(overlay);
    });
  }
  