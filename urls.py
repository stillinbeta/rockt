from django.conf.urls.defaults import *
from django.contrib import admin

#Django View Helpers
from django.views.generic import DetailView, ListView
from django.views.generic.simple import direct_to_template
admin.autodiscover()

from rockt.game.models import Car,Stop
from rockt.game.views import StopDetailedView


urlpatterns = patterns('',

    (r'^admin/', include(admin.site.urls)),
	(r'^$', direct_to_template, {'template' : 'map.html'}),
    (r'^locations/$','game.views.car_locations'),
    (r'^car/(?P<slug>.+)/$',
        DetailView.as_view(
            model = Car,
            slug_field = 'number',
            template_name = 'car.html',)),
    (r'^stops/locate/$', direct_to_template, {'template' : 'geolocation.html'}),
    (r'^stops/locate/(?P<lat>.+)/(?P<lon>.+)/', 'game.views.nearby_stops'),
    (r'^stops/$',
        ListView.as_view(
            model = Stop,
            context_object_name='stops',
            template_name = 'stops.html')),
    (r'^stop/(?P<slug>.+)/$',
        StopDetailedView.as_view(
            template_name = 'cars_nearby.html')),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/home/sib/Devel/sibcom/static'}),

)
