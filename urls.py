from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    (r'^admin/', include(admin.site.urls)),
    (r'^registration/', include('registration.urls')),
    (r'^blog/', include('blog.urls')),
    (r'^api/', include('game.api_urls')),
    url(r'^login/', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout',
        {'next_page': '/'},
         name='logout'),
    url(r'^map/$', 'game.views.web.fleet_map', name='map'),
    url(r'^fleet/$', 'game.views.web.fleet', name='fleet'),
    url(r'^fleet/(?P<number>[^/]+)/$', 'game.views.web.car', name='car'),
    url(r'^fleet/(?P<number>[^/]+)/sell/$',
        'game.views.web.sell',
        name='sell'),
    url(r'^profile/$', 'game.views.web.profile', name='profile'),
       ('^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/home/sib/Devel/rockt/static'}),
       ('^m/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/home/sib/Devel/rockt/app'}),
)
