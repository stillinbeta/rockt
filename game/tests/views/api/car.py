from base64 import b64encode
import json


from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from game.models import Car, Stop, UserProfile, Event
from game.tests.utils import temporary_settings


class CarApiTests(TestCase):
    checkout_name = 'car-checkout'
    checkin_name = 'car-checkin'
    sell_name = 'car-sell'
    buy_name = 'car-buy'
    timeline_name = 'car-timeline'

    def setUp(self):
        username = 'checkinout'
        password = 'secret'
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
                                location=[-79.402858, 43.644075],)

        self.stop = Stop.objects.create(number="00000",
                                       location=[-79.402858, 43.644075],
                                       route=511)

    def assertAuthRequired(self, url):
        response = self.client.post(url)
        self.assertEquals(response.status_code, 403)

    def assertStatusCode(self, name, args=(), stop_number=None, code=200):
        # Stop number needs to be paramaterized
        if stop_number is not None:
            data = {'stop_number': stop_number}
        else:
            data = {}

        # We usually pass args as a single paramater. Tuplize it.
        if not args == ():
            args = (args,)

        url = reverse(name, args=args)
        response = self.client.post(url, data,
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, code)

    def test_check_in_requires_auth(self):
        self.assertAuthRequired(reverse(self.checkin_name, args=('0')))

    def test_check_in_invalid_info_gives_404(self):
        self.assertStatusCode(self.checkin_name, self.car.number, 0, 404)
        self.assertStatusCode(self.checkin_name, 0, self.stop.number, 404)

    def test_check_in_missing_parameters_gives_400(self):
        self.assertStatusCode(self.checkin_name, self.car.number, code=400)

    def test_check_in_creates_riding(self):
        self.assertStatusCode(self.checkin_name,
                              self.car.number,
                              self.stop.number)

        profile = self.user.get_profile()
        self.assertIsNotNone(profile.riding)
        self.assertEquals(profile.riding.car, self.car)
        self.assertEquals(profile.riding.boarded, self.stop)

    def test_check_out_requires_auth(self):
        self.assertAuthRequired(reverse(self.checkout_name))

    def test_check_out_missing_stop_gives_400(self):
        self.assertStatusCode(self.checkout_name, code=400)

    def test_check_out_invalid_stop_gives_404(self):
        self.assertStatusCode(self.checkout_name,
                              stop_number=0,
                              code=404)

    def test_check_out_not_riding_gives_400(self):
        profile = self.user.get_profile()
        profile.riding = None
        profile.save()

        self.assertStatusCode(self.checkout_name,
                              stop_number=self.stop.number,
                              code=400)

    def test_check_out_finishes_ride(self):
        self.assertStatusCode(self.checkin_name,
                              self.car.number,
                              self.stop.number)
        self.assertStatusCode(self.checkout_name, stop_number=self.stop.number)
        self.assertIsNone(self.user.get_profile().riding)

    def _get_checkout_data(self):
        url = reverse(self.checkout_name)
        response = self.client.post(url,
                                    data={'stop_number': self.stop.number},
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)
        return json.loads(response.content)

    def test_checkout_returns_fare(self):
        fare = 100
        profile = self.user.get_profile()
        profile.balance = fare * 100
        profile.save()
        profile.check_in(self.car, self.stop)

        def fake_fare(*args, **kwargs):
            return fare
        with temporary_settings({'RULE_FIND_FARE': fake_fare}):
            data = self._get_checkout_data()
        self.assertIn('fare', data)
        self.assertEquals(data['fare'], fare)

    def test_checkout_cant_buy_has_no_purchase(self):
        self.user.get_profile().check_in(self.car, self.stop)

        def fake_fare(*args, **kwargs):
            return 0

        def fake_can_purchase(*args, **kwargs):
            return False
        with temporary_settings({'RULE_FIND_FARE': fake_fare,
                                 'RULE_CAN_BUY_CAR': fake_can_purchase}):
            data = self._get_checkout_data()
        self.assertNotIn('purchase', data)

    def test_checkout_can_buy_has_purchase(self):
        self.user.get_profile().check_in(self.car, self.stop)
        price = 1000

        def fake_fare(*args, **kwargs):
            return 0

        def fake_can_purchase(*args, **kwargs):
            return True

        def fake_price(*args, **kwargs):
            return price
        with temporary_settings({'RULE_FIND_FARE': fake_fare,
                                 'RULE_CAN_BUY_CAR': fake_can_purchase,
                                 'RULE_GET_STREETCAR_PRICE': fake_price}):
            data = self._get_checkout_data()
        self.assertIn('purchase', data)
        self.assertEquals(data['purchase']['price'], price)
        self.assertEquals(data['purchase']['url'],
                          reverse('car-sell', args=(self.car.number,)))

    def test_sell_auth_required(self):
        self.assertAuthRequired(reverse(self.sell_name, args=('0')))

    def test_car_sell_invalid_car_gives_404(self):
        self.assertStatusCode(self.sell_name, 0, code=404)

    def test_sell_not_allowed_returns_403(self):
        def fake_rule(*args, **kwargs):
            return False
        with temporary_settings({'RULE_CAN_BUY_CAR': fake_rule}):
            self.assertStatusCode(self.sell_name, self.car.number, code=403)

    def test_sell_insufficient_funds_returns_403(self):
        profile = self.user.get_profile()
        profile.balance = 0
        profile.save()

        def fake_price(*args, **kwargs):
            return 100
        with temporary_settings({'RULE_GET_STREETCAR_PRICE': fake_price}):
            self.assertStatusCode(self.sell_name, self.car.number, code=403)

    def test_sell_transfers_ownership(self):
        self.car.owner = None
        self.car.save()

        def fake_rule(*args, **kwargs):
            return True

        def fake_price(*args, **kwargs):
            return 0
        with temporary_settings({'RULE_CAN_BUY_CAR': fake_rule,
                                 'RULE_GET_STREETCAR_PRICE': fake_price}):
            self.assertStatusCode(self.sell_name, self.car.number)
        self.car = Car.objects.get(number=self.car.number)
        self.assertEquals(self.car.owner, self.user.get_profile())

    def test_buy_auth_required(self):
        self.assertAuthRequired(reverse(self.buy_name, args=('0')))

    def test_car_buy_invalid_car_gives_404(self):
        self.assertStatusCode(self.buy_name, 0, code=404)

    def test_buy_not_allowed_returns_403(self):
        self.car.owner = self.user2.get_profile()
        self.car.save()
        self.assertStatusCode(self.buy_name, self.car.number, code=403)

    def test_buy_buys_car(self):
        self.car.owner = self.user.get_profile()
        self.car.save()
        self.assertStatusCode(self.buy_name, self.car.number)
        self.car = Car.objects.get(id=self.car.id)
        self.assertIsNone(self.car.owner)

    def test_timeline_api_404_on_invalid_car(self):
        response = self.client.get(reverse(self.timeline_name, args=(0,)))
        self.assertEquals(response.status_code, 404)

    def test_timeline_accurate(self):
        e1 = Event.objects.add_car_bought(self.car, self.user, 0)
        e2 = Event.objects.add_car_ride(self.user,
                                        None,
                                        self.car,
                                        self.stop,
                                        self.stop,
                                        0)
        e3 = Event.objects.add_car_sold(self.car, self.user, 0)

        response = self.client.get(reverse(self.timeline_name,
                                           args=(self.car.number,)))
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(len(data), 3)
        expected_events = ['car_sold', 'car_bought', 'car_ride']

        for event in data:
            self.assertIn(event['event'], expected_events)
            expected_events.remove(event['event'])
            self.assertEquals(event['user'], self.user.username)

    def tearDown(self):
        # Because it's important that there only ever be one user by this
        # this username, we delete when we're finished
        self.user.delete()
