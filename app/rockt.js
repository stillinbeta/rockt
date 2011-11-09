var api_url = 'https://rockt.ca/api/'

function add_footer() {
    $('.footer').html('stillinbeta | $00');
}

function init() {
    add_footer();
}

function error(message) {
    $('#error-content').html(message);
    $('<a href="#error" data-rel="dialog" />').click();
}
    

function loadStops() {
    $.mobile.showPageLoadingMsg();
    jQuery.ajax( api_url + 'stop/43.64903/-79.3967/')
    .success(function() { loadedStops(); })
    .error(function() { error('Oops'); } );
}
    
function loadedStops() {
    $.mobile.hidePageLoadingMsg();
    $.mobile.changePage($('#loaded'));
}

function go_to_loading() {
}

$( document ).ready(init);
