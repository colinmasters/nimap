import sys
import datetime

from google.appengine.ext import db

class Venture(db.Model):
    name = db.StringProperty()
    address = db.StringProperty()
    category = db.StringProperty()
    website = db.StringProperty()
    logo = db.BlobProperty()
    approved = db.BooleanProperty()
    unique_id = db.IntegerProperty()
    
    @classmethod
    def get_one(cls, field, value):
        query = db.Query(Venture)
        query.filter(field, value)
        return query.run ()
        
    @classmethod
    def get_many(cls, field, value):
        query = db.Query(Venture)
        query.filter(field, value)
        return query.run()
    
    def save(self):
        try:
            unique_id = self.key().id()
            resave = False 
        except db.NotSavedError:
            resave = True
        self.put()
        if resave:
            self.unique_id = self.key().id()
            self.put ()f resave:
            self.unique_id = self.key().id()
            self.put ()