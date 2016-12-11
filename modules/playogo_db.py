import os, datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from playogo_flask import PlayogoFlask

# Sqalchemy singleton database
class PlayogoDb():

    # Singleton instance.
    __instance = None

    # Instantiation creates/returns the singleton instance.
    def __new__(cls):

        if PlayogoDb.__instance is None:

            PlayogoDb.__instance = SQLAlchemy(PlayogoFlask())

        return PlayogoDb.__instance

# Database instance for setup
db = PlayogoDb()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# SCHEMA ORMs
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

class VenueOwner(db.Model):
    __tablename__ = 'venue_owners'

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(50), unique=True, index=True)
    address = db.Column(db.String(50))
    city = db.Column(db.String(20))
    province_state = db.Column(db.String(20))
    postal_zip_code = db.Column(db.String(10))
    
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return '<VenueOwner %r>' % self.name

class Venue(db.Model):

    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    
    # Basic info
    name = db.Column(db.String(200), index=True)
    website = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    slug = db.Column(db.String(50))

    # Info from Google
    street_number = db.Column(db.Integer)
    route_short = db.Column(db.String(150))
    route_long = db.Column(db.String(150))
    city_short = db.Column(db.String(50))
    city_long = db.Column(db.String(50))
    admin_area_level_2_long = db.Column(db.String(50))
    admin_area_level_2_short = db.Column(db.String(50))
    admin_area_level_1_long = db.Column(db.String(50))
    admin_area_level_1_short = db.Column(db.String(50))
    country_long = db.Column(db.String(50))
    country_short = db.Column(db.String(50))
    postal_code = db.Column(db.String(10))
    lat = db.Column(db.Float(Precision=64))
    lng = db.Column(db.Float(Precision=64))
    formatted_address = db.Column(db.String(150))

    # Info from import
    import_id = db.Column(db.Integer, unique=True)
    import_address = db.Column(db.String(150))
    import_raw_address = db.Column(db.String(200))
    notes = db.Column(db.String(150))
    imported = db.Column(db.Boolean, default=False)

    # Relationship
    venue_owner_id = db.Column(db.Integer, db.ForeignKey(VenueOwner.id))
    venue_owner = db.relationship(VenueOwner, backref="venues")

    # Created/updated
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Venue %r>' % self.name

class IcePad(db.Model):

    __tablename__ = 'ice_pads'

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(50), index=True)
    width = db.Column(db.Integer)
    length = db.Column(db.Integer)
    
    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id))
    venue = db.relationship(Venue, backref="ice_pads")

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

