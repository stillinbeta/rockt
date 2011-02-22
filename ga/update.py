from google.appengine.ext import webapp
from google.appengine.api.urlfetch import fetch
from google.appengine.ext import db
from xml.dom import minidom
from models import StreetcarLocation
routes = range(501,513)
api_url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=ttc&r=%s&t=0'


class LocationUpdater(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        for route in routes:
            route = str(route)
            response = fetch(api_url % route)
            tree = minidom.parseString(response.content)
            for vehicle in tree.getElementsByTagName('vehicle'):
                car_id = int(vehicle.getAttribute('id'))
                car = StreetcarLocation.get_or_insert(key_name=str(car_id))
                if vehicle.getAttribute('predictable') == u'true':
                    car.location = (vehicle.getAttribute('lat')+","
                                    +vehicle.getAttribute('lon'))
                    car.route = route
                    car.in_service = True
                else:
                    car.in_service = False
                car.put()
        rpc = db.create_rpc(deadline=5, read_policy=db.EVENTUAL_CONSISTENCY) 
        for car in StreetcarLocation.all().filter("in_service =",True).run(rpc=rpc):
            self.response.out.write("%s at %s on route %s active: %s \n" % 
            (car.key().name(),car.location,car.route,car.in_service))
        
