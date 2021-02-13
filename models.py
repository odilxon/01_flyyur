from app import db
from datetime import datetime
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
    genres = db.Column(db.String)
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref="Venue", lazy=True)
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
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref="Artist", lazy=True)

class Show(db.Model):
  __tablename__ = "Show"
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"))
  artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"))
  start_time = db.Column(db.DateTime)



def Show_Venue(data):
    places = []
    for v in data:
      if (v.city,v.state) not in places:
        places.append((v.city, v.state))
    res = []
    for place in places:
      ve = {"city": place[0], "state": place[1], "venues": []}
      for v in data:
        if (v.city,v.state) == place:
          shows = Show.query.filter_by(venue_id=v.id).all()
          num_up_shows = 0
          for show in shows:
            if show.start_time > datetime.now():
              num_up_shows+=1
          d = {
            "id" : v.id,
            "name" : v.name,
            "num_upcoming_shows" : num_up_shows
          }
          ve["venues"].append(d)
      res.append(ve)
    return res
def Search_Venue(data, seach_term):
    response = {
      "count": 0,
      "data": []
    }
    string = seach_term.lower()
    for v in data:
        if string in v.name.lower().split():
          shows = Show.query.filter_by(venue_id=v.id).all()
          num_up_shows = 0
          for show in shows:
            if show.start_time > datetime.now():
              num_up_shows+=1
          ven = {
            "id" : v.id,
            "name" : v.name,
            "num_upcoming_shows" : num_up_shows
          }
          response["data"].append(ven)
          response["count"]+=1
    return response


    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
def Show_Artist(artists):
  data = []
  for artist in artists:
    ar = {
      "id" : artist.id,
      "name" : artist.name
    }
    data.append(ar)
  return data
def Search_Artist(data, seach_term):
  response = {
    "count" : 0,
    "data" : []
  }
  string = seach_term.lower()
  for a in data:
    if string in a.name.lower().split():
      shows = Show.query.filter_by(artist_id=a.id).all()
      num_up_shows = 0
      for show in shows:
        if show.start_time > datetime.now():
          num_up_shows+=1
      ar = {
        "id" : a.id,
        "name" : a.name,
        "num_upcoming_shows" : num_up_shows
      }
      response["data"].append(ar)
      response["count"] += 1
  return response



def Show_shows(shows):
  data = []
  
  for show in shows:
    
    ven = Venue.query.get(show.venue_id)
    art = Artist.query.get(show.artist_id)
    print(type(show.start_time))
    sh = {
      "venue_id" : ven.id,
      "venue_name" : ven.name,
      "artist_id" : art.id,
      "artist_name" : art.name,
      "artist_image_link" : art.image_link,
      "start_time" : str(show.start_time)
    }
    data.append(sh)
  return data
def Shows_for_Venue(data):
  now = datetime.now()
  venue = db.session.query(Venue).filter(Venue.id == data["id"]).one()
  shows = db.session.query(Show)
  join_venue = shows.join(Venue)
  show_for_venue = join_venue.filter(Show.venue_id == data["id"])
  
  data["upcoming_shows"] = []
  data["upcoming_shows_count"] = 0
  data["past_shows"] = []
  data["past_shows_count"] = 0
  
  for show in show_for_venue:
    art = Artist.query.get(show.artist_id)
    sh = {
      "artist_id" : show.venue_id,
      "artist_name" : art.name,
      "artist_image_link" : art.image_link,
      "start_time" : str(show.start_time)
    }
    if now < show.start_time:
      data["upcoming_shows"].append(sh)
      data["upcoming_shows_count"] += 1
    else:
      data["past_shows"].append(sh)
      data["past_shows_count"] += 1
  return data

def Shows_for_Artist(data):
  now = datetime.now()
  data["upcoming_shows"] = []
  data["upcoming_shows_count"] = 0
  data["past_shows"] = []
  data["past_shows_count"] = 0
  
  artist = db.session.query(Artist).filter(Artist.id == data["id"]).one()
  shows = db.session.query(Show)
  join_artist = shows.join(Artist)
  show_for_artist = join_artist.filter(Show.artist_id == data["id"])
  
  
  for show in show_for_artist:
    ven = Venue.query.get(show.venue_id)
    sh = {
      "venue_id" : show.venue_id,
      "venue_name" : ven.name,
      "venue_image_link" : ven.image_link,
      "start_time" : str(show.start_time)
    }
    if now < show.start_time:
      data["upcoming_shows"].append(sh)
      data["upcoming_shows_count"] += 1
    else:
      data["past_shows"].append(sh)
      data["past_shows_count"] += 1
  return data
