# Ultimate Playlist
====================
## Description
An early webapp version of Spotnik.
It starts but then crashes when you try to update the playlist. The Spotify auth isn't set up right.
## Run Locally

* `python app.py`

## Screenshot


## Deploy

"""
IF IT'S CONNECTED TO THE WRONG REMOTE:
git remote rm heroku
git remote add heroku git@heroku.com:yourappname.git
"""


* Note: make sure you run `db.create_all()` to create the tables: 
```bash
$ heroku run python --app ultimateplaylist
Python 3.6.8 (default, Jan 29 2019, 19:35:16)
>>> from app import db
>>> db.create_all()
>>> exit()
```
