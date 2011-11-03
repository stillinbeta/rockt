import json

from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from djangohttpdigest.decorators import protect_digest_model

from game.models import Car, Stop

# Create your views here.

GEOHASH_LENGTH = 5
LIMIT = 8


class StopDetailedView(DetailView):
    model = Stop
    slug_field = 'number'

    def get_context_data(self, **kwargs):
        context = super(StopDetailedView, self).get_context_data(**kwargs)
        cars = Car.objects.find_nearby(context['object'])[:LIMIT]
        context['nearby_cars'] = cars
        return context


def nearby_stops(request, lat, lon):
    stops = Stop.objects.find_nearby((float(lon), float(lat)))[:LIMIT]
    context = {'lat': lat,
               'lon': lon,
               'stops': stops
              }
    return render_to_response('station_finder.html', context)


def car_locations(request):
    cars = Car.objects.filter(active__exact=True).all()
    car_info = dict
    for car in cars:
        car_info[car.number] = {'lon': car.location[0],
                                'lat': car.location[1]}

    return HttpResponse(json.dumps(car_info), mimetype='application/json')
