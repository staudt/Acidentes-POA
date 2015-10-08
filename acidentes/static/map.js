var map;
function initMap() {
    var data = JSON.parse($("#data").text());
    
    //Leaf tryout - not working :(
    /*
    var geocoder = new google.maps.Geocoder();
    var map = new L.Map('map', {center: new L.LatLng(-30.1008231, -51.1589488), zoom: 9});
    var googleLayer = new L.Google('ROADMAP');
    map.addLayer(googleLayer);
    L.Marker([parseFloat(data["LATITUDE"]), parseFloat(data["LONGITUDE"])]).addTo(map);
    */
    
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -30.1008231, lng: -51.1589488},
        zoom: 11
    });
    if (data)
    {
        console.log(parseFloat(data["LATITUDE"]));
        console.log(parseFloat(data["LONGITUDE"]));
        var marker = new google.maps.Marker({
            position: {lat: parseFloat(data["LATITUDE"]), lng: parseFloat(data["LONGITUDE"])},
            icon: { 
                path: google.maps.SymbolPath.CIRCLE, 
                scale: 10
            },
            draggable: true,
            map: map
        });
    }
}