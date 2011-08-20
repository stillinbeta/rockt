from models import StreetcarLocation 
from google.appengine.ext import db 
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os

class CarPage(webapp.RequestHandler):
    def get(self):
        num = self.request.get('car')
        if num == '':
            self.redirect('/')
        else:
            key = db.Key.from_path('StreetcarLocation',num)
            car = StreetcarLocation.get(key)
            if not car:
                self.redirect('/')
            template_vals = {'num':num, 'car':car}
            path = os.path.join(os.path.dirname('__file__'),
                    'templates/car.html')
            self.response.out.write(template.render(path,template_vals))
        
