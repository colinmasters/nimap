var niMapStyle = [		
  	{
  		featureType: "road",
  		elementType: "geometry",
  		stylers: [
		  { hue: "#ffffff" },
		  { lightness: 100 }
		]
  		
	},	
	{
  		featureType: "road",
  		elementType: "labels",
  		stylers: [
			{ visibility: "on" },
	      	{ lightness: 6 },
	      	{ hue: "#fff700" }
	    ]
	},
  	{
  		featureType: "water",
  		stylers: [
  			{ hue: "#89cff0" }
  		]
  	},
  	{
		featureType: "transit.line",
	    stylers: [
	    	{ visibility: "off" }
	    ]
	} 	
];

function initialize(coords) {
    var mapOptions = { 
    	center: new google.maps.LatLng(54.6, -6.7),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        styles: niMapStyle
        };
    var map = new google.maps.Map(document.getElementById("map_canvas"), 
    	mapOptions);
    
    var northWest = new google.maps.LatLng(55.15, -7.9);
  	var southEast = new google.maps.LatLng(54,-5.6);
  	var bounds = new google.maps.LatLngBounds(northWest,southEast);
  	
  	map.fitBounds(bounds);
  	
  	for (var i = 0; i < coords.length; i++) {
        var coord = coords [i]

        var infoContent = 
            '<div id="infocontent" class="infocontent">'+
            '<h1>' + coord[2] + '</h1>'+
            '<p>'+ coord[3] +'</p>'+
            '<p>'+ coord[4] +'</p>'+
            '<p>'+ coord[5] +'</p>'+
            '<p>'+ coord[6] +'</p>'+
            '<p><a href="http://'+ coord[7] +'">'+ coord[7] +'</a></p>'+
            '<p>'+ coord[8] +'</p>'+
            '<p>'+ coord[9] +'</p>'+
            '</div>'+
            '<img src="http://images.electricpig.co.uk/wp-content/uploads/2011/01/map-icon.png" class="markerlogo"/>'
            '</div>';

        var infoWindow = new google.maps.InfoWindow({
          content : infoContent
        });

        var marker = new google.maps.Marker({
            position: new google.maps.LatLng (coord[0], coord[1]),
            map: map,
            title: coord[0]
        });

        google.maps.event.addListener(marker, 'click', function() {
          infoWindow.open(map, marker);
        });
    }
}