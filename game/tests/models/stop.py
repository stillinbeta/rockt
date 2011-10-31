from django.test import TestCase
from game.models import Stop

class StopTest(TestCase):
    def setUp(self):
        self.stop1= Stop.objects.create(location=[-79.39770, 43.65307])
        self.stop2= Stop.objects.create(location=[-79.39723, 43.65102])
        self.stop3= Stop.objects.create(location=[-79.40230, 43.65201])
    
    def test_find_nearby_correct(self):
        loc = (-79.39812,43.65201)
        self.assertSequenceEqual(Stop.objects.find_nearby(loc),
                                 [self.stop1, self.stop2, self.stop3])
