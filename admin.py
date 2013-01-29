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
        
class AddVenture(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template("addcompany.html")
        self.response.out.write(template.render())

class SaveVenture(webapp2.RequestHandler):
    def post(self):
        venture_vals = {}
        venture = Venture()
        venture_keys = ["name", "street", "city", "county", "postcode", "latitude", "longitude", "category", "website", "email", "phone"]
        for item in venture_keys:
            venture_vals[item] = cgi.escape(self.request.get(item))
        for value in venture_vals:
            setattr(venture, value, venture_vals[value])
        venture.save()
        self.redirect("/admin/venture/?uniqueid=%d" % venture.uniqueid)


class ViewVenture(webapp2.RequestHandler):
    def get(self):
        uniqueid = int(self.request.get("uniqueid"))
        venture = Venture.get_one("uniqueid", uniqueid)
        template = template_env.get_template("venture.html")
        template_vars = {"venture" : venture}
        self.response.out.write(template.render(template_vars))

app = webapp2.WSGIApplication([('/admin', AdminMainHandler),
                               ('/admin/add_venture', AddVenture),
                               ('/admin/save_venture', SaveVenture),
                               ('/admin/venture/?', ViewVenture)
                               ], debug=True)
