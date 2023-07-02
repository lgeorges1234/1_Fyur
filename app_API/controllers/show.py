from flask import flash, redirect, render_template, request, url_for, Blueprint
from app_API.forms import ShowForm
from ..models import Show, Venue, db, Artist

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

#  Create Show
#  ----------------------------------------------------------------

@show_bp.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@show_bp.route('/shows/create', methods=['POST'])
def create_show_submission():
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
  return redirect(url_for('index'))

# Export the show_bp blueprint object
__all__ = ['show_bp']
