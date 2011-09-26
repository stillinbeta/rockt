from django.conf.urls.defaults import *
from django.contrib import admin

#Django View Helpers
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',

        (r'^admin/', include(admin.site.urls)),
	(r'^$', direct_to_template, {'template' : 'map.html'}),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/home/sib/Devel/sibcom/static'}),

)
