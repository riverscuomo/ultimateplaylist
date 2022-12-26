# from datetime import datetime
from app import db

"""
these classes represent a database
they work similar to the form classes in forms.py
every instance of a model class represents a row in a database table
a model class inherits from db

the db object represents the database connection and
provides all the functionality of sql-alchemy

flask-sqlalechemy is a wrapper around sqlalchemy providing xtras
it provides query function
recipe.query.get(1) gets the row with a primary key of 1
recipe.query.all() gets all the rows
recipe.query.filter_by(username="cuomo").first() returns first row matching username cuomo

"""
# calling .Model on the db instance you instantiated. inherits from 
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ins
    name = db.Column(db.String(100), nullable=False)
    # type = db.Column(db.String(100)) # playlist, artist, album, 
    quantity = db.Column(db.Integer)
    #   data = db.Column(db.DataTime, default=datetime.utcnow) # utcnow is not called yet because you want the date when the instance is added
    # user_id = db.Column(db.Integer, db.ForgeignKey('username'), nullable=False)
    def __init__(self, name):
        self.name = name
        # self.type = type
        self.quantity = 10

    def __repr__(self):
        return f"<Recipe {self.name}: {self.quantity}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # ins
    username = db.Column(db.String(80), unique=True)
    # type = db.Column(db.String(100)) # playlist, artist, album, 
    email = db.Column(db.String(120), unique=True)
    #   data = db.Column(db.DataTime, default=datetime.utcnow) # utcnow is not called yet because you want the date when the instance is added
    # recipe = db.relationship('Recipe', backref='user', lazy='dynamic')
    def __repr__(self):
        return f"<User {self.username}>"

  