from djangorestframework.resources import ModelResource
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings

from game.models import Stop, Car


class StopResource(ModelResource):
    model = Stop
    fields = ('number', 'route', 'description', 'location', 'cars_nearby')
    ordering = 'number'

    def cars_nearby(self, instance):
        limit = settings.CAR_SEARCH_LIMIT
        for car in Car.objects.find_nearby(instance)[:limit]:
            yield {'number': car.number,
                   'location': car.location,
                   'checkin_url': reverse('car-checkin', args=(car.number,))}


class StopFindResource(ModelResource):
    model = Stop
    fields = ('number', 'route', 'description', 'location', 'url')

    def url(self, instance):
        return reverse('stop', args=(instance.number,))


class UserResource(ModelResource):
    model = User
    fields = ('username', 'balance')

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
