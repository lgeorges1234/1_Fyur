#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import Flask, abort, jsonify, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import Table, func
from app_API.forms import ArtistForm, ShowForm, VenueForm
import sys
import json

from app_API.models import db
from app_API.controllers import *


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

moment = Moment(app)
# get the configuration from config.py
app.config.from_object('config')
db.init_app(app)
db.app = app

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):

  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


# def format_datetime(value, format="medium"):
#     date = dateutil.parser.parse(value)
#     if format == "full":
#         format = "EEEE MMMM, d, y 'at' h:mma"
#     elif format == "medium":
#         format = "EE MM, dd, y h:mma"
#     return babel.dates.format_datetime(date, format)


# app.jinja_env.filters["datetime"] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
app.register_blueprint(venue_bp)



#  ----------------------------------------------------------------
#  Artists
#  ----------------------------------------------------------------
app.register_blueprint(artist_bp)



#  Shows
#  ----------------------------------------------------------------
app.register_blueprint(show_bp)



@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    # app.debug = True
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
