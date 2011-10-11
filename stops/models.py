from django.db import models

class Stop(models.Model):
    number = models.TextField()
    route = models.IntegerField()
    description = models.TextField()
    geohash = models.TextField()
    latitude = models.DecimalField(max_digits=9,decimal_places=6,null=True)
    longitude = models.DecimalField(max_digits=9,decimal_places=6,null=True)
