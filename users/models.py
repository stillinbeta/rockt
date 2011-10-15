from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import EmbeddedModelField,ListField


#Currenty checked in
class Riding(models.Model):
    car = models.ForeignKey('cars.Car')
    boarded = models.ForeignKey('stops.Stop')
    time = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    balance = models.IntegerField()
    user = models.ForeignKey(User, unique=True)
    riding = EmbeddedModelField(Riding,null=True)

    def check_in(self,car,stop):
        self.riding = Riding(car=car,boarded=stop)
        self.save()
    
    def check_out(self,stop):
        if self.riding == None:
            raise self.NotCheckedInException
        
        self.riding.car.ride(self.user,self.riding.boarded, stop)
        self.riding = None
        self.save()
    
    
    #Thrown when you try to check out and not checked in
    class NotCheckedInException(Exception):
        pass

    #Thrown when you can't afford something
    class InsufficientFundsException(Exception):
        pass
