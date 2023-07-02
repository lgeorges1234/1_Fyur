from datetime import datetime, timezone
from flask import flash

from .models import Venue, Show, Artist


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in field '{getattr(form, field).label.text}': {error}")


def shows(id, name):
    current_time = datetime.now(timezone.utc)

    show_response = Show.query.join(Venue).join(Artist).with_entities(
        Show.start_time.label("start_time"),
        Venue.id.label('venue_id'),
        Venue.name.label('venue_name'),
        Venue.image_link.label('venue_image_link'),
        Artist.id.label('artist_id'),
        Artist.name.label('artist_name'),
        Artist.image_link.label('artist_image_link')
    ).filter(getattr(Show, name + '_id')==id).all()

    past_shows = []
    upcoming_shows = []

    for show in show_response:

        if show.start_time < current_time:
            past_shows.append(show)
        else:
            upcoming_shows.append(show)

    return past_shows, upcoming_shows