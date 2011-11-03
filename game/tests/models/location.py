from django.test import TestCase
from game.models.location import LocationClass


class LocationClassTests(TestCase):
    def test_distance_to_correct(self):
        c1 = LocationClass()
        c1.location = (-79.44314, 43.67794)
        c2 = LocationClass()
        c2.location = (-79.46307, 43.67356)
        self.assertAlmostEqual(c1.distance_to(c2), 1.67, delta=.01)
