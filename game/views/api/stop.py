from djangorestframework.views import View
from djangorestframework.response import ErrorResponse
from djangorestframework.mixins import ListModelMixin
from django.conf import settings

from game.models import Stop
from game.resources import StopFindResource


class StopFindView(View, ListModelMixin):
    resource = StopFindResource

    def get(self, request, lat, lon):
        try:
            location = (float(lon), float(lat))
        except ValueError:
            raise ErrorResponse(400, {'detail': 'Invalid Coordinates'})

        return Stop.objects.find_nearby(location)[:settings.STOP_SEARCH_LIMIT]
