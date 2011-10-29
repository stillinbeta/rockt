from base64 import b64encode

from django.test import TestCase
from django.contrib.auth.models import User

from game.models import Car, Stop, FareInfo, UserProfile

class CheckInOutTests(TestCase):
    check_in_url = '/api/checkin/'
    check_out_url = '/api/checkout/'
    
    def setUp(self):
        username='checkinout'
        password='secret'
        self.user = User.objects.create(username=username,
                         email='joe@bloggs.com')
        self.user.set_password(password)
        self.user.save()
        self.auth_string = 'Basic ' + b64encode('{}:{}'.format(username,
                                                             'secret'))
        self.car = Car.objects.create(
                                number=4211,
                                active=True,
                                location=[ -79.402858, 43.644075 ],
                                owner_fares=FareInfo(),
                                total_fares=FareInfo(),)
        
        self.stop= Stop.objects.create(number="00000",
                                       location=[ -79.402858, 43.644075 ],
                                       route=511)
    def assertAuthRequired(self, url):
        response = self.client.post(url)
        self.assertEquals(response.status_code,403)


    def assertStatusCode(self, url, data, code):
        response= self.client.post(url, data, 
                                    HTTP_AUTHORIZATION=self.auth_string) 
        self.assertEquals(response.status_code, code)


    def test_check_in_requires_auth(self):
        self.assertAuthRequired(self.check_in_url)


    def test_check_in_missing_parameters_gives_400(self):
        self.assertStatusCode(self.check_in_url, {'stop_number':1}, 400)
        self.assertStatusCode(self.check_in_url, {'car_number':1}, 400)
    
    def test_check_in_invalid_info_gives_404(self):
        self.assertStatusCode(self.check_in_url, 
                              {'stop_number': self.stop.number,
                               'car_number': 0},
                              404)
        self.assertStatusCode(self.check_in_url, 
                              {'stop_number': 0, 
                               'car_number': self.car.number},
                              404)
    def test_check_in_creates_riding(self):
        self.assertStatusCode(self.check_in_url, 
                              {'stop_number': self.stop.number, 
                               'car_number': self.car.number},
                              200)
        
        profile = self.user.get_profile()
        self.assertIsNotNone(profile.riding)
        self.assertEquals(profile.riding.car, self.car)
        self.assertEquals(profile.riding.boarded, self.stop)

    def test_check_out_requires_auth(self):
        self.assertAuthRequired(self.check_out_url)

    def test_check_out_missing_stop_gives_400(self):
        self.assertStatusCode(self.check_out_url, {}, 400)

    def test_check_out_invalid_stop_gives_404(self):
        self.assertStatusCode(self.check_out_url, {'stop_number': 0}, 404)

    def test_check_out_not_riding_gives_400(self):
        profile = self.user.get_profile()
        profile.riding = None
        profile.save()
        
        self.assertStatusCode(self.check_out_url, 
                              {'stop_number': self.stop.number}, 
                              400)
    def test_check_out_finishes_ride(self):
        self.assertStatusCode(self.check_in_url, 
                              {'stop_number': self.stop.number, 
                               'car_number': self.car.number},
                              200)
        self.assertStatusCode(self.check_out_url, 
                              {'stop_number': self.stop.number},
                              200)
        self.assertIsNone(self.user.get_profile().riding) 


    def tearDown(self):
        # Because it's important that there only ever be one user by this
        # this username, we delete when we're finished
        self.user.delete()
