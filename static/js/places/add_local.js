if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function(position) {
        setMap(position.coords.latitude, position.coords.longitude);
    });
} else {
    setMap(-2.2874005, -78.11685009999997)
}


function setMap(lat, lon) {
    $('#inputMap').locationpicker({
        location: {
            latitude: lat,
            longitude: lon
        },
        enableAutocomplete: true,
        enableReverseGeocode: true,
        radius: 0,
        inputBinding: {
            latitudeInput: $('#id_latitude'),
            longitudeInput: $('#id_longitude'),        
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
