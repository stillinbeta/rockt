from djangorestframework.views import View 
from djangorestframework.response import ErrorResponse

from game.models import Stop

class StopFindView(View):
    def get(self, request, lat, lon):
        try:
            location = (float(lon), float(lat))
        except ValueError:
            raise ErrorResponse(400, {'detail': 'Invalid Coordinates'})

        return Stop.objects.find_nearby(location)
