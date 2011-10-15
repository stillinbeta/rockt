import Geohash
from django.views.generic import DetailView
from django.shortcuts import render_to_response

from rockt.stops.models import Stop
from rockt.cars.models import Car

# Create your views here.

GEOHASH_LENGTH=5
LIMIT=8


class StopDetailedView(DetailView):
    model = Stop
    slug_field = 'number'
    
    def get_context_data(self, **kwargs):
        context = super(StopDetailedView,self).get_context_data(**kwargs)
        
        cars =  Car.objects.find_nearby(context['object'])[:LIMIT]
        context['nearby_cars'] = cars
        return context

def locate(request, lat, lon):
    stops = Stop.objects.find_nearby((float(lon),float(lat)))[:LIMIT]
    context = {'lat' : lat,
               'lon' : lon,
               'stops' : stops
              }
    return render_to_response('station_finder.html',context)
    
