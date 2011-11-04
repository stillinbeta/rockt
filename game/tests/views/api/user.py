from base64 import b64encode
import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from game.models import Car
from game.tests.utils import temporary_settings


class UserCarListApiTests(TestCase):
    api_name = 'user-car'

    def setUp(self):
        username = 'apitest'
        password = 'secret'

        self.user = User.objects.create(username=username,
                         email='joe@bloggs.com')
        self.user.set_password(password)
        self.user.save()

        self.auth_string = 'Basic ' + b64encode('{}:{}'.format(username,
                                                             'secret'))
        self.car1 = Car.objects.create(number='4001', location=(0, 0))
        self.car2 = Car.objects.create(number='4002', location=(0, 0))
        self.car3 = Car.objects.create(number='4003', location=(0, 0))

    def testAuthRequired(self):
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
        response = self.client.get(reverse(self.api_name),
                                   HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), 2)
        for car in data:
            number = str(car['car'])
            self.assertIn(number, expected_responses)
            expected_responses.remove(number)

    def tearDown(self):
        # Because it's important that there only ever be one user by this
        # this username, we delete when we're finished
        self.user.delete()
