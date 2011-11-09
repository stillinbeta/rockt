//var api_url = 'https://rockt.ca/api/'
var apiUrl = 'http://localhost:8000/api/'


function addFooter() {
    $('.footer').html('stillinbeta | $00');
}

function init() {
    addFooter();
    initMap();

}

function initMap() {
    $('#map-content').css('padding','0');
    $('#map-content').height($('#map').height() - $('#map div:first').height() - 2);
    var latlng = new google.maps.LatLng(43.6547, -79.3739);
    var myOptions = { 
        zoom: 12,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById('map-content'),
        myOptions); 
    var marker = new google.maps.Marker({
         position: latlng,
         map: map
    });

}

function failure(message) {
    $('#error-content').html(message);
    $('<a href="#error" data-rel="dialog" />').click();
}
    

function loadStops() {
    $.mobile.showPageLoadingMsg();
    jQuery.getJSON( apiUrl + 'stop/find/43.64903/-79.3967/')
    .success(function(data) { loadedStops(data) } )
    .error(function(err) { failure('Error retriving stops'); } );
}
    
function loadedStops(data) {
    $.mobile.hidePageLoadingMsg();
    $.mobile.changePage($('#map'));
}

$( document ).ready(init);
