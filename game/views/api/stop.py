from djangorestframework.views import View
from djangorestframework.response import ErrorResponse
from djangorestframework.mixins import ListModelMixin
from django.conf import settings
from django.core.urlresolvers import reverse

from game.models import Stop, Car
from game.util import get_model_or_404
from game.resources import StopFindResource
from game.views.api.common import AuthRequiredView


class StopFindView(View, ListModelMixin):
    resource = StopFindResource

    def get(self, request, lat, lon):
        try:
            location = (float(lon), float(lat))
        except ValueError:
            raise ErrorResponse(400, {'detail': 'Invalid Coordinates'})

        return Stop.objects.find_nearby(location)[:settings.STOP_SEARCH_LIMIT]


class StopView(AuthRequiredView):
    fields = ('number', 'route', 'description', 'location')

    def get(self, request, number):
        stop = get_model_or_404(Stop, number=number)
        dic = dict()
        for field in self.fields:
            dic[field] = getattr(stop, field)

        if self.user.get_profile().riding != None:
            dic['checkout_url'] = reverse('car-checkout')
        else:
            dic['cars_nearby'] = []
            limit = settings.CAR_SEARCH_LIMIT
            checked_in = self.user.get_profile().riding != None
            for car in Car.objects.find_nearby(stop)[:limit]:
                car_dic = {'number': car.number,
                          'location': car.location,
                          'checkin_url': reverse('car-checkin',
                                                 args=(car.number,))}
                dic['cars_nearby'].append(car_dic)

        return dic
