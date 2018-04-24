import flask
from flask import render_template,jsonify, redirect, url_for, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The Geometry columns of the data tables are added to the ORM using the Geometry data type
from geoalchemy2 import Geometry

# Connect to the database called chapter11 using SQLAlchemy functions
engine = create_engine('postgresql://postgresuser:password@localhost:5432/chapter11')
Session = sessionmaker(bind=engine)
session = Session()
app = flask.Flask(__name__)

@app.route('/')
def hello():
	return "HELLO"

@app.route('/nba/api/v0.1/arenas', methods=['GET'])
def get_arenas():
	arenas = session.query(Arena).all()
	keys = ["name", "longitude", 'latitude']
	data = [{"name":arena.name, keys[1]:arena.longitude, keys[2]:arena.latitude}  for arena in arenas]
	return jsonify({'data':data})

@app.route('/nba/api/v0.1/arena/<int:arena_id>', methods=['GET'])
def get_arena(arena_id):
	print(arena_id)
	arena = session.query(Arena).get(arena_id)
	keys = ["name", "longitude", 'latitude']
	data = [{"name":arena.name, keys[1]:arena.longitude, keys[2]:arena.latitude}]
	return jsonify({'data':data})


if __name__ == '__main__':
    app.run(debug=True)