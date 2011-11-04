from djangorestframework.response import ErrorResponse
from djangorestframework.mixins import InstanceMixin

from game.util import get_model_or_404
from game.views.api.common import AuthRequiredView, ReadOnlyModelView
from game.resources import UserResource, UserCarResource


class UserCarListView(AuthRequiredView):
    def get(self, request):
        for car in self.user.get_profile().car_set.all():
            yield {'car': car.number, 'location': car.location}


class UserCarView(AuthRequiredView, InstanceMixin):
    resource = UserCarResource

    def get(self, request, number):
        model = self.resource.model
        model_instance = get_model_or_404(model, number=number)

        #Only the car's owner can view detailed information
        if not model_instance.owner == self.user.get_profile():
            raise ErrorResponse(403, {'detail': 'You do not own this car'})
        return model_instance
