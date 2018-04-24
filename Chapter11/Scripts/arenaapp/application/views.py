# Geospatial for Python 3
# Chapter 11
# views.py
# by Silas Toms
#
# This script contains the views and URLs for the Arena applicaton
#
#

#Import the app object, the flask functions, and the application forms and models
from application import app
from flask import render_template,jsonify, redirect, url_for, request
from .forms import *	
from .models import *

# A redirecting URL that pushes to the arenas URL
@app.route('/', methods=["GET"])
def home():
	return redirect(url_for('arenas'))

# This function accepts web requests, finding data about each NBA arena contained within the Arenas data table
@app.route('/arenas', methods=["GET","POST"])
def arenas():
	form = ArenaForm(request.form)

	arenas = session.query(Arena).all()
	form.selections.choices = [(arena.id, arena.name) for arena in arenas]
	form.popup = "Select an Arena"
	form.latitude = 38.89517
	form.longitude = -77.03682

	if request.method == "POST":

		arena_id = form.selections.data
		arena = session.query(Arena).get(arena_id)
		form.longitude = round(arena.longitude,4)
		form.latitude = round(arena.latitude,4)

		county = session.query(County).filter(County.geom.ST_Contains(arena.geom)).first()
		if county != None:
			district = session.query(District).filter(District.geom.ST_Intersects(arena.geom)).first()
			state = county.state_ref
			form.popup = "The {0} is located at {4}, {5}, which is in {1} County, {3}, and in {3} Congressional District {2}.".format(arena.name, county.name, 
				district.district, state.name, form.longitude, form.latitude)
		else:
			form.popup = "The county, district, and state could not be located using point in polygon analysis"


		return render_template('index.html',form=form)
	return render_template('index.html',form=form)
