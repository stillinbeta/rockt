from django.db import models
from django_mongodb_engine.contrib import MongoDBManager
from djangotoolbox.fields import ListField 
from pymongo import GEO2D

class StopLocatorManager(MongoDBManager):
    def find_nearby(self, location):
        return self.raw_query({'location':{'$near':location}})

class Stop(models.Model):
    number = models.TextField()
    route = models.IntegerField()
    description = models.TextField()
    location = ListField()

    objects = StopLocatorManager()
    class MongoMeta:
        indexes = [{'fields': [('location',GEO2D)]}]

