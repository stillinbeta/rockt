from djangorestframework.resources import ModelResource, Resource
from game.models import Stop, Car
from django.contrib.auth.models import User
from djangorestframework.views import View
from djangorestframework.mixins import AuthMixin
from djangorestframework.authentication import BasicAuthentication
from djangorestframework.permissions import IsAuthenticated

from game.util import protect_method_digest_model 
class StopResource(ModelResource):
    model = Stop
    fields = ('number', 'route', 'description', 'location', 'cars_nearby')
    ordering = 'number'

    def cars_nearby(self, instance):
         return [{'number':car.number,
                  'location':car.location,} for 
                  car in  Car.objects.find_nearby(instance)[:10]]

class CheckInView(View,AuthMixin):
    authentication = (BasicAuthentication,)
    permissions = (IsAuthenticated,)
    def get(self, request, number):
        return {'logged_in':self.user.username}
class CheckOutView(View):
    def post(self, request):
        raise Exception
