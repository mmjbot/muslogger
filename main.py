from flask import request
from controller import app
from model import Play
from flask import render_template
from decorators import login_required
from google.appengine.api import users


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/home')
def hello():
    """Return a friendly HTTP greeting."""
    plays = Play.all()
    logout_url = users.create_logout_url('/')
    logout_url_linktext = 'Logout'
    login_url = users.create_login_url('/home')
    login_url_linktext = 'Login'
    plays = sorted(plays, key=lambda x: x.time)
    return render_template('list_plays.html', plays=plays, logout_url=logout_url, logout_url_linktext=logout_url_linktext, login_url=login_url, login_url_linktext=login_url_linktext)

@app.route('/log', methods = ['POST'])
@login_required
def log():
	""" Log a play """
	print("here")
	# play = Play(artist = "Artist", album_artist = "Album Artist", album = "Album", title = "Title", user = users.get_current_user())
	play = Play(artist=request.form['artist'],
		album_artist=request.form['album_artist'],
		album=request.form['album'],
		title=request.form['title'],
		user=users.get_current_user())
	play.put()
	# flash('Play saved on database.')
	return "Success"



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404