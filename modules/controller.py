from modules.playogo_db import PlayogoDb, Venue

class Controller():
    pass

class VenuesController(Controller):

    def venue(slug):

        db = PlayogoDb()

        venue = db.session.query(Venues).filter_by(slug=slug);

        print(venue)

        return {
            'venue_name': 'Westworld',
            'venue_street_address': '100 William St. W.',
            'venue_city': 'Waterloo',
            'venue_province': 'Ontario',
            'venue_postal_code': 'N2N 3S3'
        }