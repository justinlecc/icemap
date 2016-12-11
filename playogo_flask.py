import os
from flask import Flask

# Playogo singleton
class PlayogoFlask():

    # Singleton instance.
    __instance = None

    # Instantiation creates/returns the singleton instance.
    def __new__(cls):

        if PlayogoFlask.__instance is None:
            PlayogoFlask.__instance = Flask(__name__, template_folder="templates")#,  static_url_path='/public')
            PlayogoFlask.__instance.config['SQLALCHEMY_DATABASE_URI'] = os.environ['PLAYOGO_DB_URI']

        return PlayogoFlask.__instance

