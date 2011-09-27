from django.db import models

# Create your models here.

class Car(models.Model):
    number = models.PositiveIntegerField(unique=True)
    route = models.IntegerField(null=True)
    active = models.BooleanField()
    geohash = models.TextField()
    latitude = models.DecimalField(max_digits=9,decimal_places=6,null=True)
    longitude = models.DecimalField(max_digits=9,decimal_places=6,null=True)
    
    def save(self, *args, **kwargs):
        try:
            old = Car.objects.get(number=self.number)
            self.id = old.id
        except Car.DoesNotExist:
            pass
        super(Car,self).save(*args,**kwargs)
