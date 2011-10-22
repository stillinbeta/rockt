from djangorestframework.resources import ModelResource, Resource
from game.models import Stop, Car
from django.contrib.auth.models import User
from djangorestframework.views import View

from game.util import protect_method_digest_model 
class StopResource(ModelResource):
    model = Stop
    fields = ('number', 'route', 'description', 'location', 'cars_nearby')
    ordering = 'number'

    def cars_nearby(self, instance):
         return [{'number':car.number,
                  'location':car.location,} for 
                  car in  Car.objects.find_nearby(instance)[:10]]

class CheckInView(View):
    @protect_method_digest_model(User, 'rockt')
    def get(self, request, number):
        return {'hello':'world'}

class CheckOutView(View):
    @protect_method_digest_model(User, 'rockt')
    def post(self, request):
        raise Exception
