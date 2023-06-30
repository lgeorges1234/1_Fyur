from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


# show = db.Table('show',
#     db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
#     db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
#     db.Column('start_time',db.TIMESTAMP(timezone=True))
# )

# def __repr__(self):
#     return "<Shows: id_show {}, venue_id {}, artist_id {}, start_time {}".format(
#         self.id, self.venue_id, self.artist_id, self.start_time
#     )


class Show(db.Model):
    __tablename__ = 'Show'
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.TIMESTAMP(timezone=True))

    artist = db.relationship("Artist", back_populates="shows")
    venue = db.relationship("Venue", back_populates="shows")

    __table_args__ = (
        db.PrimaryKeyConstraint('artist_id', 'venue_id'),
    )

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.Text)

    # artists = db.relationship('Artist', secondary=show,
    #   backref=db.backref('artists', lazy=True))
    shows = db.relationship("Show", back_populates="venue")

    def __repr__(self):
      return f'<Venue state: {self.state}, city: {self.city}, id: {self.id}, name: {self.name}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.Text)

    shows = db.relationship("Show", back_populates="artist")

    def __repr__(self):
        return f"<Artist: id {self.id}, name {self.name} city {self.city}"

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

