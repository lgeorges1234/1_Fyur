from datetime import datetime, timezone
import sys
from flask import abort, flash, jsonify, redirect, render_template, request, url_for, Blueprint
from app_API.forms import ArtistForm, ArtistForm
from ..models import Show, Venue, db, Artist
from ..helpers import shows

artist_bp = Blueprint('artists', __name__)

@artist_bp.route('/artists')
def artists():
  data = Artist.query.with_entities(Artist.id, Artist.name).all()

  return render_template('pages/artists.html', artists=data)

@artist_bp.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  search_request = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
  response={
    "count": len(search_request),
    "data": [
      {
        "id": result.id,
        "name": result.name,
        "num_upcoming_shows": len(shows(result.id, "artist")[1]),
      } for result in search_request
    ]
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@artist_bp.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  artist_response = Artist.query.get(artist_id)

  past_shows, upcoming_shows = shows(artist_id, "artist")

  data = {
    "id": artist_response.id,
    "name": artist_response.name,
    "genres": artist_response.genres,
    "city": artist_response.city,
    "state": artist_response.state,
    "phone": artist_response.phone,
    "website": artist_response.website_link,
    "facebook_link": artist_response.facebook_link,
    "seeking_venue": artist_response.seeking_venue,
    "seeking_description": artist_response.seeking_description,
    "image_link": artist_response.image_link,
    "past_shows": [
      {
      "venue_id": show.venue_id,
      "venue_name": show.venue_name,
      "venue_image_link": show.venue_image_link,
      "start_time": show.start_time
      } for show in past_shows
    ],
    "upcoming_shows": [
      {
      "venue_id": show.venue_id,
      "venue_name": show.venue_name,
      "venue_image_link": show.venue_image_link,
      "start_time": show.start_time
      } for show in upcoming_shows
    ],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@artist_bp.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist_to_edit = Artist.query.get(artist_id)
  form = ArtistForm(request.form)
  form.state.data=artist_to_edit.state
  form.genres.data=artist_to_edit.genres
  form.seeking_venue.data=artist_to_edit.seeking_venue
  return render_template('forms/edit_artist.html', form=form, artist=artist_to_edit)


@artist_bp.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  # Set the Flask Form
  form = ArtistForm(request.form)

  # Validate all Fields
  if form.validate():
    try:
      name: form.name.data
      city: form.city.data
      state: form.state.data
      phone: form.phone.data
      genres: form.genres.data
      website_link: form.website.data
      facebook_link: form.facebook_link.data
      image_link: form.image.link.data
      seeking_venue = form.seeking_venue.data
      seeking_description = form.seeking_description.data
    
      new_artist = Artist(name=name, city=city, state=state, genres=genres, phone=phone,
        facebook_link=facebook_link, image_link=image_link, website_link=website_link, seeking_venue=seeking_venue,seeking_description=seeking_description)
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + form.name.data + ' was successfully listed!')
    except ValueError as e:
      db.session.rollback()
      flash('An error occurred. Artist' + form.name.data + ' could not be created.')
      print(sys.exc_info)
      abort(500)
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + '' + '' '|'.join(err))
        flash('Errors ' + str(message))
        form = ArtistForm()
    return render_template('forms/edit_artist.html', form=form)
  return redirect(url_for('show_artist', artist_id=artist_id))



#  Create Artist
#  ----------------------------------------------------------------

@artist_bp.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@artist_bp.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

 # Set the Flask Form
  form = ArtistForm(request.form)

  # Validate all Fields
  if form.validate():
    try:
      name = form.name.data
      city = form.city.data
      state = form.state.data
      phone = form.phone.data
      genres = form.genres.data
      website_link = form.website_link.data
      facebook_link = form.facebook_link.data
      image_link = form.image_link.data
      seeking_venue = form.seeking_venue.data
      seeking_description = form.seeking_description.data
    
      new_artist = Artist(name=name, city=city, state=state, genres=genres, phone=phone,
        facebook_link=facebook_link, image_link=image_link, website_link=website_link, seeking_venue=seeking_venue,seeking_description=seeking_description)
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except ValueError:
        db.session.rollback()
        flash('An error occurred. Artist' + request.form['name']  + ' could not be created.')
        form = ArtistForm()  
        return render_template('forms/new_artist.html', form=form)
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + '' + '' '|'.join(err))
        flash('Errors ' + str(message))
        form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)
  return redirect(url_for('index'))

# Export the artist_bp object
__all__ = ['artist_bp']
