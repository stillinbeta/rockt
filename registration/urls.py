from django.conf.urls.defaults import *

#Django View Helpers
from django.views.generic import DetailView, ListView
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('registration',
    url(r'^$', 'views.waiting_list', name='waiting-list'),
    url(r'^(?P<key>[^/]+)/$', 'views.register', name='register')
)
