import os

from google.appengine.ext import db 
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

from models import StreetcarLocation 

class CarPage(webapp.RequestHandler):
    def get(self):
        num = self.request.get('car')
        if num == '':
            self.redirect('/')
        else:
            
            car = StreetcarLocation.get_by_key_name(num)
            if not car:
                self.redirect('/')
            user = users.get_current_user()
            status = 'unavailable'
            if not car.owner:
                status = 'available'
            elif car.owner == user:
                status = 'mine'
            template_vals = {'num':num, 'car':car, 'status':status}
            path = os.path.join(os.path.dirname('__file__'),
                    'templates/car.html')
            self.response.out.write(template.render(path,template_vals))
        
