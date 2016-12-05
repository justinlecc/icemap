import os, sys, logging, subprocess
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from playogo_flask import PlayogoFlask
from modules.playogo_db import PlayogoDb
from router import Router
from modules.csv_io import CsvIo

# Config log files
# Logging levels
#   1. debug    - detailed info
#   2. info     - confirmation that things are working
#   3. warning  - something unexpected happened
#   4. error    - a function failed
#   5. critical - the application failed
if os.environ['PLAYOGO_ENV'] == 'LOCAL':
    # logging.basicConfig(filename=os.environ['PLAYOGO_LOGFILE'], level=logging.DEBUG)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
else:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Initialize Flask here for AWS Elastic Beanstalk to import
application = PlayogoFlask()
application.debug = True

# Apply routes to Flask
router = Router()
router.apply_routes(application)

if (__name__ == "__main__"):

    # This process ran 'python application.py' so run the webserver
    if len(sys.argv) == 1:
        application.run()

    # Otherwise, see what the user wants...
    process_type = None
    param1 = None
    param2 = None

    if len(sys.argv) >= 2:
        process_type = sys.argv[1]

    if len(sys.argv) >= 3:
        param1 = sys.argv[2]

    if len(sys.argv) >= 4:
        param2 = sys.argv[3]

    # Run this as an assessment process
    if 'db' == process_type:

        try:
            # Migration command setup
            migrate = Migrate(application, PlayogoDb())
            manager = Manager(application)
            manager.add_command('db', MigrateCommand)

            # NOTE: This works when called as python application.py db migrate/upgrade
            #   Its innerworking are somewhat magical to me at this point. Would be good
            #   to provide the manager params in a different way than through 'argv'.
            manager.run()

        except Exception as e:

            logging.error("Failed to run the DB process - " + str(e))

    # Run this process as an import script
    elif 'import' == process_type:

        try:

            if param1 is not None:

                # Options passed to import process
                if param1[0] == '-':

                    # Run in 'create' mode (delete records and import)
                    if 'c' in param1:
                        CsvIo().importIcePads(param2, 'create')

                    else:
                        logging.error("Unknown option passed to import process")
                        exit()

                # Run as default import (adding unseen records)
                else:
                    CsvIo().importIcePads(param1)

            else:

                logging.warning("The import process was not given the parameter it was expecting.")

        except Exception as e:

            logging.error("Failed to run the import process process - " + str(e))