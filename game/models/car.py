from django.db import models
from pymongo import GEO2D
from djangotoolbox.fields import ListField,EmbeddedModelField 
from django_mongodb_engine.contrib import MongoDBManager

from userprofile import UserProfile
from game.rules import find_fare, get_streetcar_price


STREETCAR_PRICE = 400

# Create your models here.

class FareInfo(models.Model):
    riders = models.IntegerField(default=0)
    revenue = models.IntegerField(default=0)

class CarLocatorManager(MongoDBManager):
    def find_nearby(self,stop):
        return self.raw_query({'location': {'$near':stop.location},
                                'route':stop.route,'active':True})

class Car(models.Model):
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
        price = get_streetcar_price(user, self)
        profile = user.get_profile()
        if profile.balance < price:
            raise UserProfile.InsufficientFundsException
        self.owner = profile
        self.owner_fares = FareInfo()
        self.save()
        profile.balance -= price 
        profile.save()
    
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

        if (insufficient_funds):
            raise UserProfile.InsufficientFundsException
        profile.balance -= fare_paid
        profile.save()


             
    class MongoMeta:
        indexes = [{'fields': [('location',GEO2D),'route']}]

    class Meta:
        app_label = "game"
