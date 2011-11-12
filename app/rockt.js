//var api_url = 'https://rockt.ca/api/'
//var apiUrl = 'http://192.168.111.156:8000/api/'
apiUrl = '/api/'
var markers = [];
var map;
var bounds;
var username='ellie';
var password='test';

(function($) {
    $.fn.authAjax= function(url) {
        if (!arguments[1]) {
            arguments[1] = {}
        }
        data = arguments[1];

        if (!arguments[2]) {
            arguments[2] = 'POST'
        }
        method = arguments[2]; 

        return $.ajax(url, {
            data: data,
            type: method, 
            beforeSend: function(xhr) { 
                xhr.setRequestHeader("Authorization",
                    "Basic " + $.base64Encode(username + ':' + password));
            }
        });
    }
})(jQuery);

function makeButton(text) {
    var button = $('<a />')
    .text(text)
    .attr('data-role', 'button')
    .attr('data-theme', 'a')
    .buttonMarkup();
    if (arguments[1]) {
        button.attr('id', arguments[1]);
    }
    return button;
}

function addFooter() {
    $('.footer').html('stillinbeta | $00');
}

function init() {
    $.mobile.showPageLoadingMsg();
    addFooter();
    loadUserData();
    $.mobile.changePage('#home');
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

function failure(jqXHR) {
    try {
        var message = jqXHR.status +': ' 
            + $.parseJSON(jqXHR.responseText).detail
    }
    catch(e) {
        var message = jqXHR.status + ': Something bad happened';
    }
    $('#error-content').text(message);
    $('<a href="#error" data-rel="dialog" />').click();
}
    
function loadStopList() {
    $.mobile.showPageLoadingMsg();
    jQuery.getJSON( apiUrl + 'stop/find/43.64903/-79.3967/')
    .success(function(data) { loadedStopList(data) } )
    .error(failure);
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
    .success(loadedStop)
    .error(failure);
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
    });

    $.mobile.hidePageLoadingMsg();
    $.mobile.changePage($('#stop'));
    list.listview('refresh');
}

function checkInConfirm(carNumber, stopNumber, url) {
    $('#confirm-title').html('Check in on ' + carNumber);   
    $('#confirm-confirm').val('Check in').bind('tap', function() {
        checkIn(stopNumber, url);
    });
    $('<a href="#confirm" data-rel="dialog" />').click();
}

function checkIn(stopNumber, url) {
    $.mobile.showPageLoadingMsg();
    $.fn.authAjax(url, {'stop_number': stopNumber})
    .success(checkedIn)
    .error(failure);
}
function loadUserData() {
    $.fn.authAjax(apiUrl + 'user/', {}, 'GET')
    .success(loadedUserData)
    .error(failure);
}
    
function checkedIn() {
    $('#home-checkinout')
    .replaceWith(makeButton('Check out', 'home-checkinout'));
    $.mobile.hidePageLoadingMsg();
    $.mobile.changePage($('#home'));
}

function loadedUserData(data) {
    $('.footer').html( data.username + ' | $' + data.balance ); 
    if (data.check_out_url) {
        var button = makeButton('Check Out', 'home-checkinout');
    } 
    else {
        var button = makeButton('Check In', 'home-checkinout');
    }
    $('#home-checkinout').replaceWith(button);
    $.mobile.hidePageLoadingMsg();
}



$(document).ready(init);
