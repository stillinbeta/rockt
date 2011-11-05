import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from game.models import Stop
from game.tests.utils import temporary_settings


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
        api_urls = [reverse('stop-find', args=args) for args in (('00', 'aa'),
                                                                 ('aa', '00'))]
        for api_url in api_urls:
            self.assertEquals(self.client.get(api_url).status_code, 400)

    def test_find_nearby_api(self):
        #Grumble grumble lat,lon for everyone but Mongo
        api_url = reverse('stop-find', args=(self.loc[1], self.loc[0]))

        response = self.client.get(api_url)
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(len(data), len(self.expected))
        expected_fields = (u'number', u'route', u'description', 'location')
        for i in range(len(data)):
            for key in expected_fields:
                self.assertIn(key, data[i])
                self.assertEquals(data[i][key], getattr(self.expected[i], key))

    def test_find_nearby_limits_by_setting(self):
        api_url = reverse('stop-find', args=(self.loc[1], self.loc[0]))

        limit = 2
        with temporary_settings({'STOP_SEARCH_LIMIT': limit}):
            response = self.client.get(api_url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEquals(len(data), limit)
