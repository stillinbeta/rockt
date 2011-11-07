from django.conf.urls.defaults import *
from django.views.generic.list import ListView
#from django.views.generic.detail import DetailView

from models import Post

urlpatterns = patterns('blog',
    url(r'^$',
        ListView.as_view(model=Post,
                         paginate_by=10,
                         template_name='blog.html'),
        name='blog'),
)
