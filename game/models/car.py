from django.db import models
from pymongo import GEO2D
from djangotoolbox.fields import ListField,EmbeddedModelField 
from django_mongodb_engine.contrib import MongoDBManager
from django.db.models.signals import pre_save
from django.dispatch import receiver

from userprofile import UserProfile
from event import Event
from game.rules import find_fare, get_streetcar_price
from location import LocationClass

@receiver(pre_save)
def add_fareinfo(sender, **kwargs):
    if sender != Car:
        return
    car = kwargs.get('instance')
    if not car.owner_fares:
        car.owner_fares = FareInfo()
    if not car.total_fares:
        car.total_fares = FareInfo()


STREETCAR_PRICE = 400

# Create your models here.

class FareInfo(models.Model):
    riders = models.IntegerField(default=0)
    revenue = models.IntegerField(default=0)

class CarLocatorManager(MongoDBManager):
    def find_nearby(self,stop):
        return self.raw_query({'location': {'$near':stop.location},
                                'route':stop.route,'active':True})

class Car(models.Model,LocationClass):
    #Location information fields
    number = models.PositiveIntegerField(db_index=True)
    route = models.IntegerField(null=True)
    active = models.BooleanField()
    location = ListField() #(lon, lat)

    #Financial information fields 
    owner = models.ForeignKey('game.UserProfile',null=True)
    owner_fares = EmbeddedModelField(FareInfo)
    total_fares = EmbeddedModelField(FareInfo)
    
    
    objects = CarLocatorManager()

    def sell_to(self,user):
        old_user = self.owner
        price = get_streetcar_price(user, self)
        profile = user.get_profile()
        if profile.balance < price:
            raise UserProfile.InsufficientFundsException
        self.owner = profile
        self.owner_fares = FareInfo()
        self.save()
        profile.balance -= price 
        
        Event.objects.add_car_bought(self,user, price, self._get_owner_user()) 
        profile.save()
        
    def buy_back(self):
        price = get_streetcar_price(self.owner, self) 
        owner = self.owner
        self.owner = None
        self.owner_fares = FareInfo()
        self.save()
        
        owner.balance += price
        Event.objects.add_car_sold(self, owner.user, price)
        owner.save()
    def ride(self,user,on,off):
        profile = user.get_profile()
        #You don't have to pay for your own streetcars
        insufficient_funds = False
        fare_paid  = find_fare(user, self, on, off) 
        if fare_paid > profile.balance:
           fare_paid = 0
           insufficient_funds = True

        for fare_info in (self.owner_fares,self.total_fares):
            fare_info.riders += 1
            fare_info.revenue += fare_paid 
        self.save()
        
        Event.objects.add_car_ride(user, self._get_owner_user(), self, 
                                   on, off, fare_paid) 

        if (insufficient_funds):
            raise UserProfile.InsufficientFundsException
        profile.balance -= fare_paid
        profile.save()
        if self.owner:
            self.owner.balance += fare_paid
            self.owner.save()

    def _get_owner_user(self):
        if self.owner:
            return self.owner.user
        return None

             
    class MongoMeta:
        indexes = [{'fields': [('location',GEO2D),'route']}]

    class Meta:
        app_label = "game"
