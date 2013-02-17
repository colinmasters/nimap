#!/usr/bin/env python

import os
import cgi
import jinja2
import logging
import webapp2

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache
from models import Venture

template_dir = os.path.dirname("templates/frontend/")
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


def get_coords(ventures):
    coords = []
    for venture in ventures:
        if venture.approved:
            coord = []
            fields = ["latitude",  # 0
                      "longitude",  # 1
                      "name",  # 2
                      "street",  # 3
                      "street2",  # 4
                      "city",  # 5
                      "county",  # 6
                      "website",  # 7
                      "email",  # 8
                      "phone",  # 9
                      "uniqueid"  # 10
                      ]
            for field in fields:
                value = getattr(venture, field)
                if value != None:
                    coord.append(str(value))
                else:
                    coord.append("")
            coords.append(coord)
    return coords

def is_mobile(uastring):

    mobile_devices = ["Android", "BlackBerry", "iPhone", "iPad", "iPod",
                      "Opera Mini", "IEMobile", "Windows Phone"]

    for device in mobile_devices:
        if device in uastring:
            return True

    return False 


class MainHandler(webapp2.RequestHandler):

    def get(self):

        uastring = self.request.headers.get("user_agent")
        if is_mobile(uastring):
            self.redirect("/mobile")

        template = template_env.get_template("index.html")

        # check if we have a cached result
        cache_key = 'ventures_all'
        template_vars = memcache.get(cache_key)
        # return result from cache if found
        if template_vars is not None:
            self.response.out.write(template.render(template_vars))
            return

        logging.info('CACHE MISS: %s' % cache_key)
        # cache miss so get from datastore
        ventures = Venture.all()
        coords = get_coords(ventures)
        template_vars = {"coords": coords}
        # add template_vars to cache so subsequent checks are quicker
        memcache.set(cache_key, template_vars)

        self.response.out.write(template.render(template_vars))


class AddVenture(webapp2.RequestHandler):

    def get(self):
        template = template_env.get_template("addcompany.html")
        self.response.out.write(template.render())


class SaveVenture(webapp2.RequestHandler):

    def post(self):
        venture_vals = {}
        venture = Venture()
        venture_keys = ["name", "street", "street2", "city", "county",
                        "postcode", "latitude", "longitude",
                        "category", "website", "email", "phone"]
        for item in venture_keys:
            venture_vals[item] = cgi.escape(self.request.get(item))
        for value in venture_vals:
            setattr(venture, value, str(venture_vals[value]))

        try:
            image = self.request.get('img')
            venture.logo = db.Blob(image)
        except:
            pass

        if "http://" in venture.website:
            venture.website = venture.website.replace("http://", "")

        venture.approved = False
        venture.save()

        # flush on successful save to force cache rebuild
        memcache.flush_all()

        self.redirect("/venture/?uniqueid=%d" % venture.uniqueid)


class FilterCategory(webapp2.RequestHandler):

    def get(self):
        template = template_env.get_template("index.html")
        category = self.request.get("category")

        # check if we have a cached result
        cache_key = 'ventures_category_%s' % category
        template_vars = memcache.get(cache_key)
        # return result from cache if found
        if template_vars is not None:
            self.response.out.write(template.render(template_vars))
            return

        # cache miss so get from datastore
        logging.info('CACHE MISS: %s' % cache_key)
        ventures = Venture.get_many("category", category)
        coords = get_coords(ventures)
        template_vars = {"coords": coords}
        # add template_vars to cache so subsequent checks are quicker
        memcache.set(cache_key, template_vars)

        self.response.out.write(template.render(template_vars))


class ViewVenture(webapp2.RequestHandler):

    def get(self):

        uniqueid = int(self.request.get("uniqueid"))

        # check if we have a cached result
        cache_key = 'venture_%d' % uniqueid
        venture = memcache.get(cache_key)
        # return result from cache if found
        if venture is None:
            logging.info('CACHE MISS: %s' % cache_key)
            # cache miss so get from datastore
            venture = Venture.get_one("uniqueid", uniqueid)

        if venture:
            if venture.approved:
                template = template_env.get_template("venture.html")
                template_vars = {"venture": venture}
            else:
                template = template_env.get_template("unapproved.html")
                template_vars = {"venture": venture}
        else:
            template = template_env.get_template("notfound.html")
            template_vars = {"uniqueid": uniqueid}

        # add template_vars to cache so subsequent checks are quicker
        memcache.set(cache_key, venture)
        self.response.out.write(template.render(template_vars))


class MobileVersion(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template("mobile.html")

        # check if we have a cached result
        cache_key = 'ventures_all'
        template_vars = memcache.get(cache_key)
        # return result from cache if found
        if template_vars is not None:
            self.response.out.write(template.render(template_vars))
            return

        logging.info('CACHE MISS: %s' % cache_key)
        # cache miss so get from datastore
        ventures = Venture.all()
        coords = get_coords(ventures)
        template_vars = {"coords": coords}
        # add template_vars to cache so subsequent checks are quicker
        memcache.set(cache_key, template_vars)

        self.response.out.write(template.render(template_vars))


class ServeLogo(webapp2.RequestHandler):

    def get(self):

        uniqueid = int(self.request.get("uniqueid"))

        # check if we have a cached result
        cache_key = 'venture_image_%s' % uniqueid
        image = memcache.get(cache_key)
        # return result from cache if found
        if image is not None:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(image)
            return

        logging.info('CACHE MISS: %s' % cache_key)
        venture = Venture.get_one("uniqueid", uniqueid)
        image = venture.logo
        if venture.logo:
            image = images.resize(image, 96, 96)
            self.response.headers['Content-Type'] = 'image/png'
            # add image to cache so subsequent checks are quicker
            memcache.set(cache_key, image)
            self.response.out.write(image)
        else:
            self.abort(404)


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/add', AddVenture),
                               ('/save', SaveVenture),
                               ('/category/?', FilterCategory),
                               ('/venture/?', ViewVenture),
                               ('/logo/?', ServeLogo),
                               ('/mobile', MobileVersion)
                               ], debug=True)
