import sys
from flask import abort, flash, jsonify, redirect, render_template, request, url_for, Blueprint
from app_API.forms import VenueForm
from ..helpers import shows
from ..models import db, Venue

#Instanciate a blueprint object
venue_bp = Blueprint('venues', __name__)

#  Venue Menue
#  ----------------------------------------------------------------

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

#  Search Venue
#  ----------------------------------------------------------------

@venue_bp.route('/venues/search', methods=['POST'])
def search_venues():
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

#  Show a particular Venue
#  ----------------------------------------------------------------

@venue_bp.route('/venues/<int:venue_id>')
def show_venue(venue_id):
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

  form = VenueForm(request.form)

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

#  Delete Venue
#  ----------------------------------------------------------------

@venue_bp.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue_to_delete = Venue.query.get(venue_id)
    db.session.delete(venue_to_delete)
    db.session.commit()
    flash('Venue ' + venue_id + ' has been deleted.')
  except ValueError as e:
    db.session.rollback()
    flash('An error occurred. Venue ' + venue_id + ' could not be deleted.')
    venue = Venue.query.get(venue_id)
    return render_template('venue.html', venue=venue)
  finally:
    db.session.close()
  return jsonify({'success': True})

#  Edit Venue
#  ----------------------------------------------------------------

@venue_bp.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # Fill the Venue's edit form with the edited Venue values.
  venue_to_edit = Venue.query.get(venue_id)
  form = VenueForm(request.form)
  form.state.data=venue_to_edit.state
  form.genres.data=venue_to_edit.genres
  form.seeking_talent.data=venue_to_edit.seeking_talent
  return render_template('forms/edit_venue.html', form=form, venue=venue_to_edit)

@venue_bp.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
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



# Export the venue_bp blueprint object
__all__ = ['venue_bp']
