from django.db import models

class Stop(models.Model):
    number = models.TextField()
    route = models.IntegerField()
    description = models.TextField()
    geohash = models.TextField()
    latitude = models.DecimalField(max_digits=9,decimal_places=6,null=True)
    longitude = models.DecimalField(max_digits=9,decimal_places=6,null=True)
    
    def save(self, *args, **kwargs):
        try:
            old = Stop.objects.get(number=self.number)
            self.id  = old.id
        except Stop.DoesNotExist:
            pass
        super(Stop,self).save(*args,**kwargs)
