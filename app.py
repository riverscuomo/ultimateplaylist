import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_sqlalchemy import SQLAlchemy

from pprint import pprint

import models
from dotenv import load_dotenv
load_dotenv()
"""
Until version 0.9, Flask-WTF provided its own wrappers around the WTForms fields and validators. 
You may see a lot of code out in the wild that imports TextField, PasswordField, etc. from flask_wtforms instead of wtforms.

As of 0.9, we should be importing that stuff straight from wtforms.


https://www.youtube.com/watch?v=jTiyt6W1Qpo

install sqlite
https://www.sqlitetutorial.net/download-install-sqlite/
BUT ISN'T THIS PART OF PYTHON???

look at second option for adding sqlite to path
https://stackoverflow.com/questions/9546324/adding-directory-to-path-environment-variable-in-windows

pipenv shell
python
from app import db
db.create_all()

DEPLOYING TO HEROKU:
For existing repositories, simply add the heroku remote
$ heroku git:remote -a ultimateplaylist

oTHERWISE:
https://dashboard.heroku.com/apps/ultimateplaylist/deploy/heroku-git
"""

app = Flask(__name__)

# 3 slashes = relative

DATABASE_URL = "sqlite:///db.sqlite3"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = 'balls'
db = SQLAlchemy(app) # the db object represents the database connection
    
""" 
VIEW 

    the request method is always bound to the current http request
    if request.method = 'post' (it's checking the method you spcified in the html).  (the user clicked something to enter something.)

    OH YEAH, POST IS WHEN THE USER CLICKS ON SOMETHING TO SUBMIT THE FORM
    GET IS MORE JUST LIKE YOUR HOMEPAGE THAT AUTOMATICALLY LOADS?

    GET is the request the browser sends when you request a page
    but when we set the request with the POST method, it will not respond unless we add POST method to the decordator methods

    request.form[''] is looking at the name field, not id

    THE REQUEST OBJECT is a magic flask feature
    it's globally available, but flask makes sure it's bound to current request
    only use it inside a view function
    request attributes:
    form: form data from post or PUT requests
    ARGS: contents of the query string
    others (cookies, headers (request headers as a dict), files, method)
    AND MANY OTHERS

    THE SESSION OBJECT
    only use it inside a view function
    works by setting a cookie with flask.secret_key

    """

@app.route('/', methods=['GET'])
def index():
  playlist_id = os.environ.get('ULTIMATE_PLAYLIST_ID')
  print(playlist_id)
  return render_template('index.html', recipe=models.Recipe.query.all(), playlist_id=playlist_id)


@app.route('/add', methods=['POST'])
def add():
  r = models.Recipe(request.form['playlist'])
  db.session.add(r)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/setQuantity', methods=['GET', 'POST'])
def setQuantity():
  # if request.method == 'POST':  # inspect the HTTP request TO SEE IF THE FORM HAS BEEN SUBMITTED BY THE USER. OTHERWISE THE USER IS SIMPLY VIEWING THE FORM
  
  print('setting quantity')
# if form.validate_on_submit(): # THIS METHOD ALSO ENSURES THAT THE HTTP METHOD IS POST
  for i in range (1, 20):
    try:
      quantity = 'quantity'+str(i)
      q = request.form[quantity] # ask for any form data with the NAME ''.  FORM IS A DICT THAT CONTAINS ALL VALUES IN THE FORM.
      print(quantity)
      print('q: ', q)
      break
    except:
      continue
  
  print(request.form)
  print(type(q))
  if q == '0':
    db.session.query(models.Recipe).filter_by(id=i).delete()
    # print(f'deleteing {row}').delete()
  else:  
    db.session.query(models.Recipe).filter_by(id=i).update({"quantity":q})

  # row = models.Recipe.query.get(rowId)

  # # row = Recipe.query.get_or_404(recipeId)
  # print(row)
  # print(row.quantity)
  # # row = models.Recipe.query.filter_by(id=1).first()

  # # THIS IS GETTING THE FORM DATA, I.E. THE NUMBER YOU PUT IN
  # # q = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
  

  # row.quantity = int(q)
  # # form.populate_object(row)
  # # print(row.name)
  # print(row.quantity)

  db.session.commit()
  # flash(f"Quantity has been updated to {q}")

  return redirect(url_for('index'))  # IF THEY'RE JUST VIEWING THE FORM
  # return render_template(url_for('index'), form=form)

@app.route('/clearAll', methods=['POST'])
def clearAll():
  print('clearAll...')
  db.session.query(models.Recipe).delete()
  db.session.commit()
  flash("All ingredients cleared from your playlist recipe!")
  return redirect(url_for('index'))


@app.route('/createPlaylist', methods=['GET'])
def createPlaylist():
  print("createPlaylist...")

  allData = models.Recipe.query.all()
  rows = []
  for row in allData:
    d = {
      "name" : row.name,
      "quantity" : row.quantity,
    }
    rows.append(d)

  #   r = Recipe.query.with_entities(Recipe.name).all()
  #   r = Recipe.query.all()[0].name
  # playlistNames = [r.name for r in Recipe.query.all()]
  pprint(rows)

  """ Here we would use the latest Spotnik code instead of the old newmusic.py code below """
  import newmusic
  playlist_id = newmusic.main(rows)
  
  flash(f'Your Ultimate Playlist has been added to your Spotify account here: {playlist_id}')
  return redirect(url_for('index'))




if __name__ == '__main__':
  db.create_all()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
