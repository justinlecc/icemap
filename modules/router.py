from flask import request, render_template, send_from_directory
import subprocess, os
from modules.controller import VenuesController

class Router():

    def __init__(app):
        pass

    def apply_routes(self, app):

        # AVAILABILITY ENDPOINTS

        # Test the availability of Playogo
        @app.route("/status", methods=['GET', 'POST'])
        def status ():
            return "Playogo is available"

        # VENUE ENDPOINTS

        @app.route("/rinks/<slug>", methods=['GET'])
        def venue (slug):
            return render_template('venue.html', params=VenuesController.venue(slug))

        # STATIC FILES
        #   Only serve static files through flask in development.
        #   Configure AWS to serve static files in production.
        if os.environ['PLAYOGO_ENV'] == 'LOCAL':

            # Javascript files
            @app.route('/public/js/<path:path>')
            def send_js(path):
                print("path: " + path)
                return send_from_directory('public/js', path)

            # Css files
            @app.route('/public/css/<path:path>')
            def send_css(path):
                print("path: " + path)
                return send_from_directory('public/css', path)

            