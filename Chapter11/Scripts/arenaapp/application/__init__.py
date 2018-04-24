# Chapter 11
# __init__.py
# by Silas Toms
#
# This script initiates the Arena application's app controler and 
# configures the connection to database tables using GeoAlchemy2 and SQLAlchemy
#
#



import flask
app = flask.Flask(__name__)
conn_string = 'postgresql://postgresuser:password@localhost:5432/chapter11'
app.config['SQLALCHEMY_DATABASE_URI'] = conn_string	
app.config['SECRET_KEY'] = "SECRET_KEY"
import application.views
