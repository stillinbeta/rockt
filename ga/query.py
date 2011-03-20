from models import StreetcarLocation,Stop
from google.appengine.ext import db 
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os

class QueryPage(webapp.RequestHandler):
    def get(self):
        arg = self.request.get('stop')
        if arg == '':
            stops = Stop.all()
            path = os.path.join(os.path.dirname('__file__'),
                'templates/stops.html')
            template_vals = {'stops':stops}
        else:
            stop = Stop.get(db.Key.from_path('Stop','stop-%s' % arg))
            nearby_cars = StreetcarLocation.proximity_fetch(
                                    StreetcarLocation.all().filter(
                                        'route =',str(stop.route)).filter(
                                        'in_service =',True),
                                    stop.location,
                                    max_results=10,
                                    max_distance=500)
            template_vals = {'stop':stop, 'cars':nearby_cars}
            path = os.path.join(os.path.dirname('__file__'),
                    'templates/cars_nearby.html')
        self.response.out.write(template.render(path,template_vals))

class StationFinderPage(webapp.RequestHandler):
    def get(self):
        lat = self.request.get('lat')
        lon = self.request.get('lon')
        if lat == '' or lon == '':
            path = os.path.join(os.path.dirname('__file__'),
                'templates/geolocation.html')
            template_vals = {}
            self.response.out.write(template.render(path,template_vals))
        else:
            stops = Stop.proximity_fetch(
                            Stop.all(),
                            db.GeoPt(lat,lon),
                            max_results=10,
                            max_distance=500)

            path = os.path.join(os.path.dirname('__file__'),
                'templates/station_finder.html')
            template_vals = {'stops':stops, 'lat':lat, 'lon':lon}
            self.response.out.write(template.render(path,template_vals))

