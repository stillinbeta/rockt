import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from game.models import Car, Stop
from game.tests.views.api.common import ApiTests


class StopApiTests(ApiTests):
    api_name = 'stop'

    def setUp(self):
        super(StopApiTests, self).setUp()

        def create_car(loc, number, route=511, active=True):
            return Car.objects.create(
                number=number,
                route=route,
                active=active,
                location=loc,)

        self.closest = create_car((-79.4110, 43.66449), 4211)
        self.closer = create_car((-79.4065, 43.66449), 4212)
        self.close = create_car((-79.39951, 43.63651), 4213)

        self.stop = Stop.objects.create(number="00258",
                                        location=[-79.411286, 43.666532],
                                        route=511)

    def test_auth_required(self):
        response = self.client.get(reverse(self.api_name,
                                           args=(self.stop.number,)))
        self.assertEquals(response.status_code, 403)

    def test_data_correct(self):
        response = self._make_get((self.stop.number,))
        self.assertEquals(response.status_code, 200)

        expected_cars = [self.closest, self.closer, self.close]
        data = json.loads(response.content)

        stop_fields = ('number', 'route', 'description', 'location')
        for field in stop_fields:
            self.assertIn(field, data)
            self.assertEquals(data[field], getattr(self.stop, field))

        self.assertIn('cars_nearby', data)
        self.assertEquals(len(data['cars_nearby']), len(expected_cars))

        for i in range(len(expected_cars)):
            car = data['cars_nearby'][i]
            self.assertEquals(car['number'], expected_cars[i].number)
            self.assertSequenceEqual(car['location'],
                                      expected_cars[i].location)

    def test_shows_checkin_url_when_not_riding(self):
        profile = self.user.get_profile()
        profile.riding = None
        profile.save()

        response = self._make_get((self.stop.number,))
        data = json.loads(response.content)
        for car in data['cars_nearby']:
            self.assertNotIn('checkout_url', car)
            self.assertIn('checkin_url', car)
            self.assertEquals(car['checkin_url'],
                              reverse('car-checkin', args=(car['number'],)))

    def test_shows_checkout_url_when_riding(self):
        profile = self.user.get_profile()
        profile.check_in(self.close, self.stop)

        response = self._make_get((self.stop.number,))
        data = json.loads(response.content)
        for car in data['cars_nearby']:
            self.assertNotIn('checkin_url', car)
            self.assertIn('checkout_url', car)
            self.assertEquals(car['checkout_url'], reverse('car-checkout'))
