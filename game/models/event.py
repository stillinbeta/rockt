from django.db import models
from djangotoolbox.fields import DictField
from django_mongodb_engine.contrib import MongoDBManager
from pymongo.objectid import InvalidId
from django.contrib.auth.models import User


class EventManager(MongoDBManager):
    def add_car_bought(self, car, user, price, old_user=None):
        event = 'car_bought'

        data = {'car': car.number,
                'user': user.id,
                'price': price}
        if old_user:
            data['old_user'] = old_user.id
        return self.create(event=event, data=data)

    def add_car_sold(self, car, user, price):
        event = 'car_sold'
        data = {'car': car.number,
                'user': user.id,
                'price': price}
        return self.create(event=event, data=data)

    def add_car_ride(self, rider, owner, car, on, off, fare):
        ##TODO: Make more robust framework for measuring distances
        traveled = on.distance_to(off)
        event = 'car_ride'
        data = {'car': car.number,
                'rider': rider.id,
                'on': {'number': on.number,
                      'location': on.location},
                'off': {'number': off.number,
                       'location': off.location},
                'traveled': traveled,
                'fare': fare}
        if owner:
            data['owner'] = owner.id
        return self.create(event=event, data=data)

    def get_car_timeline(self, car):
        user_fields = ('old_user', 'user', 'rider')
        for event in self.raw_query({'data.car': car.number}):
            for field in user_fields:
                if field in event.data:
                    try:
                        event.data[field] = User.objects.get(
                            id=event.data[field])
                    except (User.DoesNotExist, InvalidId):
                        event.data[field] = None
            yield event


class Event(models.Model):
    event = models.TextField()
    data = DictField()
    date = models.DateTimeField(auto_now_add=True)

    objects = EventManager()

    class Meta:
        ordering = ['date']
        app_label = "game"

    class MongoMeta:
        indexes = [{'fields': [('data.car', 1)], 'sparse': True}]
