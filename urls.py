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
from rockt.game.views.api.user import UserCarListView, UserCarView, UserView

urlpatterns = patterns('',

    (r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^map/$', 'game.views.web.fleet_map', name='map'),
    url(r'^fleet/$', 'game.views.web.fleet', name='fleet'),
    url(r'^fleet/(?P<number>[^/]+)/$', 'game.views.web.car', name='car'),
    url(r'^fleet/(?P<number>[^/]+)/sell/$',
        'game.views.web.sell',
        name='sell'),
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
        UserView.as_view(),
        name='user'),
    url(r'^api/user/car/$',
        UserCarListView.as_view(),
        name='user-car-list'),
    url('^api/user/car/(?P<number>[^/]+)/$',
        UserCarView.as_view(),
        name='user-car'),
    ('^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/sib/Devel/rockt/static'})
)
