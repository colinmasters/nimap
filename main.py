#!/usr/bin/env python

import os
import cgi
import urllib
import jinja2
import webapp2
import datetime

from google.appengine.ext import db
from google.appengine.api import users
from models import Venture

template_dir = os.path.dirname("templates/frontend/")
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

def get_coords(ventures):
    coords = []
    for venture in ventures:
        if venture.approved:
            coord = []
            coord = []
            coord.append(str(venture.name))
            coord.append(str(venture.latitude))
            coord.append(str(venture.longitude))
            coords.append(coord)
    return coords

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template("index.html")
        ventures = Venture.all()
        coords = get_coords(ventures)
        template_vars = {"coords" : coords}
        self.response.out.write(template.render(template_vars))

class AddVenture(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template("addcompany.html")
        self.response.out.write(template.render())

class SaveVenture(webapp2.RequestHandler):
    def post(self):
        venture_vals = {}
        venture = Venture()
        venture_keys = ["name", "street", "city", "county", 
                        "postcode", "latitude", "longitude", 
                        "category", "website", "email", "phone"]
        for item in venture_keys:
            venture_vals[item] = cgi.escape(self.request.get(item))
        for value in venture_vals:
            setattr(venture, value, str(venture_vals[value]))
        venture.approved = False
        venture.save()
        self.redirect("/venture/?uniqueid=%d" % venture.uniqueid)

class FilterCategory(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template("index.html")
        category = self.request.get("category")
        ventures = Venture.get_many("category", category)
        coords = get_coords(ventures)
        template_vars = {"coords" : coords}
        self.response.out.write(template.render(template_vars))

class ViewVenture(webapp2.RequestHandler):
    def get(self):
        uniqueid = int(self.request.get("uniqueid"))
        venture = Venture.get_one("uniqueid", uniqueid)
        if venture:
            if venture.approved:
                template = template_env.get_template("venture.html")
                template_vars = {"venture" : venture}
                self.response.out.write(template.render(template_vars))
            else:
                template = template_env.get_template("unapproved.html")
                template_vars = {"venture" : venture}
                self.response.out.write(template.render(template_vars))
        else:
            template = template_env.get_template("notfound.html")
            template_vars = {"uniqueid" : uniqueid}
            

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/add', AddVenture),
                               ('/save', SaveVenture),
                               ('/category/?', FilterCategory),
                               ('/venture/?', ViewVenture),
                               ], debug=True)







