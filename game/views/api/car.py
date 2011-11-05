from django.contrib.auth.models import User
from djangorestframework.views import View
from djangorestframework.response import ErrorResponse

from game.util import get_model_or_404, get_key_or_400
from game.models import Stop, Car, UserProfile, Event
from game.views.api.common import AuthRequiredView


class CarCheckInView(AuthRequiredView):
    def post(self, request, number):
            car = get_model_or_404(Car, number=number)

            stop_number = get_key_or_400(request.POST, 'stop_number')
            stop = get_model_or_404(Stop, number=stop_number)

            userprofile = self.user.get_profile()
            userprofile.check_in(car, stop)
            return {'status': 'ok'}


class CheckOutView(AuthRequiredView):
    def post(self, request):
        stop_number = get_key_or_400(request.POST, 'stop_number')
        stop = get_model_or_404(Stop, number=stop_number)
        try:
            self.user.get_profile().check_out(stop)
            return {'status': 'ok'}
        except UserProfile.NotCheckedInException:
            raise ErrorResponse(400, {'detail': 'User is not checked in'})


class CarSellView(AuthRequiredView):
    def post(self, request, number):
        car = get_model_or_404(Car, number=number)

        try:
            car.sell_to(self.user)
        except Car.NotAllowedException:
            raise ErrorResponse(403,
                {'detail': 'You are not allowed to purchase this car'})
        except UserProfile.InsufficientFundsException:
            raise ErrorResponse(403, {'detail': 'You cannot afford this car'})
        else:
            return {'status': 'ok'}


class CarBuyView(AuthRequiredView):
    def post(self, request, number):
        car = get_model_or_404(Car, number=number)

        try:
           # import pdb; pdb.set_trace()
            car.buy_back(self.user)
        except Car.NotAllowedException:
            raise ErrorResponse(403,
                {'detail': 'This car doesn not belong to you'})
        else:
            return {'status': 'ok'}


class CarTimelineView(View):
    def get(self, request, number):
        car = get_model_or_404(Car, number=number)

        for event in Event.objects.get_car_timeline(car):
            yield {'user': event.data.get('user'),
                   'event': event.event,
                   'date': event.date}