import json

from django.test import TestCase
from game.models import Stop


class StopTest(TestCase):
    loc = [-79.39812, 43.65201]

    def setUp(self):
        self.stop1 = Stop.objects.create(location=[-79.39770, 43.65307],
                                        number='05112',
                                        route=512)
        self.stop2 = Stop.objects.create(location=[-79.39723, 43.65102],
                                        number='05241',
                                        route=512)
        self.stop3 = Stop.objects.create(location=[-79.40230, 43.65201],
                                        number='20541',
                                        route=511)
        self.expected = [self.stop1, self.stop2, self.stop3]

    def test_find_nearby_correct(self):
        self.addTypeEqualityFunc(Stop, lambda a, b: a.number == b.number)
        self.assertSequenceEqual(Stop.objects.find_nearby(self.loc),
                                 self.expected)

    def test_find_nearby_api_returns_400_invalid_lat_lon(self):
        api_urls = ['/api/stop/find/' + tail for tail in ('00/aa/', 'aa/00/')]
        for api_url in api_urls:
            self.assertEquals(self.client.get(api_url).status_code, 400)

    def test_find_nearby_api(self):
        #Grumble grumble lat,lon for everyone but Mongo
        api_url = '/api/stop/find/{}/{}/'.format(self.loc[1], self.loc[0])

        response = self.client.get(api_url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), len(self.expected))
        for i in range(len(data)):
            for key, val in data[i].items():
                self.assertEquals(val, getattr(self.expected[i], key))
