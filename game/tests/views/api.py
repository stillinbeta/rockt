from base64 import b64encode
import json

from django.test import TestCase
from django.contrib.auth.models import User

from game.models import Car, Stop, UserProfile, Event
from game.tests.utils import temporary_settings

class Tests(TestCase):
    check_in_url = '/api/checkin/'
    check_out_url = '/api/checkout/'
    car_sell_url = '/api/car/sell/'
    car_buy_url = '/api/car/buy/'
    car_timeline_url = '/api/car/timeline/{number}/'
    
    def setUp(self):
        username='checkinout'
        password='secret'
        self.user = User.objects.create(username=username,
                         email='joe@bloggs.com')
        self.user.set_password(password)
        self.user.save()
        self.user2 = User.objects.create(username='heidi',
                                         email='heidi@spam.ca')
        self.auth_string = 'Basic ' + b64encode('{}:{}'.format(username,
                                                             'secret'))
        self.car = Car.objects.create(
                                number=4211,
                                active=True,
                                location=[ -79.402858, 43.644075 ],)
        
        self.stop= Stop.objects.create(number="00000",
                                       location=[ -79.402858, 43.644075 ],
                                       route=511)
    def assertAuthRequired(self, url):
        response = self.client.post(url)
        self.assertEquals(response.status_code,403)


    def assertStatusCode(self, url, data, code):
        response = self.client.post(url, data, 
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


    def test_car_sell_auth_required(self):
        self.assertAuthRequired(self.car_sell_url)


    def test_car_sell_missing_car_gives_400(self):
        self.assertStatusCode(self.car_sell_url, {}, 400)


    def test_car_sell_invalid_car_gives_404(self):
        self.assertStatusCode(self.car_sell_url, {'car_number': 0}, 404)


    def test_car_sell_not_allowed_returns_403(self):
        def fake_rule(*args, **kwargs):
            return False
        with temporary_settings({'RULE_CAN_BUY_CAR': fake_rule}):
            self.assertStatusCode(self.car_sell_url,
                                  {'car_number': self.car.number},
                                  403) 
    
    def test_car_sell_insufficient_funds_returns_403(self):
        profile = self.user.get_profile()
        profile.balance = 0
        profile.save()
        def fake_price(*args, **kwargs):
            return 100
        with temporary_settings({'RULE_GET_STREETCAR_PRICE': fake_price}):
            self.assertStatusCode(self.car_sell_url,
                                  {'car_number': self.car.number},
                                  403)
            
         
    def test_car_sell_transfers_ownership(self):
        self.car.owner = None
        self.car.save()
        
        def fake_rule(*args, **kwargs):
            return True 
        def fake_price(*args, **kwargs):
            return 0
        with temporary_settings({'RULE_CAN_BUY_CAR': fake_rule,
                                 'RULE_GET_STREETCAR_PRICE': fake_price}):
            self.assertStatusCode(self.car_sell_url,
                                  {'car_number': self.car.number},
                                  200)
        self.car = Car.objects.get(number=self.car.number)
        self.assertEquals(self.car.owner, self.user.get_profile())


    def test_car_buy_auth_required(self):
        self.assertAuthRequired(self.car_buy_url)


    def test_car_buy_missing_car_gives_400(self):
        self.assertStatusCode(self.car_buy_url, {}, 400)


    def test_car_buy_invalid_car_gives_404(self):
        self.assertStatusCode(self.car_buy_url, {'car_number': 0}, 404)


    def test_car_buy_not_allowed_returns_403(self):
        self.car.owner = self.user2.get_profile()
        self.car.save()
        self.assertStatusCode(self.car_buy_url,
                              {'car_number': self.car.number},
                              403) 
    def test_car_buy_buys_car(self):
        self.car.owner = self.user.get_profile()
        self.car.save()
        self.assertStatusCode(self.car_buy_url,
                              {'car_number': self.car.number},
                              200) 
        self.car = Car.objects.get(id=self.car.id)
        self.assertIsNone(self.car.owner)
    
    
    def test_car_timeline_api_404_on_invalid_car(self):
        response = self.client.get(self.car_timeline_url.format(number=0))
        self.assertEquals(response.status_code, 404)

    def test_car_timeline_accurate(self):
        e1 = Event.objects.add_car_bought(self.car, self.user, 0)
        e2 = Event.objects.add_car_ride(self.user, 
                                        None, 
                                        self.car, 
                                        self.stop, 
                                        self.stop,
                                        0)
        e3 = Event.objects.add_car_sold(self.car, self.user, 0)
        
        url = self.car_timeline_url.format(number=self.car.number)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        
        self.assertEquals(len(data), 3)
        expected_events = ('car_sold', 'car_bought', 'car_ride')

        for event in data:
            self.assertIn(event['event'], expected_events)
