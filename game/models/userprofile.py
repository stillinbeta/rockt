from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import EmbeddedModelField,ListField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings 

@receiver(post_save)
def create_user_profile(sender, **kwargs):
    if sender != User or not kwargs.get('created'):
        return
    UserProfile.objects.create(balance=settings.INITIAL_BALANCE, 
                               user=kwargs.get('instance'))





#Currenty checked in
class Riding(models.Model):
    car = models.ForeignKey('game.Car')
    boarded = models.ForeignKey('game.Stop')
    time = models.DateTimeField(auto_now=True)

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

    class Meta:
        app_label = "game"
