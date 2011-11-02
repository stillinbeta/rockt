from django.conf.urls.defaults import *
from django.contrib import admin

#Django View Helpers
from django.views.generic import DetailView, ListView
from django.views.generic.simple import direct_to_template
admin.autodiscover()
from djangorestframework.views import InstanceModelView 

from rockt.game.models import Car,Stop
from rockt.game.views.web import StopDetailedView
from rockt.game.resources import StopResource
from rockt.game.views.api import *

urlpatterns = patterns('',

    (r'^admin/', include(admin.site.urls)),
	(r'^$', direct_to_template, {'template' : 'map.html'}),
    (r'^api/stop/(?P<number>[^/]+)/$', 
        InstanceModelView.as_view(resource=StopResource)),
    (r'^api/stop/find/(?P<lat>[^/]+)/(?P<lon>[^/]+)/',
        StopFindView.as_view()),
    (r'^api/checkin/$', CheckInView.as_view()),
    (r'^api/checkout/$', CheckOutView.as_view()),
    (r'^api/car/sell/$', SellCarView.as_view()),
    (r'^locations/$','game.views.web.car_locations'),
    (r'^car/(?P<slug>.+)/$',
        DetailView.as_view(
            model = Car,
            slug_field = 'number',
            template_name = 'car.html',)),
    (r'^stops/locate/$', direct_to_template, {'template' : 'geolocation.html'}),
    (r'^stops/locate/(?P<lat>.+)/(?P<lon>.+)/', 'game.views.web.nearby_stops'),
    (r'^stops/$',
        ListView.as_view(
            model = Stop,
            context_object_name='stops',
            template_name = 'stops.html')),
    (r'^stop/(?P<slug>.+)/$',
        StopDetailedView.as_view(
            template_name = 'cars_nearby.html')),
)
