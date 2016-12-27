from modules.playogo_db import PlayogoDb, Venue
from bs4 import BeautifulSoup
import os, urllib, json, logging

class VenueSearch():

    def get_lat_lng(location_string):
        encoded_address = urllib.parse.quote_plus(location_string)
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + encoded_address + '&key=' + os.environ['PLAYOGO_GMAPS_API_KEY'])
        content_string = BeautifulSoup(response.content, 'html.parser').prettify()
        data = json.loads(content_string)

        if data['status'] != 'OK' or len(data['results']) == 0:
            logging.error("Request to google for lat/long failed with location_string: " + location_string)
            return (None, None, 1)

        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']

        return (lat, lng, 0)

    def get_closest_venues(origin_lat, origin_lng):

        db = PlayogoDb()

        # Query from here:
        #  http://stackoverflow.com/questions/2234204/
        #   latitude-longitude-find-nearest-latitude-longitude-complex-sql-or-complex-calc
        sql = """
            SELECT subqueryvenues.*
            FROM (
                SELECT v.*, SQRT(
                    POW(69.1 * (lat - :lat), 2) +
                    POW(69.1 * (:lng - lng) * COS(lat / 57.3), 2)) AS distance
                FROM venues AS v
            ) AS subqueryvenues
            WHERE distance < :distance_limit ORDER BY distance;
            """
        result = db.session.execute(sql, {'lat': origin_lat, 'lng': origin_lng, 'distance_limit': 100})

        raw_venues = result.fetchall()

        origins_string = str(origin_lat) + "," + str(origin_lng)
        destinations_string = ''

        for i, raw_venue in enumerate(raw_venues):

            destinations_string += str(raw_venue['lat']) + "," + str(raw_venue['lng'])

            if i < len(raw_venues) - 1:

                destinations_string += "|"

        encoded_origins = urllib.parse.quote_plus(origins_string)
        encoded_destinations = urllib.parse.quote_plus(destinations_string)
        response = requests.get( \
            'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + \
                encoded_origins + '&destinations=' + encoded_destinations + '&key=' + \
                os.environ['PLAYOGO_GMAPS_API_KEY'] \
        )
        content_string = BeautifulSoup(response.content, 'html.parser').prettify()
        data = json.loads(content_string)

        venues_info = []

        for i, raw_venue in enumerate(raw_venues):

            if i < len(data['rows'][0]['elements']):
                duration_text = data['rows'][0]['elements'][i]['duration']['text']
            else:
                duration_text = 'Driving distance not available.'

            venues_info.append({
                'duration_text': duration_text,
                'venue': Venue(
                            id=raw_venue['id'],
                            name=raw_venue['name'],
                            website=raw_venue['website'],
                            phone_number=raw_venue['phone_number'],
                            slug=raw_venue['slug'],
                            street_number=raw_venue['street_number'],
                            route_short=raw_venue['route_short'],
                            route_long=raw_venue['route_long'],
                            city_short=raw_venue['city_short'],
                            city_long=raw_venue['city_long'],
                            admin_area_level_2_long=raw_venue['admin_area_level_2_long'],
                            admin_area_level_2_short=raw_venue['admin_area_level_2_short'],
                            admin_area_level_1_long=raw_venue['admin_area_level_1_long'],
                            admin_area_level_1_short=raw_venue['admin_area_level_1_short'],
                            country_long=raw_venue['country_long'],
                            country_short=raw_venue['country_short'],
                            postal_code=raw_venue['postal_code'],
                            lat=raw_venue['lat'],
                            lng=raw_venue['lng'],
                            formatted_address=raw_venue['formatted_address'],
                            import_id=raw_venue['import_id'],
                            import_address=raw_venue['import_address'],
                            import_raw_address=raw_venue['import_raw_address'],
                            notes=raw_venue['notes'],
                            venue_owner_id=raw_venue['venue_owner_id']
                        )
            })

        return venues_info
