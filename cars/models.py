from django.db import models
from pymongo import GEO2D
from djangotoolbox.fields import ListField,EmbeddedModelField 
from django_mongodb_engine.contrib import MongoDBManager


from rockt.users.models import UserProfile

MAX_DISTANCE = ''
STREETCAR_PRICE = 400

# Create your models here.

class FareInfo(models.Model):
    riders = models.IntegerField(default=0)
    revenue = models.IntegerField(default=0)

class CarLocatorManager(MongoDBManager):
    def find_nearby(self,route, location):
        return self.raw_query({'location':
                                {'$maxDistance':MAX_DISTANCE,'$near':location},
                                'route':route})

class Car(models.Model):
    number = models.PositiveIntegerField(db_index=True)
    route = models.IntegerField(null=True)
    active = models.BooleanField()
    location = ListField()

    
    owner = models.ForeignKey(UserProfile,null=True)
    owner_fares = EmbeddedModelField(FareInfo)
    total_fares = EmbeddedModelField(FareInfo)
    
    
    objects = CarLocatorManager()

    def purchase(self,user):
        profile = user.get_profile()
        if profile.balance < STREETCAR_PRICE:
            raise UserProfile.InsufficientFundsException
        self.owner = profile
        self.owner_fares = FareInfo()
        self.save()
        profile.balance -= STREETCAR_PRICE
        profile.save()
    
    class MongoMeta:
        indexes = [{'fields': [('location',GEO2D),'route']}]
