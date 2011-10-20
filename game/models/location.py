from django.db import models
from geopy.distance import distance

class LocationClass:
    def distance_to(self, model):
        #geopy is lat,lon, mongo is lon,lat
        return distance(*(stop.location[::-1] 
                         for stop in (self,model))).kilometers
