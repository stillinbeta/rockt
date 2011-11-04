from game.views.api.common import AuthRequiredView
from game.resources import UserResource


class UserCarListView(AuthRequiredView):
    def get(self, request):
        for car in self.user.get_profile().car_set.all():
            yield {'car': car.number}
