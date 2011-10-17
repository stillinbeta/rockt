from django.test import TestCase
from django.contrib.auth.models import User 

from game.models import Car,Stop,UserProfile,FareInfo
from game.rules import find_fare, get_streetcar_price 

class CarTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='joe',
                                        email='joe@bloggs.com',
                                        password='secret')
        UserProfile.objects.create(user=self.user, balance=0)
        
        def create_car(loc, number,route=511, active=True):
            return Car.objects.create(
                number=number,
                route=route,
                active=active,
                location=loc,
                owner_fares=FareInfo(),
                total_fares=FareInfo(),)

        self.closest = create_car((-79.4110, 43.66449),4211)
        self.closer = create_car((-79.4065, 43.66449), 4212)
        self.close = create_car((-79.39951, 43.63651), 4213)

        self.off_bathurst = create_car((-79.39629, 43.64858),4123, 510)
        self.inactive = create_car((-79.40405, 43.64729),4124, active=False)

        
        self.bathurst_station = Stop.objects.create(
                            location=[ -79.411286, 43.666532 ],
                            route=511)
        self.bathurst_and_king = Stop.objects.create(
                            location=[ -79.402858, 43.644075 ],
                            route=511)
        
    def test_sell_to_with_insufficient_funds_raises_exception(self):
        profile = self.user.get_profile()
        profile.balance = 0
        profile.save()
        with self.assertRaises(UserProfile.InsufficientFundsException):
            self.close.sell_to(self.user)

    def test_sell_to(self):
        profile = self.user.get_profile()
        new_balance = get_streetcar_price(self.user,self.close) + 50 
        profile.balance = new_balance
        profile.save()
        
        self.close.owner_fares=FareInfo(riders=10,revenue=15)
        self.close.sell_to(self.user)
        self.assertEqual(profile.balance,50)
        self.assertEqual(self.close.owner_fares.riders,0)
        self.assertEqual(self.close.owner_fares.revenue,0)
        self.assertEqual(self.close.owner,profile)
    def test_find_nearby(self):
        nearby = Car.objects.find_nearby(self.bathurst_station).all()

        self.assertSequenceEqual(nearby,[self.closest,self.closer,self.close])

    def test_ride_insufficient_fare_throws_exception(self):
        profile = self.user.get_profile()
        profile.balance = 0
        with self.assertRaises(UserProfile.InsufficientFundsException):
            self.close.ride(self.user,
                            self.bathurst_station,
                            self.bathurst_and_king) 

    def test_ride(self):
        profile = self.user.get_profile()
        profile.balance = 10 * 100 
        self.close.owner_fares=FareInfo()
        self.close.total_fares=FareInfo(riders=1,revenue=15)

        total_fare = find_fare(self.user,
                               self.close, 
                               self.bathurst_station, 
                               self.bathurst_and_king,)

        expected_balance = profile.balance - total_fare
        self.close.ride(self.user,
                        self.bathurst_station,
                        self.bathurst_and_king)

        self.assertEqual(self.user.get_profile().balance,expected_balance)
        self.assertEqual(self.close.owner_fares.riders,1)
        self.assertEqual(self.close.owner_fares.revenue,total_fare)
        self.assertEqual(self.close.total_fares.riders,2)
        self.assertEqual(self.close.total_fares.revenue,15 + total_fare)

    def test_ride_own_car_doesnt_charge(self):
        profile = self.user.get_profile()
        self.close.owner = profile
        self.close.save()

        old_owner_rev = self.close.owner_fares.revenue
        old_total_rev = self.close.total_fares.revenue
        old_balance = profile.balance
        
        self.close.ride(self.user,
                        self.bathurst_station,
                        self.bathurst_and_king)

        self.assertEqual(self.close.owner_fares.revenue,old_owner_rev)
        self.assertEqual(self.close.total_fares.revenue,old_total_rev)
        self.assertEqual(self.user.get_profile().balance,old_balance)
