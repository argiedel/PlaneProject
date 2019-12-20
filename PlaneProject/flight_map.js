function loadMap() {
    mapboxgl.accessToken = 'pk.eyJ1IjoiYXJnaWVkZWwiLCJhIjoiY2pvN3Iwb3lrMHllbDNxczFjejU0N2MzMiJ9.RUtWszz6MhkntqVX38HSAQ';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/satellite-streets-v9',
        center: [-78.8, 43],
        zoom: 12
    });

    map.on('click', function (e) {
        var loc = e.lngLat;
        var lat = loc['lat'];
        var lon = loc['lng'];
        document.getElementById("lon").value = lon;
        document.getElementById("lat").value = lat;
        get_flights(lat, lon)
    });
}

function get_flights(lat, lon) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("flights").innerHTML = formatFlights(JSON.parse(this.responseText));
        }
    };
    xhttp.open("GET", "http://0.0.0.0:8090/flights/" + String(lat) + "/" + String(lon), true);
    xhttp.send();
}

function formatFlights(data) {
    var plane_list = [];
    for (var plane of data) {
        var flight_number = plane[1];
        if (flight_number == "") {
            continue
        }
        plane_list.push(flight_number);
    }
    if (plane_list.length == 0) {
        return "None"
    }
    return plane_list.join("<br/>");
}