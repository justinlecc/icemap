import logging, csv, os
from modules.playogo_db import PlayogoDb, VenueOwner, Venue, IcePad

class CsvIo():

    def importIcePads(self, csv_file_name, mode='add'):

        """
        High level logic
            Each line in the CSV is an ice pad from a rink. This program adds those ice pads to the
            database, adding owners and venues, using the 'Owner Name' and 'Venue Name' respectively,
            as needed. Empty fields are interpreted to be the value of that field in the preceeding
            row.

        Modes
            The 'mode' parameter enables different import types:
                1. 'add' - Adds the data to the DB that does not already exist.
                2. 'create' - Deletes all related records and populates it with all new records.

        CSV Format
            Owner Name,Venue Name,Ice Pad Name,Ice Pad Length, \
            Ice Pad Width,Street Address,City,Province,Postal 
        """

        indexes = {
            'owner_name': 0,
            'venue_name': 1,
            'ice_pad': 2,
            'ice_pad_length': 3,
            'ice_pad_width': 4,
            'street_address': 5,
            'city': 6,
            'province': 7,
            'postal': 8
        }

        current_owner = None
        current_venue = None
        current_street_address = None
        current_city = None
        current_province = None
        current_postal = None

        db = PlayogoDb();

        if mode == 'create':
            logging.debug("need to implement the deleting of records here...")
            try:
                db.session.query(IcePad).delete()
                db.session.query(Venue).delete()
                db.session.query(VenueOwner).delete()
                db.session.commit()
            except:
                db.session.rollback()
                logging.error("Failed to delete records.")
                exit()

        csv_file_path = os.getcwd() + '/import/' + csv_file_name
        logging.info("Opening file for import: " + csv_file_path)

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row_index, row in enumerate(csv_reader, start=0):

                # Ignore the file header
                if row_index == 0:
                    continue

                # Set the current owner
                if row[indexes['owner_name']] != "":
                    current_owner = row[indexes['owner_name']]

                # Set the current venue
                if row[indexes['venue_name']] != "":
                    current_venue = row[indexes['venue_name']]

                # Set the current street address
                if row[indexes['street_address']] != "":
                    current_street_address = row[indexes['street_address']]

                # Set the current city
                if row[indexes['city']] != "":
                    current_city = row[indexes['city']]

                # Set the current province
                if row[indexes['province']] != "":
                    current_province = row[indexes['province']]

                # Set the current postal
                if row[indexes['postal']] != "":
                    current_postal = row[indexes['postal']]

                # Get or create the owner
                owner = db.session.query(VenueOwner).filter_by(name=current_owner).first()
            
                if owner is None:
                    owner = VenueOwner(name=current_owner)
                    db.session.add(owner)
                    db.session.commit()
                    logging.info("Created VenueOwner: " + str(owner))

                # Get or create the venue
                venue = db.session.query(Venue) \
                            .filter_by(name=current_venue, venue_owner_id=owner.id) \
                            .first()

                if venue is None:
                
                    venue = Venue(
                        name=current_venue,
                        address=current_street_address,
                        city=current_city,
                        province_state=current_province,
                        postal_zip_code=current_postal,
                        venue_owner_id=owner.id
                    )

                    db.session.add(venue)
                    db.session.commit()
                    logging.info("Created Venue: " + str(venue))

                # Get or create the ice pad
                ice_pad = db.session.query(IcePad) \
                            .filter_by(name=row[indexes['ice_pad']], venue_id=venue.id) \
                            .first()
            
                if ice_pad is None:
                
                    length_int = None
                    width_int = None

                    if row[indexes['ice_pad_length']] != '':
                        length_int = int(row[indexes['ice_pad_length']])

                    if row[indexes['ice_pad_width']] != '':
                        width_int = int(row[indexes['ice_pad_width']])

                    ice_pad = IcePad(
                        name=row[indexes['ice_pad']],
                        length=length_int,
                        width=width_int,
                        venue_id=venue.id
                    )
                
                    db.session.add(ice_pad)
                    db.session.commit()
                    logging.info("Created IcePad: " + str(ice_pad))
