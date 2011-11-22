//var api_url = 'https://rockt.ca/api/'
//var apiUrl = 'http://192.168.111.156:8000/api/'
apiUrl = '/api/'

var markers = [];
var map;


(function($) {
    
    $.fn.authAjax= function(url) {
        var username = localStorage.getItem('username'); 
        var password = localStorage.getItem('password'); 
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
        })
        .error(failure);
    }
})(jQuery);

// Make a jQuery Mobile button with the given text
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

// Load the google maps object. 
// data is an array of objects with a location array [lon, lat]
// title is the title of the page
// infoFunc is a callback for the popup box. It takes an object as an argument
function loadMap(data, title, infoFunc) {
    $('#map-name').text(title); 
    $.mobile.changePage($('#map'));
    $('#map-content').css('padding','0');
    $('#map-content').height($('#map').height() - $('#map div:first').height() - 2);
    if (!map) {
        var latlng = new google.maps.LatLng(43.6547, -79.3739);
        var myOptions = { 
            center: latlng,
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById('map-content'),
                myOptions); 
    }
    $.each(markers, function(index, point) {
            point.setMap(null);
            });
    markers = []; 
    var bounds = new google.maps.LatLngBounds();
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

// Fill a list with objects
// data the list of objects
// header the header for the page
// title header for the list 
// itemfunc a callback that takes an object
// itemBind  a function to bind to each item, it also takes an object
function loadList(data, header, title, itemFunc, itemBind) {
    $('#list-description').text(header);
    $('#list-name').text(title);
    $('#list-list li[data-role!=list-divider]').remove(); 

    var list = $('#list-list');
    $.each(data, function(index, car) {
            var link = $('<a />').text(itemFunc(car)); 
            link.bind('tap', itemBind(car));
            list.append($('<li />').append(link));
            });

    $.mobile.hidePageLoadingMsg();
    $.mobile.changePage($('#list'));
    list.listview('refresh');
}


// Display an error message as a dialog
// message the error to display
function error(message) {
    $('#error-content').text(message);
    $('<a href="#error" data-rel="dialog" />').click();
}

// Given a failed AJAX response, show a dialog
// jqXHR the failed response
function failure(jqXHR) {
    if (jqXHR.status == 403) {
        login();
        return; 
    }
    try {
        var message = jqXHR.status +': ' 
            + $.parseJSON(jqXHR.responseText).detail
    }
    catch(e) {
        var message = jqXHR.status + ': Something bad happened';
    }
    error(message);
}

// Confirm something
// message the message for the confirm box
// button the text for the button
// handler the handler for the button
function confirmation(message, button, handler) {
    $('#confirm-title').html(message);   
    $('#confirm-confirm').replaceWith(makeButton(button, 'confirm-confirm')
            .attr('data-icon', 'check')
            .one('tap', handler));
    $('<a href="#confirm" data-rel="dialog" />').click();
}

// Retrieve a user's username and balance and apply it to the footer
function loadUserData() {
    $.fn.authAjax(apiUrl + 'user/', {}, 'GET')
    .success(loadedUserData);

    function loadedUserData(data) {
        $('.footer').html( data.username + ' | $' + data.balance ); 
        if (data.check_out_url) {
            var button = makeButton('Check Out', 'home-checkinout');
        } 
        else {
            var button = makeButton('Check In', 'home-checkinout');
        }
        button.unbind('tap').bind('tap', findMe);
        $('#home-checkinout').replaceWith(button);
        $.mobile.hidePageLoadingMsg();
    }
}

// Display the login page
function login() {
    $('#login-submit').one("tap", function () {
        localStorage.setItem('username', $('#username').val());
        localStorage.setItem('password', $('#password').val());
        loadUserData();
        $.mobile.changePage($('#home'));

    }); 
    $.mobile.changePage($('#login'));
}

// Initailize the application
function init() {
    $.mobile.showPageLoadingMsg();
    loadUserData();
    $.mobile.changePage('#home');
}

$(document).ready(init);
 
// Initalize the GPS and load the stop list
function findMe() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(loadStopList, error); 
    }
    else {
        error("You can't geolocate. This game will not be much fun");
    }
    
    function loadStopList(position) {
        $.mobile.showPageLoadingMsg();
        jQuery.getJSON( apiUrl + 'stop/find/' + position.coords.latitude
                        + '/' + position.coords.longitude + '/')
        .success(loadedStopList)
        .error(failure);
    }

    function loadedStopList(data) { 
        loadMap(data, 'Select a stop', function (stop) {
            return '<a style="color: black;" href="javascript:loadStop(\''
                + stop.url + '\')">' + stop.description + ' (' 
                + stop.number + ')</a>';
        });
    
    }
  
}

// Load a stop page
// url the url to the stop page
function loadStop(url) {
    $.mobile.showPageLoadingMsg();
    $.fn.authAjax(url, {}, 'GET')
    .success(loadedStop);

    function loadedStop(data) {
        if (data.checkout_url) {
            checkOutConfirm(data.number, data.checkout_url);
        }
        else {
            loadList(data.cars_nearby,
                     'Check in',
                     data.description,
                     function (car) { return car.number },
                     function (car) { 
                         return function() {
                             checkInConfirm(car.number,
                                            data.number,
                                            car.checkin_url)
                         }
                    }
            );
        }
    }
}

// Confirm a checkin 
// carnumber the number to check in on
// stopNumber the current stop
// url the url for the checkin
function checkInConfirm(carNumber, stopNumber, url) {
    confirmation(carNumber,
                 'Check in',
                 function() {
                    checkIn(stopNumber, url);
                 });

    function checkIn(stopNumber, url) {
        $.mobile.showPageLoadingMsg();
        $.fn.authAjax(url, {'stop_number': stopNumber})
        .success(function() {
            loadUserData();
            $.mobile.changePage($('#home'))
        });
    }
}
    
// Confirm a checkout
// stopnumber the current stop
// url the url to check out on
function checkOutConfirm(stopNumber, url) {
    confirmation('Check out',
                 'Check out',
                 function() {
                     console.debug(url);
                     checkOut(stopNumber, url);
                 }); 
    $.mobile.hidePageLoadingMsg();

    function checkOut(stopNumber, url) {
        $.mobile.showPageLoadingMsg();
        $.fn.authAjax(url, {stop_number: stopNumber})
        .success(function(data) {
            loadUserData();
            checkedOut(data);
        });
    }

    function checkedOut(data) {
        $('#checkedout-fare').text(data.fare);
        if (data.purchase) {
            $('#purchase-div').show();
            $('#purchase-price').text(data.purchase.price);
            $('#purchase-link').unbind('tap').bind('tap', function() {
                purchaseConfirm(data.purchase.url);
            });
        }
        else {
            $('#purchase-div').hide(); 
        }
        $.mobile.changePage($('#checkedout'));
    }
}
    
// Confirm a purchase
// url the URL to post the purchase to
function purchaseConfirm(url) {
    confirmation('Purchase?',
                 'Purchase',
                 function() {
                     purchase(url);
                 });

    function purchase(url) {
        $.mobile.showPageLoadingMsg();
        $.fn.authAjax(url)
        .success(function(data) {
            loadUserData();
            $.mobile.changePage($('#home'));
        });
    }
}

// Show a map of your fleet
function loadFleetMap() {
    $.mobile.showPageLoadingMsg();
    $.fn.authAjax(apiUrl + 'user/car/', {}, 'GET')
    .success(loadedFleetMap);

    function loadedFleetMap(data) {
        loadMap(data, 'Fleet', function(car) {
            return '<a href onclick="loadCar(\'' + car.stats_url+ '\')"' 
                   + ' style="color: black">Car ' + car.number + '</a>';
        });
    }
}

// Show a list of your fleet
function loadFleet() {
    $.mobile.showPageLoadingMsg();
    $.fn.authAjax(apiUrl + 'user/car/', {}, 'GET')
    .success(loadedFleet);

    function loadedFleet(data) {
        loadList(data,
                 'Fleet',
                 'Fleet',
                 function (car) { return car.number },
                 function (car) { return function() { loadCar(car.stats_url); }}
        );
    }
}

// Load a car information page
// url a car's stats_url 
function loadCar(url) {
    $.mobile.showPageLoadingMsg();
    $.fn.authAjax(url, {}, 'GET')
    .success(loadedCar);

    function loadedCar(data) {
        $('#car-route').text(data.route);
        $('#car-active').text(data.active && 'Active' || 'Inactive');

        $('#car-owner-revenue').text(data.owner_fares.revenue);
        $('#car-total-revenue').text(data.total_fares.revenue);
                
        $('#car-owner-riders').text(data.owner_fares.riders);
        $('#car-total-riders').text(data.total_fares.riders);

        $('#car-sell').unbind('tap')
        .bind('tap', function() { 
            confirmSell(data.sell_car_url,
                        data.number);
        });
                            

        $.mobile.changePage($('#car'));
        $.mobile.hidePageLoadingMsg();
    }            
}

// Confirm a sale
// url the URL to post the sale to
// number the number of the car being sold
function confirmSell(url, number) {
    confirmation('Sell ' + number + '?',
                 'Sell',
                 function() { sell(url); });


    function sell(url) {
        $.mobile.showPageLoadingMsg();
        $.fn.authAjax(url)
        .success(sold);

        
    }

    function sold() {
            loadUserData();
            loadFleet();
    }

}
