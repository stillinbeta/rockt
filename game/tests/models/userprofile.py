from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import User

from game.models import Car, UserProfile, Stop
from game.tests.utils import temporary_settings


class UserProfileTests(TestCase):
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
        self.car = Car.objects.create(
                                number=4211,
                                active=True,
                                location=[-79.402858, 43.644075],)

    def test_check_in(self):
        profile = self.user.get_profile()
        profile.check_in(self.car, self.bathurst_station)
        self.assertEqual(profile.riding.car, self.car)
        self.assertEqual(profile.riding.boarded, self.bathurst_station)
        self.assertAlmostEqual(profile.riding.time, datetime.now(),
                               delta=timedelta(seconds=2))

    def test_checkout_no_checkin_raises_exception(self):
        profile = self.user.get_profile()
        profile.riding = None
        profile.save()
        with self.assertRaises(UserProfile.NotCheckedInException):
            profile.check_out(self.bathurst_and_king)

    def test_checkout_causes_ride(self):
        #check for a raised exception of no balance to ensure ride called
        profile = self.user.get_profile()
        profile.balance = 0
        profile.save()
        profile.check_in(self.car, self.bathurst_station)
        with self.assertRaises(UserProfile.InsufficientFundsException):
            profile.check_out(self.bathurst_and_king)

    def test_checkout_returns_fare(self):
        fare = 100
        profile = self.user.get_profile()
        profile.balance = fare * 10
        profile.save()

        def fake_fare(*args, **kwargs):
            return fare

        profile.check_in(self.car, self.bathurst_station)
        with temporary_settings({'RULE_FIND_FARE': fake_fare}):
            self.assertEquals(profile.check_out(self.bathurst_and_king),
                              fare)
