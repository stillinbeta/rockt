from urllib import urlopen
from xml.dom import minidom

from django.core.management.base import BaseCommand
from django.conf import settings

from game.models import Car,FareInfo


class Command(BaseCommand):
    help = 'Update the positions of the streetcars'

    def handle(self,*args,**kwargs):
        route_list = settings.NEXTBUS_ROUTE_LIST
        cars_updated = self.update_streetcars(route_list)
        self.stdout.write("Update is Complete, %d cars in service\n" 
            % len(cars_updated))
        self.remove_out_of_service(cars_updated)
        self.stdout.write("Removal Complete\n")


    def remove_out_of_service(self,cars_updated):
        all_streetcars = Car.objects.filter(active__exact = True).all()

        to_remove = []
        for streetcar in all_streetcars:
            if streetcar.number not in cars_updated:
                to_remove.append(streetcar.number)
                self.stdout.write("Removing inactive car %s\n" % streetcar.number)
        if to_remove:
            for number in to_remove:
                car = Car.objects.get(number=number)
                car.active = False
                car.save()


    def update_streetcars(self,route_list):
        cars_updated = []

        response = urlopen(settings.NEXTBUS_API_URL)
        tree = minidom.parse(response)

        for vehicle in tree.getElementsByTagName('vehicle'):
            if (vehicle.getAttribute('routeTag') in route_list and
                vehicle.getAttribute('predictable') == u'true'):
                car_id = vehicle.getAttribute('id')
                try: 
                    car = Car.objects.get(number=car_id)
                except Car.DoesNotExist:
                    car = Car()
                    car.owner_fares = FareInfo()
                    car.total_fares = FareInfo()
                    
                car.number = vehicle.getAttribute('id')
                car.location = [float(vehicle.getAttribute(i)) for i in (
                                                                'lon',
                                                                'lat')]
                car.route = vehicle.getAttribute('routeTag')
                car.active = True
                cars_updated.append(int(car.number))
                self.stdout.write("Car %s in service\n" % car_id)
                car.save()

        return cars_updated 
