from django.db import models
from djangotoolbox.fields import DictField

class EventManager(models.Manager):
    def add_car_sold(self, car, user, price, old_user=None):
        event = 'car_sold'

        data = {'car':car.number,
                'user':user.username,
                'price':price}
        if old_user:
            data['old_user'] = old_user.username
        return self.create(event=event,data=data)
    def add_car_ride(self, rider, owner, car, on, off, fare):
        ##TODO: Make more robust framework for measuring distances
        traveled = on.distance_to(off)
        event = 'car_ride'
        data = {'car':car.number,
                'rider':rider.username,
                'on':{'number':on.number,
                      'location':on.location},
                'off':{'number':off.number,
                       'location':off.location},
                'traveled': traveled,
                'fare':fare} 
        if owner:
            data['owner'] = owner.username
        return self.create(event=event,data=data)
class Event(models.Model):
    event  = models.TextField()
    data = DictField()
    date = models.DateField(auto_now_add=True)

    objects = EventManager()

    class Meta:
        ordering = ['date']
   
         
        
