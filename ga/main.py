from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
#from update import LocationUpdater
from models import StreetcarLocation

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('<html><head><title>Streetcars</title></head>')
        self.response.out.write("<body>")
        map_str = "http://maps.google.com/maps/api/staticmap?size=1024x1024&sensor=false&maptype=roadmap&markers=color:red"
        rpc = db.create_rpc(deadline=5, read_policy=db.EVENTUAL_CONSISTENCY)

        for car in StreetcarLocation.all().filter("in_service = ",True).fetch(limit=75,rpc=rpc):
            map_str += '%7C'+str(car.location)
        self.response.out.write("<body><img src='%s' /></body></html>" % map_str)

application = webapp.WSGIApplication(
                                    [('/',MainPage),
   #                                  ('/update',LocationUpdater),
                                     ],
									debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
