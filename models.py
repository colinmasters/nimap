import sys
import datetime

from google.appengine.ext import db

class Venture(db.Model):
    name = db.StringProperty()
    street = db.StringProperty()
    city = db.StringProperty()
    county = db.StringProperty()
    postcode = db.StringProperty()
    latitude = db.StringProperty()
    longitude = db.StringProperty()
    category = db.StringProperty()
    website = db.StringProperty()
    email = db.StringProperty()
    phone = db.StringProperty()
    logo = db.BlobProperty()
    terms = db.BooleanProperty()
    approved = db.BooleanProperty()
    uniqueid = db.IntegerProperty()
    
    @classmethod
    def get_one(cls, field, value):
        query = db.Query(Venture)
        query.filter(field, value)
        return query.get ()
        
    @classmethod
    def get_many(cls, field, value):
        query = db.Query(Venture)
        query.filter(field, value)
        return query.run()
    
    def save(self):
        try:
            uniqueid = self.key().id()
            resave = False 
        except db.NotSavedError:
            resave = True
        self.put()
        if resave:
            self.uniqueid = self.key().id()
            self.put ()