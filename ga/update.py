from google.appengine.ext import webapp
from google.appengine.api import urlfetch,apiproxy_stub_map
from google.appengine.ext import db
from xml.dom import minidom
from models import StreetcarLocation
routes = range(501,513)
api_url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=ttc&r=%s&t=0'


cars_updated = []

def process_response(rpc,route):
    response = rpc.get_result()
    tree = minidom.parseString(response.content)
    for vehicle in tree.getElementsByTagName('vehicle'):
        car_id = vehicle.getAttribute('id')
        car = StreetcarLocation.get_or_insert(key_name=car_id)
        if vehicle.getAttribute('predictable') == u'true':
            car.location = (vehicle.getAttribute('lat')+","
                            +vehicle.getAttribute('lon'))
            car.route = route
            cars_updated.append(car_id)
            car.in_service = True
        else:
            car.in_service = False
        car.put()
    print "Route %s processed" % route
  
def create_callback(rpc,route):
    return lambda: process_response(rpc,route)

def remove_out_of_service():
    rpc = db.create_rpc(deadline=10, read_policy=db.EVENTUAL_CONSISTENCY)
    query = StreetcarLocation.all()
    all_streetcars = query.filter("in_service = ",True).run(rpc=rpc)

    changed = []
    for streetcar in all_streetcars:
        key = streetcar.key().name()
        if key not in cars_updated:
            streetcar.in_service = False
            changed.append(streetcar)
    if changed:
        rpc = db.create_rpc(deadline=10, read_policy=db.EVENTUAL_CONSISTENCY)
        db.put(changed)

rpcs = []
for route in routes:
    route = str(route)
    rpc = urlfetch.create_rpc()
    rpc.callback = create_callback(rpc,route)
    urlfetch.make_fetch_call(rpc,api_url % route)
    rpcs.append(rpc)

print "Content-Type: text/plain"
apiproxy_stub_map.UserRPC.wait_all(rpcs)
print "All Routes Updated"
remove_out_of_service()
print "Updated is complete"

