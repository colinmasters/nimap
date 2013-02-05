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

class Approvals(webapp2.RequestHandler):
    def get(self):
        ventures = Venture.get_many("approved", False)
        template_vars = {"ventures" : ventures }
        template = template_env.get_template("approvals.html")
        self.response.out.write(template.render(template_vars))
        
class Approved(webapp2.RequestHandler):
    def post(self):
        uniqueid = int(cgi.escape(self.request.get("uniqueid")))
        venture = Venture.get_one("uniqueid", uniqueid)
        venture.approved = True
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
                               ('/admin/approvals', Approvals),
                               ('/admin/approved/?', Approved),
                               ('/admin/venture/?', ViewVenture)
                               ], debug=True)
