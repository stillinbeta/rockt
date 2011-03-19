from google.appengine.ext import db
from geo.geomodel import GeoModel

class StreetcarLocation(GeoModel):
#    num = db.IntegerProperty() #we're using key_name as car number
    route = db.StringProperty()
    in_service = db.BooleanProperty()
    

class Stop(GeoModel):
    num = db.StringProperty() #"number" is apparently sometimes not a number.
    desc = db.StringProperty()
    route = db.IntegerProperty()
 
