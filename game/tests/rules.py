from django.test import TestCase
from django.contrib.auth.models import User

from game.models import Car, Stop, UserProfile
from game.rules import find_fare, get_streetcar_price, can_buy_car


class RulesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='joe',
                                        email='joe@bloggs.com',
                                        password='secret')

        self.bathurst_station = Stop.objects.create(
                            location=[-79.411286, 43.666532],
                            route=511)
        self.bathurst_and_king = Stop.objects.create(
                            location=[-79.402858, 43.644075],
                            route=511)

        make_car = lambda number: Car.objects.create(
                                    number=number,
                                    active=True,
                                    location=[-79.402858, 43.644075],)
        self.alrv = make_car(4211)
        self.clrv = make_car(4011)

    def test_find_fare_owner_not_charged(self):
        self.alrv.owner = self.user.get_profile()
        self.alrv.save()

        fare = find_fare(self.user, self.alrv, None, None)
        self.assertEquals(fare, 0)

    def test_find_fare_alrv_twice_as_expensive(self):
        self.alrv.owner = None
        self.alrv.save()
        self.clrv.owner = None
        self.clrv.save()

        fare_args = lambda car: [self.user,
                                 car,
                                 self.bathurst_and_king,
                                 self.bathurst_station]

        fare_alrv = find_fare(*fare_args(self.alrv))
        fare_clrv = find_fare(*fare_args(self.clrv))

        #We use integer multiplication, so there may be some rounding error
        self.assertAlmostEqual(fare_clrv * 2, fare_alrv, delta=1)

    def test_streetcar_price_is_two_hundred(self):
        self.assertEquals(get_streetcar_price(None, None), 200)

    def test_can_buy_car(self):
        self.alrv.owner = None
        self.assertTrue(can_buy_car(self.user, self.alrv))
        self.alrv.owner = self.user.get_profile()
        self.assertFalse(can_buy_car(self.user, self.alrv))
