from . import db
from flask_sqlalchemy import sqlalchemy

class PropertyProfile(db.Model):
    __tablename__ = 'property_profiles'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(80))
    numbathroom = db.Column(db.String(80))
    numbedroom = db.Column(db.String(80))
    location = db.Column(db.String(80))
    price = db.Column(db.String(80))
    description = db.Column(db.Text())
    propertytype = db.Column(db.String(80))
    filename = db.Column(db.String(80))


    def __init__(self, title, numbathroom, numbedroom, location, price, description, propertytype, filename):
        self.title = title
        self.numbathroom = numbathroom
        self.numbedroom = numbedroom
        self.location = location
        self.price = price
        self.description = description
        self.propertytype = propertytype
        self.filename = filename

    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)