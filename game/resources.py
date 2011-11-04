from djangorestframework.resources import ModelResource
from django.contrib.auth.models import User

from game.models import Stop, Car


class StopResource(ModelResource):
    model = Stop
    fields = ('number', 'route', 'description', 'location', 'cars_nearby')
    ordering = 'number'

    def cars_nearby(self, instance):
        for car in Car.objects.find_nearby(instance)[:10]:
            yield {'number': car.number, 'location': car.location}


class UserResource(ModelResource):
    model = User
    fields = ('username', 'balance',)

    def balance(self, instance):
        return instance.get_profile().balance


class UserCarResource(ModelResource):
    model = Car
    fields = ('route', 'active', 'number', 'owner_fares', 'total_fares',
              'location')
    #exclude = ('owner', 'owner_fares', 'total_fares')

    def owner_fares(self, instance):
        return {'revenue': instance.owner_fares.revenue,
                'riders': instance.owner_fares.riders}

    def total_fares(self, instance):
        return {'revenue': instance.total_fares.revenue,
                'riders': instance.total_fares.riders}
