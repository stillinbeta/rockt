import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from game.models import Car, Stop


class StopApiTest(TestCase):
    api_name = 'stop'

    def setUp(self):
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

    def test_data_correct(self):
        response = self.client.get(reverse(self.api_name,
                                           args=(self.stop.number,)))
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
            self.assertEquals(car['checkin_url'],
                reverse('car-checkin', args=(expected_cars[i].number,)))
