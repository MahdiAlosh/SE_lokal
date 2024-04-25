
from . import db
# . for local path folder 
# can be as Website tho
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    
    id          = db.Column(db.Integer, primary_key = True)
    data        = db.Column(db.String(1000))
    date        = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id')) # 1 to n relationship : one USER has many Notes!


#class Reminder():

# UserMixin for import 'current_user'
class User(db.Model, UserMixin): # inhirate from Database, inhirate also from UserMixin
    
    id          = db.Column(db.Integer, primary_key = True)
    email       = db.Column(db.String(100), unique = True)
    password    = db.Column(db.String(100))
    first_name  = db.Column(db.String(100))
    notes       = db.relationship('Note') # referense the class "Note"


