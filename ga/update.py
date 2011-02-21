from google.appengine.ext import webapp
from google.appengine.api.urlfetch import fetch
from xml.dom import minidom
routes = ['510']


class LocationUpdater(webapp.RequestHandler):
    def get(self):
        response = fetch('http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=ttc&r={0}&t=0'.format(routes[0]))
        tree = minidom.parseString(response.content)
        vehicles = {}
        for vehicle in tree.getElementsByTagName('vehicle'):
            if vehicle.getAttribute('predictable') == u'true':
                vehicles[vehicle.getAttribute('id')] = ( vehicle.getAttribute('lat'), 
                vehicle.getAttribute('lon'))

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(vehicles)
        
