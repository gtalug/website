// var map = L.map('map').setView([43.659, -79.381], 16)

var map = L.map('map', {
    // center: [43.659, -79.381],
    center: [43.65911684437622, -79.3763279914856],
    zoom: 16,
    touchZoom: false,
    scrollWheelZoom: false
});

var mapIcon = L.icon({
    iconUrl: '/static/img/leaflet/market-icon.png',
    iconRetinaUrl: '/static/img/leaflet/market-icon-2x.png',
    shadowUrl: '/static/img/leaflet/market-shadow.png'
})

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'myles.mp1f6ado',
    accessToken: 'pk.eyJ1IjoibXlsZXMiLCJhIjoiYzM4NjE3NjA4ZjYxYzJhMzJjNjU3MzcxZWEyYzRhMGIifQ.V_-nhDa5NoL9uhK7OqUOew'
}).addTo(map);

var marker = L.marker([43.65911684437622, -79.3763279914856], {icon: mapIcon}).addTo(map);

marker.bindPopup("<strong>George Vari Engineering and Computing Centre</strong><br/>245 Church Street, Room 203.").openPopup();