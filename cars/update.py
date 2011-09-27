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

def remove_out_of_service(cars_update):
    query = StreetcarLocation.all(keys_only=True)
    all_streetcars = query.filter("in_service = ",True).run()

    to_remove = []
    for streetcar in all_streetcars:
        if streetcar not in cars_updated:
            to_remove.append(streetcar)
            print "Removing inactive car %s" % streetcar.name()
    if to_remove:
        streetcars = db.get(to_remove)
        for streetcar in streetcars:
            streetcar.in_service = False
        db.put(streetcars)

def update_streetcars():
    cars_updated = []

    response = urlfetch.fetch(api_url)
    tree = minidom.parseString(response.content)

    for vehicle in tree.getElementsByTagName('vehicle'):
        if (vehicle.getAttribute('routeTag') in route_list and
            vehicle.getAttribute('predictable') == u'true'):
            car_id = vehicle.getAttribute('id')
            car = StreetcarLocation.get_or_insert(key_name=car_id,
                location=db.GeoPt('0,0'))
            car.location = db.GeoPt(vehicle.getAttribute('lat'),
                            vehicle.getAttribute('lon'))
            car.route = vehicle.getAttribute('routeTag')
            car.in_service = True
            car.update_location()
            cars_updated.append(car.key())
            print "Car %s in service" % car_id
            car.put()

    return cars_updated 

print "Content-Type: text/plain"
cars_updated = update_streetcars()
print "Update is Complete, %d cars in service" % len(cars_updated)
remove_out_of_service(cars_updated)
print "Removal Complete"



