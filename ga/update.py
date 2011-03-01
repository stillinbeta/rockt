from google.appengine.ext import webapp
from google.appengine.api import urlfetch,apiproxy_stub_map
from google.appengine.ext import db
from xml.dom import minidom
from models import StreetcarLocation
routes = range(501,513)
api_url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=ttc&r=%&t=0'

route_list = []
for route in routes:
    route_list.append(str(route)) 

print "Content-Type: text/plain"

response = urlfetch.fetch(api_url)
tree = minidom.parseString(response.content)
for vehicle in tree.getElementsByTagName('vehicle'):
    if (vehicle.getAttribute('predictable') == u'true' and
        vehicle.getAttribute('routeTag') in route_list):
        car_id = vehicle.getAttribute('id')
        car = StreetcarLocation.get_or_insert(key_name=car_id)
        car.location = (vehicle.getAttribute('lat')+","
                        +vehicle.getAttribute('lon'))
        car.route = vehicle.getAttribute('routeTag')
        car.in_service = True
        car.put()
        print "Car %s processed" % car_id

print "Update is Complete"

