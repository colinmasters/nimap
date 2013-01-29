#!/usr/bin/env python

import os
import cgi
import urllib
import jinja2
import webapp2
import datetime

from google.appengine.ext import db
from google.appengine.api import users

template_dir = os.path.dirname("templates/frontend/")
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        category = self.request.get("category")
        if category:
            #Do stuff
            pass
        else:
            #Do other stuff
            pass
        categories = ["Companies", "Investment Funds", "Private Investors", "Co-working Spaces"]
        template = template_env.get_template("index.html")
        template_vars = {"categories" : categories, "coords" : [["Belfast", "54.602699", "-5.930557"],
                                                                ["Derry", "54.995933", "-7.307968"],
                                                                ["Kates House", "54.19568620658723", "-6.1399738476073935"]]}
        self.response.out.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
