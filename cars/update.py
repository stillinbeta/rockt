from urllib import urlopen
from xml.dom import minidom

import Geohash

from rockt.cars.models import Car

API_URL = 'http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=ttc&r=%&t=0'

def remove_out_of_service(cars_updated):
    all_streetcars = Car.objects.filter(active__exact = True).all()

    to_remove = []
    for streetcar in all_streetcars:
        if streetcar.number not in cars_updated:
            to_remove.append(streetcar.number)
            print "Removing inactive car %s" % streetcar.number
    if to_remove:
        for number in to_remove:
            car = Car(number=number, active=False)
            car.save()


def update_streetcars(route_list):
    cars_updated = []

    response = urlopen(API_URL)
    tree = minidom.parse(response)

    for vehicle in tree.getElementsByTagName('vehicle'):
        if (vehicle.getAttribute('routeTag') in route_list and
            vehicle.getAttribute('predictable') == u'true'):
            car_id = vehicle.getAttribute('id')
            car = Car()
            car.number = vehicle.getAttribute('id')
         #   car.location = (float(vehicle.getAttribute('latitude')),
         #                   float(vehicle.getAttribute('longitude')))
            car.location = [float(vehicle.getAttribute(i)) for i in (
                                                            'lon',
                                                            'lat')]
            car.route = vehicle.getAttribute('routeTag')
            car.active = True
            car.geohash = Geohash.encode(*car.location)
            cars_updated.append(int(car.number))
            print "Car %s in service" % car_id
            car.save()

    return cars_updated 




