import sys
from flask import abort, flash, jsonify, redirect, render_template, request, url_for, Blueprint
from app_API.forms import ArtistForm, VenueForm
from ..models import db, Artist

artist_bp = Blueprint('artists', __name__)

@artist_bp.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  data = []
  artists = Artist.query.with_entities(Artist.id, Artist.name)
  for artist in artists:
    data.append(artist)
  return render_template('pages/artists.html', artists=data)

@artist_bp.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  search_request = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
  response={
  "count": search_request.count(),
  "data": [
    {
      "id": result.id,
      "name": result.name,
      "num_upcoming_shows": 0,
    } for result in search_request
  ]
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@artist_bp.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  data = Artist.query.get(artist_id)
  return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@artist_bp.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>

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
        form = VenueForm()
    return render_template('forms/edit_artist.html', form=form)
  return render_template('pages/home.html', form=form, artist=new_artist)

@artist_bp.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

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
    except ValueError as e:
        db.session.rollback()
        flash('An error occurred. Artist' + request.form['name']  + ' could not be created.')
        print(sys.exc_info)
        abort(500)
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + '' + '' '|'.join(err))
        flash('Errors ' + str(message))
        form = VenueForm()
    return render_template('forms/new_artist.html', form=form)
  return redirect(url_for('/'))

# Export the artist_bp object
__all__ = ['artist_bp']
