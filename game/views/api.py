from django.contrib.auth.models import User
from djangorestframework.views import View
from djangorestframework.mixins import AuthMixin
from djangorestframework.authentication import BasicAuthentication
from djangorestframework.permissions import IsAuthenticated
from djangorestframework.response import ErrorResponse

from game.util import get_model_or_404, get_key_or_400
from game.models import Stop, Car, UserProfile


class AuthRequiredView(View, AuthMixin):
    authentication = (BasicAuthentication,)
    permissions = (IsAuthenticated,)


class CheckInView(AuthRequiredView):
    def post(self, request):
            stop_number = get_key_or_400(request.POST,'stop_number')
            car_number = get_key_or_400(request.POST,'car_number')

            stop = get_model_or_404(Stop, number=stop_number)
            car = get_model_or_404(Car, number=car_number)
            
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


class StopFindView(View):
    def get(self, request, lat, lon):
        try:
            location = (float(lon), float(lat))
        except ValueError:
            raise ErrorResponse(400, {'detail': 'Invalid Coordinates'})

        return Stop.objects.find_nearby(location)


class SellCarView(AuthRequiredView):
    def post(self, request):
        car_number = get_key_or_400(request.POST,'car_number')
        car = get_model_or_404(Car, number=car_number)

        try:
            car.sell_to(self.user)
        except Car.NotAllowedException:
            raise ErrorResponse(403, 
                {'detail': 'You are not allowed to purchase this car'})
        except UserProfile.InsufficientFundsException:
            raise ErrorResponse(403, {'detail': 'You cannot afford this car'})
        else:
            return {'status': 'ok'}

class BuyCarView(AuthRequiredView):
    def post(self, request):
        car_number = get_key_or_400(request.POST,'car_number')
        car = get_model_or_404(Car, number=car_number)

        try:
           # import pdb; pdb.set_trace()
            car.buy_back(self.user)
        except Car.NotAllowedException:
            raise ErrorResponse(403,
                {'detail': 'This car doesn not belong to you'})
        else:
            return {'status': 'ok'}
            
            
        
