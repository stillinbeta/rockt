from google.appengine.ext import db

class StreetcarLocation(db.Model):
#    num = db.IntegerProperty() #we're using key_name as car number
    location = db.GeoPtProperty()
    route = db.StringProperty()
    in_service = db.BooleanProperty()
    

class Stop(db.Model):
    num = db.StringProperty() #"number" is apparently sometimes not a number.
    desc = db.StringProperty()
    location = db.GeoPtProperty()
    route = db.IntegerProperty()
 
