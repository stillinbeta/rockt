from django.db import models
from pymongo import GEO2D
from djangotoolbox.fields import ListField 
from django_mongodb_engine.contrib import MongoDBManager

MAX_DISTANCE = ''

# Create your models here.

class CarLocatorManager(MongoDBManager):
    def find_nearby(self,route, location):
        return self.raw_query({'location':
                                {'$maxDistance': MAX_DISTANCE,'$near':location},
                                'route':route})

class Car(models.Model):
    number = models.PositiveIntegerField(db_index=True)
    route = models.IntegerField(null=True)
    active = models.BooleanField()
    geohash = models.TextField()
    location = ListField()
    
    objects = CarLocatorManager()
    
    class MongoMeta:
        indexes = [{'fields': [('location',GEO2D),'route']}]
    
    def save(self, *args, **kwargs):
        try:
            old = Car.objects.get(number=self.number)
            self.id = old.id
        except Car.DoesNotExist:
            pass
        super(Car,self).save(*args,**kwargs)
    
