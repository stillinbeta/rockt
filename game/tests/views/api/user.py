from base64 import b64encode
import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from game.models import Car
from game.tests.utils import temporary_settings
from game.tests.views.api.common import ApiTests


class UserCarListApiTests(ApiTests):
    api_name = 'user-car-list'

    def setUp(self):
        super(UserCarListApiTests, self).setUp()

        self.car1 = Car.objects.create(number='4001', location=(0, 0))
        self.car2 = Car.objects.create(number='4002', location=(0, 0))
        self.car3 = Car.objects.create(number='4003', location=(0, 0))

    def test_auth_required(self):
        response = self.client.get(reverse(self.api_name))
        self.assertEquals(response.status_code, 403)

    def test_get_list_data_correct(self):
        def fake_price(*args, **kwargs):
            return 0
        with temporary_settings({'RULE_GET_STREETCAR_PRICE': fake_price}):
            self.car1.sell_to(self.user)
            self.car3.sell_to(self.user)

        expected_responses = [car.number for car in (self.car1,
                                                            self.car3)]
        response = self._make_get()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 2)
        for car in data:
            number = str(car['car'])
            self.assertIn(number, expected_responses)
            expected_responses.remove(number)


class UserCarApiTests(ApiTests):
    api_name = 'user-car'

    def setUp(self):
        super(UserCarApiTests, self).setUp()

        self.car = Car.objects.create(number='4010',
                                      route='510',
                                      location=[-79.30111, 43.68375])
        self.car.total_fares.revenue = 150
        self.car.total_fares.riders = 12
        self.car.owner_fares.revenue = 100
        self.car.owner_fares.riders = 2
        self.car.save()

    def test_auth_required(self):
        response = self.client.get(reverse(self.api_name, args=(0,)))
        self.assertEquals(response.status_code, 403)

    def test_not_owning_car_is_403(self):
        self.car.owner = None
        self.car.save()

        response = self._make_get((self.car.number,))
        self.assertStatusCode(response, 403)

    def test_data_is_accurate(self):
        self.car.owner = self.user.get_profile()
        self.car.save()

        response = self._make_get((self.car.number,))
        self.assertStatusCode(response, 200)

        data = json.loads(response.content)
        for key, value in data.items():
            field = getattr(self.car, key, None)
            self.assertIsNotNone(field)
            if type(value) == dict:
                for sub_key, sub_value in value.items():
                    self.assertEquals(sub_value,
                        getattr(field, sub_key))
            elif type(field) == str:
                self.assertEquals(str(value), field)
            else:
                self.assertEquals(value, field)
