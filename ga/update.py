from google.appengine.ext import webapp
from google.appengine.api.urlfetch import fetch
from google.appengine.ext import db
from xml.dom import minidom
from models import StreetcarLocation
routes = range(501,513)
api_url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=ttc&r={0}&t=0'


class LocationUpdater(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        for route in routes:
            response = fetch(api_url.format(route))
            tree = minidom.parseString(response.content)
            for vehicle in tree.getElementsByTagName('vehicle'):
                if vehicle.getAttribute('predictable') == u'true':
                    car_id = int(vehicle.getAttribute('id'))
                    self.response.out.write(car_id)
                    car = StreetcarLocation.get_or_insert(key_name=str(car_id))
                    car.location = (vehicle.getAttribute('lat')+","
                                    +vehicle.getAttribute('lon'))
                    car.route = route
                    car.put()
        rpc = db.create_rpc(deadline=5, read_policy=db.EVENTUAL_CONSISTENCY) 
        for car in StreetcarLocation.all().run(rpc=rpc):
            self.response.out.write("{0} at {1} on route {2}\n".format(car.key().name(),car.location,car.route))
        
