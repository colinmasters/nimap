function initialize(coords) {
    var mapOptions = { 
    	center: new google.maps.LatLng(54.6, -6.7),
        mapTypeId: google.maps.MapTypeId.ROADMAP
        };
    var map = new google.maps.Map(document.getElementById("map_canvas"), 
    	mapOptions);
    
    var northWest = new google.maps.LatLng(55.15, -7.9);
  	var southEast = new google.maps.LatLng(54,-5.6);
  	var bounds = new google.maps.LatLngBounds(northWest,southEast);
  	
  	map.fitBounds(bounds);
  	
  	for (var i = 0; i < coords.length; i++) {
        var coord = coords [i]
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng (coord[1], coord[2]),
            map: map,
            title: coord[0]
        });
    }
}