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
            path = os.path.join(os.path.dirname('__file__'),'templates/stops.html')
            template_vals = {'stops':stops}
        else:
            stop = Stop.get(db.Key.from_path('Stop','stop-%s' % arg))
            nearby_cars = StreetcarLocation.proximity_fetch(
                                    StreetcarLocation.all().filter('route =',str(stop.route)),
                                    stop.location,
                                    max_results=10,
                                    max_distance=500)
            template_vals = {'stop':stop, 'cars':nearby_cars}
            path = os.path.join(os.path.dirname('__file__'),'templates/cars_nearby.html')
        self.response.out.write(template.render(path,template_vals))


#for car in nearby_cars:
#    print car.key().name()


#for stop in Stop.all():
#    print "{} ({}) at {}".format(stop.num,stop.desc,stop.location)
