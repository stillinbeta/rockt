import logging

from google.appengine.ext import db
from google.appengine.api import users
from geo.geomodel import GeoModel

class Stop(GeoModel):
    num = db.StringProperty() #"number" is apparently sometimes not a number.
    desc = db.StringProperty()
    route = db.IntegerProperty()

class UserInfo(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    balance = db.FloatProperty(default=0.0)

    @classmethod
    def get_current_user(cls):
        current_user = users.get_current_user()
        if not current_user:
           return None
        user = db.Query(cls).filter('user = ',users.get_current_user()).get()
        if not user:
            user = cls().save()
        return user

class StreetcarLocation(GeoModel):
#    num = db.IntegerProperty() #we're using key_name as car number
    route = db.StringProperty()
    in_service = db.BooleanProperty()
    owner = db.ReferenceProperty(UserInfo,collection_name='streetcars')
