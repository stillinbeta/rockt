from django.test import TestCase
from django.contrib.auth.models import User

from game.models import Car, Stop, FareInfo, Event

class EventTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='joe',
                                        email='joe@bloggs.com',
                                        password='secret')
        self.user2 = User.objects.create(username='heidi',
                                         email='heidi@yahoo.com',
                                         password='idieh')
        
        self.bathurst_station = Stop.objects.create(
                            number='00112',
                            route='510',
                            location=[ -79.411286, 43.666532 ],)
        self.bathurst_and_king = Stop.objects.create(
                            number='04412',
                            route='510',
                            location=[ -79.402858, 43.644075 ],)
        self.car = Car.objects.create(
                                number=4211,
                                active=True,
                                location=[ -79.402858, 43.644075 ],
                                owner_fares=FareInfo(),
                                total_fares=FareInfo(),)

    def test_add_car_sold_data_correct(self):
        price = 150
        event = Event.objects.add_car_sold(self.car,self.user,price) 
        self.assertEquals(event.event, 'car_sold')
        self.assertEquals(event.data['car'], self.car.number)
        self.assertEquals(event.data['user'], self.user.username)
        self.assertEquals(event.data['price'], price)
    def test_add_car_old_user_only_added_if_present(self):
        price = 150
        event = Event.objects.add_car_sold(self.car,self.user,price) 
        self.assertNotIn('old_user',event.data)  

        event = Event.objects.add_car_sold(self.car,self.user,price,self.user2) 
        self.assertEquals(event.data['old_user'],self.user2.username)
    
    def test_add_car_ride_data_accurate(self):
        fare = 120    
        distance=500
        event = Event.objects.add_car_ride(self.user, self.user2,
                                           self.car,
                                           self.bathurst_and_king,
                                           self.bathurst_station,
                                           fare,
                                           distance) 
        make_dict = lambda stop: {'number': stop.number, 'location':stop.location}
        expected = {
            'car':self.car.number,
            'rider':self.user.username,
            'on':make_dict(self.bathurst_and_king),
            'off':make_dict(self.bathurst_station),
            'traveled':distance,
            'fare':fare,
            'owner':self.user2.username}
        
        for key, val in expected.items():
            self.assertEquals(event.data[key],val)
    def test_add_car_ride_doesnt_add_owner_if_not_present(self):
        event = Event.objects.add_car_ride(self.user, None,
                                           self.car,
                                           self.bathurst_and_king,
                                           self.bathurst_station,
                                           0,0)
        self.assertNotIn('owner',event.data)
