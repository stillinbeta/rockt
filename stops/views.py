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
        
        cars =  Car.objects.find_nearby(context['object'].route,
                                        (float(context['object'].longitude),
                                         float(context['object'].latitude)))[:LIMIT]
        context['nearby_cars'] = cars
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
    


import math

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc 
