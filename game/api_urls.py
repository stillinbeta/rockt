from django.conf.urls.defaults import *

from rockt.game.views.api.car import *
from rockt.game.views.api.stop import StopView, StopFindView
from rockt.game.views.api.user import UserCarListView, UserCarView, UserView


urlpatterns = patterns('api',
    url(r'^car/checkout/$',
        CheckOutView.as_view(),
        name='car-checkout'),
    url(r'^car/(?P<number>[^/]+)/checkin/$',
        CarCheckInView.as_view(),
        name='car-checkin'),
    url(r'^car/(?P<number>[^/]+)/sell/$',
        CarSellView.as_view(),
        name='car-sell'),
    url(r'^car/(?P<number>[^/]+)/buy/$',
        CarBuyView.as_view(),
        name='car-buy'),
    url(r'^car/(?P<number>[^/]+)/timeline/$',
        CarTimelineView.as_view(),
        name='car-timeline'),
    url(r'^stop/(?P<number>[^/]+)/$',
        StopView.as_view(),
        name='stop'),
    url(r'^stop/find/(?P<lat>[^/]+)/(?P<lon>[^/]+)/$',
        StopFindView.as_view(),
        name='stop-find'),
    url(r'^user/$',
        UserView.as_view(),
        name='user'),
    url(r'^user/car/$',
        UserCarListView.as_view(),
        name='user-car-list'),
    url('^user/car/(?P<number>[^/]+)/$',
        UserCarView.as_view(),
        name='user-car'),
)
