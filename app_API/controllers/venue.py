import sys
from flask import abort, flash, jsonify, redirect, render_template, request, url_for, Blueprint
from app_API.forms import VenueForm
from ..helpers import shows
from ..models import db, Venue

venue_bp = Blueprint('venues', __name__)

@venue_bp.route('/venues')
def venues():
  venues = Venue.query.all()
  venues_city = Venue.query.distinct(Venue.city, Venue.state).all()

  data = []
  for place in venues_city:
    print(place)
    data.append({
      "city": place.city,
      "state": place.state,
      "venues": 
        [
          {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(shows(venue.id, "venue")[1])
          } for venue in venues if venue.city == place.city and venue.state == place.state
        ]
    })
  return render_template('pages/venues.html', areas=data)

@venue_bp.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  search_term=request.form.get('search_term', '')
  search_request = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
  response={
    "count": len(search_request),
    "data": [
      {
      "id": result.id,
      "name": result.name,
      "num_upcoming_shows": len(shows(result.id, "venue")[1]),
      } for result in search_request
    ]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@venue_bp.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

  venue_response = Venue.query.get(venue_id)

  past_shows, upcoming_shows = shows(venue_id, "venue")

  data = {
    "id": venue_response.id,
    "name": venue_response.name,
    "genres": venue_response.genres,
    "address": venue_response.address,
    "city": venue_response.city,
    "state": venue_response.state,
    "phone": venue_response.phone,
    "website": venue_response.website_link,
    "facebook_link": venue_response.facebook_link,
    "seeking_talent": venue_response.seeking_talent,
    "seeking_description": venue_response.seeking_description,
    "image_link": venue_response.image_link,
    "past_shows": [
      {
      "artist_id": show.artist_id,
      "artist_name": show.artist_name,
      "artist_image_link": show.artist_image_link,
      "start_time": show.start_time
      } for show in past_shows
    ],
    "upcoming_shows": [
      {
      "artist_id": show.artist_id,
      "artist_name": show.artist_name,
      "artist_image_link": show.artist_image_link,
      "start_time": show.start_time
      } for show in upcoming_shows
    ],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@venue_bp.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@venue_bp.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # Set the Flask Form
  form = VenueForm(request.form)

  # Validate all Fields
  if form.validate():
    try:
      name = form.name.data
      city = form.city.data
      state = form.state.data
      address = form.address.data
      phone = form.phone.data
      genres = form.genres.data
      facebook_link = form.facebook_link.data
      image_link = form.image_link.data
      website_link = form.website_link.data
      seeking_talent = form.seeking_talent.data
      seeking_description = form.seeking_description.data
      new_venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, 
      facebook_link=facebook_link, image_link=image_link, website_link=website_link, seeking_talent=seeking_talent, seeking_description=seeking_description)
      
      db.session.add(new_venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Venue ' + form.name.data + ' could not be created.')
      form = VenueForm()  
      return render_template('forms/new_venue.html', form=form)
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + '' + '' '|'.join(err))
        flash('Errors ' + str(message))
        form = VenueForm()
    return render_template('forms/new_venue.html', form=form)
  return render_template('pages/home.html')

@venue_bp.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue_to_delete = Venue.query.get(venue_id)
    db.session.delete(venue_to_delete)
    db.session.commit()
    flash('Venue ' + venue_id + ' has been deleted.')
  except ValueError as e:
    db.session.rollback()
    flash('An error occurred. Venue ' + venue_id + ' could not be deleted.')
    print(sys.exc_info)
    abort(500)
  finally:
    db.session.close()
  return jsonify({'success': True})

@venue_bp.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue_to_edit = Venue.query.get(venue_id)
  form = VenueForm(request.form)
  form.state.data=venue_to_edit.state
  form.genres.data=venue_to_edit.genres
  form.seeking_talent.data=venue_to_edit.seeking_talent
  return render_template('forms/edit_venue.html', form=form, venue=venue_to_edit)

@venue_bp.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  if form.validate():
    try:
          updated_venue = Venue.query.get(venue_id)
          updated_venue.name = form.name.data
          updated_venue.city = form.city.data
          updated_venue.state = form.state.data
          updated_venue.address = form.address.data
          updated_venue.phone = form.phone.data
          updated_venue.genres = form.genres.data
          updated_venue.facebook_link = form.facebook_link.data
          updated_venue.image_link = form.image_link.data
          updated_venue.website_link = form.website_link.data
          updated_venue.seeking_talent = form.seeking_talent.data
          updated_venue.seeking_description = form.seeking_description.data
          db.session.commit()
          flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Venue ' + form.name.data + ' could not be created.' + str(e))
        form = VenueForm()  
        return render_template('forms/new_venue.html', form=form)
    finally:
        db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + '' + '' '|'.join(err))
        flash('Errors ' + str(message))
        form = VenueForm()
    return render_template('forms/new_venue.html', form=form)
  return redirect(url_for('venues.show_venue', venue_id=venue_id))



# Export the venue_bp object
__all__ = ['venue_bp']
