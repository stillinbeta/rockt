import Geohash
from django.views.generic import DetailView
from django.shortcuts import render_to_response

from rockt.stops.models import Stop
from rockt.cars.models import Car

# Create your views here.

GEOHASH_LENGTH=5
LIMIT=10


class StopDetailedView(DetailView):
    model = Stop
    slug_field = 'number'
    
    def get_context_data(self, **kwargs):
        context = super(StopDetailedView,self).get_context_data(**kwargs)
        
        cars =  Car.objects.filter(
            geohash__startswith = context['object'].geohash[0:GEOHASH_LENGTH],
            route__exact = context['object'].route
        )
        context['nearby_cars'] = cars.order_by('geohash')[:LIMIT]
        return context

def locate(request, lat, lon):
    stops = Stop.objects.filter(
        geohash__startswith = Geohash.encode(float(lat),float(lon),6)
    ).order_by('geohash')[:LIMIT]
    context = {'lat' : lat,
               'lon' : lon,
               'stops' : stops
              }
    return render_to_response('station_finder.html',context)
    


    
