from django.conf.urls.defaults import *
from django.contrib import admin

#Django View Helpers
from django.views.generic import DetailView, ListView
from django.views.generic.simple import direct_to_template
admin.autodiscover()

from rockt.game.models import Car, Stop
from rockt.game.resources import StopResource, UserResource 
from rockt.game.views.api.car import *
from rockt.game.views.api.common import ReadOnlyModelView
from rockt.game.views.api.stop import StopFindView
from rockt.game.views.api.user import UserCarListView

urlpatterns = patterns('',

    (r'^admin/', include(admin.site.urls)),
    url(r'^api/car/checkout/$',
        CheckOutView.as_view(),
        name='car-checkout'),
    url(r'^api/car/(?P<number>[^/]+)/checkin/$',
        CarCheckInView.as_view(),
        name='car-checkin'),
    url(r'^api/car/(?P<number>[^/]+)/sell/$',
        CarSellView.as_view(),
        name='car-sell'),
    url(r'^api/car/(?P<number>[^/]+)/buy/$',
        CarBuyView.as_view(),
        name='car-buy'),
    url(r'^api/car/(?P<number>[^/]+)/timeline/$',
        CarTimelineView.as_view(),
        name='car-timeline'),
    url(r'^api/stop/(?P<number>[^/]+)/$',
        ReadOnlyModelView.as_view(resource=StopResource),
        name='stop'),
    url(r'^api/stop/find/(?P<lat>[^/]+)/(?P<lon>[^/]+)/$',
        StopFindView.as_view(),
        name='stop-find'),
    url(r'^api/user/$',
        ReadOnlyModelView.as_view(resource=UserResource),
        name='user'),
    url(r'^api/user/car/$',
        UserCarListView.as_view(),
        name='user-car'),
)
