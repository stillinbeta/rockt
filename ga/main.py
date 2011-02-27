from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
#from update import LocationUpdater
from models import StreetcarLocation
import simplejson as json

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/json'

        rpc = db.create_rpc(deadline=5, read_policy=db.EVENTUAL_CONSISTENCY)

        locations = []
        for car in StreetcarLocation.all().filter("in_service = ",True).run(rpc=rpc):
            locations.append([car.location.lat, car.location.lon])
        
        self.response.out.write(json.dumps(locations))

application = webapp.WSGIApplication([('/streetcars',MainPage),], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
