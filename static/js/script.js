// var map = L.map('map').setView([43.659, -79.381], 16)

var map = L.map('map', {
    // center: [43.659, -79.381],
    center: [43.6577,-79.3773],
    zoom: 16,
    touchZoom: false,
    scrollWheelZoom: false
});

var mapIcon = L.icon({
    iconUrl: '/static/img/leaflet/marker-icon.png',
    iconRetinaUrl: '/static/img/leaflet/marker-icon-2x.png',
    shadowUrl: '/static/img/leaflet/marker-shadow.png'
})

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'gtalug-home',
    accessToken: 'pk.eyJ1IjoiZ3RhbHVnIiwiYSI6ImNqZWVramt4dzFkMXcyeGxhanltdGg5dXEifQ.eoBUNwjc5f5nPPnmDmlYzw'
}).addTo(map);

var marker = L.marker([43.6577,-79.3773], {icon: mapIcon}).addTo(map);

marker.bindPopup("<strong>George Vari Engineering and Computing Centre</strong><br/>245 Church Street, Room 203.").openPopup();