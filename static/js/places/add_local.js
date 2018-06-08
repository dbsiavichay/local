function getPosition() {
    var lon = $('#id_longitude').val();
    var lat = $('#id_latitude').val();

    if (lon && lat) setMap(lon, lat)
    else {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function(position) {
                setMap(position.coords.longitude, position.coords.latitude);
            });
        } else {
            setMap(-78.11685009999997, -2.2874005)
        }        
    }
}


$('#id_address, #id_latitude, #id_longitude').keydown(function (e) {
    if (e.keyCode == 13) e.preventDefault();
});

function setMap(lon, lat) {    
    var l = $('#inputMap').locationpicker({
        location: {
            latitude: lat,
            longitude: lon,
        },
        enableAutocomplete: true,
        enableReverseGeocode: true,
        radius: 0,
        inputBinding: {
            longitudeInput: $('#id_longitude'),        
            latitudeInput: $('#id_latitude'),
            locationNameInput: $('#id_address')
        },
        onchanged: function (currentLocation, radius, isMarkerDropped) {
            var addressComponents = $(this).locationpicker('map').location.addressComponents;            
            //console.log(currentLocation);  //latlon  
            //console.log(addressComponents);
            //updateControls(addressComponents); //Data
        }
    });
}

getPosition();
