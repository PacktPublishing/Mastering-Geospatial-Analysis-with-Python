# Geospatial for Python 3
# Chapter 13
# views.py
# by Silas Toms
#
# This script contains the views and URLs for the Arena REST API
#
#

#Import the app object, the flask functions, and the application forms and models
from application import app
from flask import render_template,jsonify, redirect, url_for, request, Markup
from .forms import *	
from .models import *
import geoalchemy2,shapely
from geoalchemy2.shape import to_shape


@app.route('/', methods=['GET'])
def get_api():
	return redirect('/nba/api/v0.1')


@app.route('/nba/api/v0.1', methods=['GET'])
def get_endpoints():
	data= [{'name':"Arena", "endpoint":"/arena"},
	{'name':"State", "endpoint":"/state"},
	{'name':"County", "endpoint":"/county"},
	{'name':"District", "endpoint":"/district"},]
	return jsonify({"endpoints":data})



@app.route('/nba/api/v0.1/arena', methods=['GET'])
def get_arenas():
	arenas = session.query(Arena).all()
	data = [{"type": "Feature",
	"properties":{"name":arena.name, "id":arena.id}, 
	"geometry":{"type":"Point",	
	"coordinates":[round(arena.longitude,6), round(arena.latitude,6)]},
	}  for arena in arenas]
	return jsonify({"type": "FeatureCollection","features":data})

@app.route('/nba/api/v0.1/arena/<int:arena_id>', methods=['GET'])
def get_arena(arena_id):
	arena = session.query(Arena).get(arena_id)
	if arena != None:
		data = [{"type": "Feature",
		"properties":{"name":arena.name, "id":arena.id},  
		"geometry":{"type":"Point",	
		"coordinates":[round(arena.longitude,6), round(arena.latitude,6)]}, 
		}]
	else:
		data = []
	return jsonify({"type": "FeatureCollection","features":data})

@app.route('/nba/api/v0.1/arena/<arena_name>', methods=['GET'])
def get_arena_name(arena_name):
	arenas = session.query(Arena).filter(Arena.name.like(arena_name+"%")).all()
	data = [{"type": "Feature",
	"properties":{"name":arena.name}, 
	"geometry":{"type":"Point",	
	"coordinates":[round(arena.longitude,6), round(arena.latitude,6)]}, 
	} for arena in arenas]
	return jsonify({"type": "FeatureCollection","features":data})

# @app.route('/nba/api/v0.1/arena/<int:arena_id>/intersect', methods=['GET'])
# def arena_interset(arena_id):
# 	arena = session.query(Arena).get(arena_id)
# 	county = session.query(County).filter(County.geom.ST_Intersects(arena.geom)).first()
# 	district = session.query(District).filter(District.geom.ST_Intersects(arena.geom)).first()
# 	if county !=None:
# 		properties = {"name":arena.name, "id":arena.id, "district":district.district, "county":county.name, "state":county.state_ref.name}
# 	else:
# 		properties = {"name":arena.name, "id":arena.id,} 
# 	data = [{"type": "Feature", "properties": properties,
# 	"geometry":{"type":"Point", "coordinates":[round(arena.longitude,6), round(arena.latitude,6)]}, 
# 	}]
# 	return jsonify({"type": "FeatureCollection","features":data})

@app.route('/nba/api/v0.1/arena/<int:arena_id>/intersect', methods=['GET'])
def arena_intersect(arena_id):
	arena = session.query(Arena).get(arena_id)
	county = session.query(County).filter(County.geom.ST_Intersects(arena.geom)).first()
	district = session.query(District).filter(District.geom.ST_Intersects(arena.geom)).first()
	if county != None:
		data = [{"type": "Feature", "properties": {"name":arena.name, "id":arena.id,} ,
		"geometry":{"type":"Point", "coordinates":[round(arena.longitude,6), round(arena.latitude,6)]}, 
		},{"type": "Feature", "properties": {"name":county.name, "id":county.id,} ,
		"geometry":{"type":"MultiPolygon", 
		"coordinates":[shapely.geometry.geo.mapping(to_shape(county.geom))]}, 
		},{"type": "Feature", "properties": {"name":district.district, "id":district.id,},
		"geometry":{"type":"MultiPolygon", 
		"coordinates":[shapely.geometry.geo.mapping(to_shape(district.geom))]}, 
		},{"type": "Feature", "properties": {"name":county.state_ref.name, "id":county.state_ref.id,},
		"geometry":{"type":"MultiPolygon", 
		"coordinates":[shapely.geometry.geo.mapping(to_shape(county.state_ref.geom))]}, 
		}
		]
		return jsonify({"type": "FeatureCollection","features":data})
	else:
		return redirect('/nba/api/v0.1/arena/' + str(arena_id))

@app.route('/nba/api/v0.1/county', methods=['GET'])
def get_counties():
	counties = session.query(County).all()
	geoms = {county.id:shapely.geometry.geo.mapping(to_shape(county.geom)) for county in counties}
	data = [{"type": "Feature",	
	"properties":{"name":county.name, "state":county.state.name}, 
	"geometry":{"type":"MultiPolygon",	
	"coordinates":geoms[county.id]["coordinates"]},
	} for county in counties]
	return jsonify({"type": "FeatureCollection","features":data})

@app.route('/nba/api/v0.1/county/query/size/<float:size>', methods=['GET'])
def get_county_size(size):
	counties = session.query(County).filter(County.geom.ST_Area() > size).all()
	data = [{"type": "Feature",	
	"properties":{"name":county.name,"id":county.id ,"state":county.state.name}, 
	"geometry":{"type":"MultiPolygon",	
	"coordinates":[shapely.geometry.geo.mapping(to_shape(county.geom))["coordinates"]]},
	} for county in counties]
	return jsonify({"type": "FeatureCollection","features":data})

@app.route('/nba/api/v0.1/county/<int:county_id>', methods=['GET'])
def get_county(county_id):
	
	county = session.query(County).get(county_id)
	shp = to_shape(county.geom)
	geojson = shapely.geometry.geo.mapping(shp)
	data = [{"type": "Feature",
	"properties":{"name":county.name, "state":county.state.name}, 
	"geometry":{"type":"MultiPolygon",	
	"coordinates":[geojson]}, #"["+str(rnd(arena.geom.x,5)) + str(rnd(arena.geom.x,5))+"]"
	}]
	return jsonify({"type": "FeatureCollection","features":data})

@app.route('/nba/api/v0.1/county/<county_name>', methods=['GET'])
def get_county_name(county_name):
	counties = session.query(County).filter(County.name.like(county_name+"%")).all()
	data = [{"type": "Feature",	
	"properties":{"name":county.name,  "state":county.state.name}, 
	"geometry":{"type":"MultiPolygon",	
	"coordinates":[shapely.geometry.geo.mapping(to_shape(state.geom))["coordinates"]]},
	} for county in counties]
	return jsonify({"type": "FeatureCollection","features":data})

# @app.route('/nba/api/v0.1/states', methods=['GET'])
# def get_states():
# 	states = session.query(State).all()
# 	geoms = {state.id:smapping(to_shape(state.geom)) for state in states}

# 	data = [{"type": "Feature",	
# 	"properties":{"state":state.name}, 
# 	"geometry":{"type":"MultiPolygon",	
# 	"coordinates":geoms[state.id]["coordinates"]},
# 	} for state in states]
# 	return jsonify({"type": "FeatureCollection","features":data})

@app.route('/nba/api/v0.1/state', methods=['GET'])
def get_states():
	states = session.query(State).all()
	data = [{"type": "Feature",	
	"properties":{"state":state.name,"id":state.id}, 
	"geometry":{"type":"MultiPolygon",	
	"coordinates":"[Truncated]"},
	} for state in states]
	if "geometry" in request.args.keys():
		if request.args["geometry"]=='1' or request.args["geometry"]=='True':
			data = [{"type": "Feature",	
			"properties":{"state":state.name,"id":state.id}, 
			"geometry":{"type":"MultiPolygon",	
			"coordinates":[shapely.geometry.geo.mapping(to_shape(state.geom))["coordinates"]]},
			} for state in states]
	return jsonify({"type": "FeatureCollection","features":data})


@app.route('/nba/api/v0.1/state/<int:state_id>', methods=['GET'])
def get_state(state_id):
	
	state = session.query(State).get(state_id)
	shp = to_shape(state.geom)
	geojson = shapely.geometry.geo.mapping(shp)
	data = [{"type": "Feature",
	"properties":{"name":state.name,"id":state.id}, 
	"geometry":{"type":"MultiPolygon",	
	"coordinates":[geojson]},
	}]
	return jsonify({"type": "FeatureCollection","features":data})

@app.route('/nba/api/v0.1/state/<int:state_id>/within', methods=['GET'])
def get_state_arenas(state_id):
	
	state = session.query(State).get(state_id)
	shp = to_shape(state.geom)
	geojson = shapely.geometry.geo.mapping(shp)
	data = [{"type": "Feature",
	"properties":{"name":state.name,"id":state.id}, 
	"geometry":{"type":"MultiPolygon",	
	"coordinates":[geojson]},
	}]
	arenas = session.query(Arena).filter(Arena.geom.ST_Within(state.geom))
	data_arenas =[{"type": "Feature",
	"properties":{"name":arena.name}, 
	"geometry":{"type":"Point",	
	"coordinates":[round(arena.longitude,6), round(arena.latitude,6)]}, 
	} for arena in arenas]
	data.extend(data_arenas)
	return jsonify({"type": "FeatureCollection","features":data})

@app.route('/nba/api/v0.1/state/<state_name>', methods=['GET'])
def get_state_name(state_name):
	states = session.query(State).filter(State.name.like(state_name+"%")).all()
	data = [{"type": "Feature",	
	"properties":{"state":state.name,"id":state.id}, 
	"geometry":{"type":"MultiPolygon",	
	"coordinates":[shapely.geometry.geo.mapping(to_shape(state.geom))["coordinates"]]},
	} for state in states]
	return jsonify({"type": "FeatureCollection","features":data})


@app.route('/nba/api/v0.1/district', methods=['GET'])
def get_districts():
	districts = session.query(District).all()
	if 'geometry' in request.args.keys() and request.args['geometry'] in ('1','True'):
		data = [{"type": "Feature", 
		"properties":{"representative":district.name, "district":district.district,
		"state": district.state_ref.name, "id":district.id}, 
		"geometry":{"type":"MultiPolygon", 
		"coordinates":shapely.geometry.geo.mapping(to_shape(district.geom))["coordinates"]},
		} for district in districts]
	else:
		data = [{"type": "Feature", 
		"properties":{"representative":district.name, "district":district.district,
		"state": district.state_ref.name, "id":district.id}, 
		"geometry":{"type":"MultiPolygon", 
		"coordinates":["Truncated"]},
		} for district in districts]
	return jsonify({"type": "FeatureCollection","features":data})



@app.route('/nba/api/v0.1/district/<int:district_id>', methods=['GET'])
def get_district(district_id):
	
	district = session.query(District).get(district_id)
	shp = to_shape(district.geom)
	geojson = shapely.geometry.geo.mapping(shp)
	data = [{"type": "Feature",
	"properties":{"district":district.district,"id":district.id}, 
	"geometry":{"type":"MultiPolygon",	
	"coordinates":[geojson]},
	}]
	return jsonify({"type": "FeatureCollection","features":data})

@app.route('/nba/api/v0.1/district/<district_name>', methods=['GET'])
def get_district_name(district_name):
	

	districts = session.query(District).filter(District.name.like(district_name+"%")).all()
	geoms = {district.id:smapping(to_shape(district.geom)) for district in districts}

	data = [{"type": "Feature",	
	"properties":{"state":district.name}, 
	"geometry":{"type":"MultiPolygon",	
	"coordinates":geoms[state.id]["coordinates"]},
	} for district in districts]
	return jsonify({"type": "FeatureCollection","features":data})






@app.route('/nba/api/v0.1/arena/add', methods=['GET', 'POST'])
def add_arenas():
	form = AddForm(request.form)
	form.name.data = "New Arena"
	form.longitude.data = -121.5
	form.latitude.data = 37.8
	if request.method == "POST":
		arena = Arena()
		arena.name = request.form['name']
		arena.longitude, arena.latitude = float(request.form['longitude']), float(request.form['latitude'])
		arena.geom = 'SRID=4326;POINT({0} {1})'.format(arena.longitude, arena.latitude)
		session.add(arena)
		arena = session.query(Arena).filter(Arena.name== request.form['name']).first()
		data = [{"type": "Feature", "properties":{"id":arena.id, "name":arena.name}, 
		"geometry":{"type":"Point", 
		"coordinates":[round(arena.longitude,6), round(arena.latitude,6)]},}]
		return jsonify({'added':'success',"type": "FeatureCollection","features":data})
	return render_template('addarena.html', form=form)



@app.route('/nba/api/v0.1/arena/delete/<int:arena_id>', methods=['DELETE'])
def delete_arena(arena_id):
  arena = session.query(Arena).delete(arena_id)
  return jsonify({"deleted":"success"})


