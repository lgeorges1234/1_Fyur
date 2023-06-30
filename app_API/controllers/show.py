import sys
from flask import abort, flash, jsonify, redirect, render_template, request, url_for, Blueprint
from app_API.forms import ArtistForm, ShowForm, VenueForm
from ..models import Show, db, Artist

show_bp = Blueprint('shows', __name__)

@show_bp .route('/shows')
def shows():
  # displays list of shows at /shows
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }]
  data = Show.query.all()
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
    except ValueError as e:
      db.session.rollback()
      flash('An error occurred. Artist' + form.name.data + ' could not be created.')
      print(sys.exc_info)
      return render_template('forms/new_show.html', form=form)
    finally:
      db.session.close()
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + '' + '' '|'.join(err))
        flash('Errors ' + str(message))
        form = VenueForm()  
    return render_template('forms/new_show.html', form=form)
  # on successful db insert, flash success
  return redirect(url_for('static'))

# Export the artist_bp object
__all__ = ['show_bp']
