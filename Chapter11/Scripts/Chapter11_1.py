# Chapter 11-1.py
# by Silas Toms
#
# This script demonstrates how to connect to shapefiles using the pyshp module
# and add the data to database tables using GeoAlchemy2 and SQLAlchemy
#
#

# The pyshapefile module is used to read shapefiles and
# the pygeoif module is used to convert between geometry types
import shapefile
import pygeoif

# The database connections and session management are managed with SQLAlchemy functions
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

# The Geometry columns of the data tables are added to the ORM using the Geometry data type
from geoalchemy2 import Geometry

# The built-in Tkinter GUI module allows for file dialogs
from tkinter import filedialog
from tkinter import Tk
 

# Connect to the database called chapter11 using SQLAlchemy functions
conn_string = 'postgresql://postgresuser:password@localhost:5432/chapter11'
engine = create_engine(conn_string, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


# Define the Arena class, which will model the Arena database table
class Arena(Base):
    __tablename__ = 'arena'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))

# Define the County class, which will model the County database table
class County(Base):
    __tablename__ = 'county'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    state_id = Column(Integer, ForeignKey('state.id'))
    state_ref = relationship("State",backref='county')
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))

# Define the District class, which will model the District database table
class District(Base):
    __tablename__ = 'district'
    id = Column(Integer, primary_key=True)
    district = Column(String)
    name = Column(String)
    state_id = Column(Integer, ForeignKey('state.id'))
    state_ref = relationship("State",backref='district')
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))

# Define the State class, which will model the State database table
class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    statefips = Column(String)
    stpostal = Column(String)
    counties = relationship('County', backref='state')
    districts = relationship('District', backref='state')
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))


# Initiate the Tkinter module and withdraw the console it generates
root = Tk()
root.withdraw()


# Navigate to the Arena shapefile using the Tkinter file dialog
root.arenafile =  filedialog.askopenfilename(initialdir = "/",
                                            title = "Select Arena Shapefile",
                                            filetypes = (("shapefiles","*.shp"),
                                                         ("all files", "*.*")))

# Navigate to the State shapefile using the Tkinter file dialog
root.statefile =  filedialog.askopenfilename(initialdir = "/",
                                            title = "Select State Shapefile",
                                            filetypes = (("shapefiles","*.shp"),
                                                         ("all files", "*.*")))

# Navigate to the Congressional District shapefile using the Tkinter file dialog
root.districtfile =  filedialog.askopenfilename(initialdir = "/",
                                            title = "Select Congressional District Shapefile",
                                            filetypes = (("shapefiles","*.shp"),
                                                         ("all files", "*.*")))

# Navigate to the County shapefile using the Tkinter file dialog
root.countyfile =  filedialog.askopenfilename(initialdir = "/",
                                            title = "Select County Shapefile",
                                            filetypes = (("shapefiles","*.shp"),
                                                         ("all files", "*.*")))


print(root.statefile)
print(root.arenafile)
print(root.countyfile)
print(root.districtfile)

# Read the Arena shapefile using the Reader class of the pyshp module
arena_shapefile = shapefile.Reader(root.arenafile)
arena_shapes = arena_shapefile.shapes()
arena_records = arena_shapefile.records()

# Read the County shapefile using the Reader class of the pyshp module
county_shapefile = shapefile.Reader(root.countyfile)
county_shapes = county_shapefile.shapes()
county_records = county_shapefile.records()

# Read the District shapefile using the Reader class of the pyshp module
district_shapefile = shapefile.Reader(root.districtfile)
district_shapes = district_shapefile.shapes()
district_records = district_shapefile.records()

# Read the State shapefile using the Reader class of the pyshp module
state_shapefile = shapefile.Reader(root.statefile)
state_shapes = state_shapefile.shapes()
state_records = state_shapefile.records()


# Iterate through the Arena data read from the shapefile
for count, record in enumerate(arena_records):

    # Instantiate an arena from the Arena class and populate the fields
    arena = Arena()
    arena.name = record[6]
    print(arena.name)

    # Get the district geometry associated with the current record and use
    # indexing to get the longitude and latitude for the point.
    # Insert the coordinates into a Well Known Text string template using string formatting
    point = arena_shapes[count].points[0]
    arena.longitude = float(point[0])
    arena.latitude = float(point[1])
    arena.geom = 'SRID=4326;POINT({0} {1})'.format(arena.longitude, arena.latitude)
    session.add(arena)
session.commit()

# Iterate through the State data read from the shapefile
for count, record in enumerate(state_records):

    # Instantiate a state from the State class and populate the fields
    state = State()
    state.name = record[1]
    state.statefips = record[0]
    state.stpostal = record[2]
    print(state.name)

    # Get the state geometry associated with the current record and convert it
    # into a pygeoif MultiPolygon, then into Well Known Text
    # for insertion into the data table
    state_geo = state_shapes[count]
    gshape = pygeoif.MultiPolygon(pygeoif.geometry.as_shape(state_geo))
    state.geom = 'SRID=4326;{0}'.format(gshape.wkt)

    session.add(state)
    if count % 10 == 0:
        session.commit()
session.commit()

# Iterate through the District data read from the shapefile
# This uses the STFIPS data to query the State table and find the related state
for count, record in enumerate(district_records):

    # Instantiate a district from the District class and populate the fields
    district = District()
    district.district = record[0]
    district.name = record[1]
    state = session.query(State).filter_by(statefips=record[4]).first()
    district.state_id = state.id
    print(district.name, district.district)

    # Get the district geometry associated with the current record and convert it
    # into a pygeoif MultiPolygon, then into Well Known Text
    # for insertion into the data table
    district_geo = district_shapes[count]
    gshape = pygeoif.MultiPolygon(pygeoif.geometry.as_shape(district_geo))
    district.geom = 'SRID=4326;{0}'.format(gshape.wkt)

    session.add(district)
    if count % 50 == 0:
        session.commit()
session.commit()

# Iterate through the County data read from the shapefile
# This uses the STFIPS data to query the State table and find the related state
for count, record in enumerate(county_records):

    # Instantiate a county from the County class and populate the fields
    county = County()
    county.name = record[3]
    state = session.query(State).filter_by(statefips=record[0]).first()
    county.state_id = state.id

    # Get the county geometry associated with the current record and convert it
    # into a pygeoif MultiPolygon, then into Well Known Text
    # for insertion into the data table
    county_geo = county_shapes[count]
    gshape = pygeoif.MultiPolygon(pygeoif.geometry.as_shape(county_geo))
    county.geom = 'SRID=4326;{0}'.format(gshape.wkt)

    session.add(county)
    if count % 100 == 0:
        session.commit()
session.commit()



# Close the session and dispose of the engine connection to the database
session.close()
engine.dispose()