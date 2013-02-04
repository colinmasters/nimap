function validateForm() {
    var formname = "profile";
    var name=document.forms[formname]["name"].value;
    var street=document.forms[formname]["street"].value;
    var city=document.forms[formname]["city"].value;
    var county=document.forms[formname]["county"].value;
    var postcode=document.forms[formname]["postcode"].value;
    var properties = [name, street, city, county, postcode];

    for (i=0; i < properties.length; i++) {
        if (properties[i] == null || properties[i]=="") {
            alert("All fields must be filled out");
            return false;
        }
    }

    var longitude = document.forms[formname]["hidLong"].value;
    var latitude = document.forms[formname]["hidLat"].value;

    if (longitude==null || longitude=="" || latitude==null || latitude==""){
        alert("Please hit find so I can Geomap your address!");
        return false;
    }


    if (document.getElementById("terms").checked) {
        return true;
    }
    else {
        alert("Please read and accept the terms and conditions");
        return false;
    }
    return true;
}

var PostCodeid = "#Postcode";
        var longval = "#hidLong";
        var latval = "#hidLat";
        var geocoder;
        var map;
        var marker;

        function initialize() {
            //MAP
            var initialLat = $(latval).val();
            var initialLong = $(longval).val();
            if (initialLat == '') {
                initialLat = "54.867124";
                initialLong = "-6.503906";
            }
            var latlng = new google.maps.LatLng(initialLat, initialLong);
            var options = {
                zoom: 16,
                center: latlng,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
        
            map = new google.maps.Map(document.getElementById("geomap"), options);
        
            geocoder = new google.maps.Geocoder();    
        
            marker = new google.maps.Marker({
                map: map,
                draggable: true,
                position: latlng
            });
        
            google.maps.event.addListener(marker, "dragend", function (event) {
                var point = marker.getPosition();
                map.panTo(point);
            });
            
        };
        
        $(document).ready(function () {
        
            initialize();
        
            $(function () {
                $(PostCodeid).autocomplete({
                    //This bit uses the geocoder to fetch address values
                    source: function (request, response) {
                        geocoder.geocode({ 'address': request.term }, function (results, status) {
                            response($.map(results, function (item) {
                                return {
                                    label: item.formatted_address,
                                    value: item.formatted_address
                                };
                            }));
                        });
                    }
                });
            });
        
            $('#findbutton').click(function (e) {
                var address = $(PostCodeid).val();
                geocoder.geocode({ 'address': address }, function (results, status) {
                    if (status == google.maps.GeocoderStatus.OK) {
                        map.setCenter(results[0].geometry.location);
                        marker.setPosition(results[0].geometry.location);
                        $(latval).val(marker.getPosition().lat());
                        $(longval).val(marker.getPosition().lng());
                    } else {
                        alert("Geocode was not successful for the following reason: " + status);
                    }
                });
                e.preventDefault();
            });
        
            //Add listener to marker for reverse geocoding
            google.maps.event.addListener(marker, 'drag', function () {
                geocoder.geocode({ 'latLng': marker.getPosition() }, function (results, status) {
                    if (status == google.maps.GeocoderStatus.OK) {
                        if (results[0]) {
                            $(latval).val(marker.getPosition().lat());
                            $(longval).val(marker.getPosition().lng());
                        }
                    }
                });
            });
        
        });
