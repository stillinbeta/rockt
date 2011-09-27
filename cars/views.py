import json 
import logging
from django.http import HttpResponse

from rockt.cars.models import Car

# Create your views here.

def locations(request):
    cars = Car.objects.filter(active__exact=True).all()
    car_info = dict()
    for car in cars:
        car_info[car.number] ={'lat' : car.latitude, 'lon' : car.longitude} 
                                             
    return HttpResponse(json.dumps(car_info),mimetype='application/json')

