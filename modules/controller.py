from modules.playogo_db import PlayogoDb, Venue
from modules.venue_search import VenueSearch
from bs4 import BeautifulSoup
import os, urllib, requests, json, logging

class Controller():
    pass


class VenuesController(Controller):

    def search_results(search_query):

        db = PlayogoDb()

        lat, lng, err = VenueSearch.get_lat_lng(search_query)

        if err:
            logging.error("VenueSearch::get_lat_lng failed.")
            return {
                'closest_venues': [],
                'search_query': search_query,
                'error': "Sorry but there was a problem processing your request. If this problem persists please report it to playogosports@gmail.com."
            }

        closest_venues = VenueSearch.get_closest_venues(lat, lng)

        return {
            'closest_venues': closest_venues,
            'search_query': search_query,
            'encoded_search_query': urllib.parse.quote_plus(search_query)
        }

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

    def home_page():
        return {}


