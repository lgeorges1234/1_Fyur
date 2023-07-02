import sys
from flask import abort, flash, jsonify, redirect, render_template, request, url_for, Blueprint
from app_API.forms import ArtistForm, ShowForm, ShowForm
from ..models import Show, Venue, db, Artist

from ..helpers import flash_errors

show_bp = Blueprint('shows', __name__)

@show_bp.route('/shows')
def shows():

  data = Show.query.join(Venue, Show.venue_id==Venue.id).join(Artist, Show.artist_id==Artist.id).with_entities(
    Venue.id.label('venue_id'),
    Venue.name.label('venue_name'),
    Artist.id.label('artist_id'),
    Artist.name.label('artist_name'),
    Artist.image_link.label('artist_image_link'),
    Show.start_time.label('start_time')
  ).all()

  return render_template('pages/shows.html', shows=data)

@show_bp.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@show_bp.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  if form.validate():
    try:
      venue_id = form.venue_id.data
      artist_id = form.artist_id.data
      start_time = form.start_time.data
      new_show = Show(venue_id=venue_id,artist_id=artist_id,start_time=start_time)
      db.session.add(new_show)
      db.session.commit()
      flash('Show was successfully listed!')
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Show: Venue '+ form.venue_id.data+' and Artist ' + form.artist_id.data + ' could not be created : ' + str(e))
      form = ShowForm()  
      return render_template('forms/new_show.html', form=form)
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + '' + '' '|'.join(err))
    flash('Errors ' + str(message))
    form = ShowForm()  
    return render_template('forms/new_show.html', form=form)
  # on successful db insert, flash success
  return redirect(url_for('index'))

# Export the artist_bp object
__all__ = ['show_bp']
