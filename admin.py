#!/usr/bin/env python

import os
import cgi
import jinja2
import webapp2
import datetime

from google.appengine.ext import db
from models import Venture

#Prepare template environment
template_dir = os.path.dirname("templates/backend/")
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class AdminMainHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template("index.html")
        self.response.out.write(template.render())
        
class AddVenture(webapp2.RedirectHandler):
    def get(self):
        template = template_env.get_template("addcompany.html")
        self.response.out.write(template.render())
        
        
        

app = webapp2.WSGIApplication([('/admin', AdminMainHandler),
                               ('/admin/add_venture', AddVenture)
                               ], debug=True)
        
    
