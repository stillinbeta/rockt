from djangorestframework.resources import ModelResource

from game.models import Stop,Car

class StopResource(ModelResource):
    model = Stop
    fields = ('number', 'route', 'description', 'location', 'cars_nearby')
    ordering = 'number'

    def cars_nearby(self, instance):
         return [{'number':car.number,
                  'location':car.location,} for 
                  car in  Car.objects.find_nearby(instance)[:10]]

