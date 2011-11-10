//var api_url = 'https://rockt.ca/api/'
var apiUrl = 'http://192.168.1.42:8000/api/'
var markers = [];
var map;
var bounds;


function addFooter() {
    $('.footer').html('stillinbeta | $00');
}

function init() {
    addFooter();
  //  initMap();
}

function initMap() {
    $('#map-content').css('padding','0');
    $('#map-content').height($('#map').height() - $('#map div:first').height() - 2);
    var latlng = new google.maps.LatLng(43.6547, -79.3739);
    var myOptions = { 
        center: latlng,
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map-content'),
        myOptions); 
}

function failure(message) {
    $('#error-content').html(message);
    $('<a href="#error" data-rel="dialog" />').click();
}
    

function loadStopList() {
    $.mobile.showPageLoadingMsg();
    jQuery.getJSON( apiUrl + 'stop/find/43.64903/-79.3967/')
    .success(function(data) { loadedStopList(data) } )
    .error(function(err) { failure('Error retriving stops'); } );
}

function loadedStopList(data) { 
    loadMap(data, 'Select a stop', function (stop) {
        return '<a style="color: black;" href="javascript:loadStop(\''
            + stop.url + '\')">' + stop.description + ' (' 
            + stop.number + ')</a>';
    });
}
    
function loadMap(data, title, infoFunc) {
    $('#map-name').html(title); 
    $.mobile.changePage($('#map'));
    initMap();
    markers.map( function(point) {
        point.setMap(null);
    });
    markers = [];
    
    bounds = new google.maps.LatLngBounds();
    $.each(data, function(index, stop) {
        var location = new google.maps.LatLng(stop.location[1], 
            stop.location[0]);
        var point = new google.maps.Marker({
            position: location,
            map: map 
        }); 
        var infoWindow = new google.maps.InfoWindow({
            content: infoFunc(stop)
        });
        google.maps.event.addListener(point, 'click', function() {
            infoWindow.open(map, point);
        });  
        bounds.extend(location);
        markers.push(point); 
    });
    map.fitBounds(bounds);
    google.maps.event.addListener(map, 'tilesloaded', function() {
        $.mobile.hidePageLoadingMsg();
    });
}

function loadStop(url) {
    $.mobile.showPageLoadingMsg();
    $.getJSON( url )
    .success(function(data) { loadedStop(data); })
    .error(function() { failure('Error retriving nearby cars'); } );
}

function loadedStop(data) {
    $('#stop-description').html(data.description);
    $('#car-list li[data-role!=list-divider]').remove(); 
    var list = $('#car-list');
    $.each(data.cars_nearby, function(index, car) {
        var link = $('<a href="">' + car.number + '</a>'); 
        link.click(function(event) { checkInConfirm(car.number, 
                                                    data.number,
                                                    car.checkin_url)
                                   });
        list.append($('<li />').append(link));
        console.debug(car.number);
    });

    $.mobile.hidePageLoadingMsg();
    $.mobile.changePage($('#stop'));
    list.listview('refresh');
}

function checkInConfirm(carNumber, stopNumber, url) {
    $('#confirm-title').html('Check in on ' + carNumber);   
    $('#confirm-confirm').html('Check in');
    $('<a href="#confirm" data-rel="dialog" />').click();
}

function loadCheckIn(stop,url) {
       
}

$( document ).ready(init);
