import os

from google.appengine.ext import db 
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

from models import UserInfo 

class UserPage(webapp.RequestHandler):
    def get(self):
        user = UserInfo.get_current_user()
        if not user:
            self.redirect('/')
        template_vals = {'user':user}
        path = os.path.join(os.path.dirname('__file__'),
                'templates/user.html')
        self.response.out.write(template.render(path,template_vals))
        
