from modules.playogo_db import PlayogoDb, Venue
import os, urllib

class Controller():
    pass

class VenuesController(Controller):

    def venue(slug):

        db = PlayogoDb()

        venue = db.session.query(Venue).filter_by(id=slug).first();

        return {
            'venue_name': venue.name,
            'venue_formatted_address': venue.formatted_address,
            'venue_street_number': str(venue.street_number),
            'venue_route_short': venue.route_short,
            'venue_city': venue.city_long,
            'venue_province_short': venue.admin_area_level_1_short,
            'venue_country': venue.country_short,
            'venue_postal_code': venue.postal_code,
            'venue_lat': venue.lat,
            'venue_lng': venue.lng,
            'venue_phone_number': venue.phone_number,
            'venue_website': venue.website,
            'google_encoded_location': urllib.parse.quote_plus(venue.formatted_address),
            'google_encoded_timhortons': urllib.parse.quote_plus('Tim Horton\'s near ' + venue.formatted_address),
            'google_encoded_hotels': urllib.parse.quote_plus('Hotels near ' + venue.formatted_address),
            'google_api_key': os.environ['PLAYOGO_GMAPS_API_KEY']
        }