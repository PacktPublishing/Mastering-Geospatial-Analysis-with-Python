# Chapter 12-0.py
# by Silas Toms
#
# This script demonstrates how to create a new database


# The database connections and session management are managed with SQLAlchemy functions
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.ext.declarative import declarative_base





engine = create_engine('postgresql://postgresuser:password@localhost:5432/chapter12', echo=True)

# Uncomment the line below if you need to drop the database (having already created it) and recreate it.
#drop_database(engine.url)


# Check to ensure that the database doesn't exist
# If it doesn't, create it and generate the PostGIS extention and tables
if not database_exists(engine.url):
    create_database(engine.url)


    # Create a direct connection to the database using the engine.
    # This will allow the new database to use the PostGIS extension.
    conn = engine.connect()
    conn.execute("commit")
    try:
        conn.execute("CREATE EXTENSION postgis")
    except Exception as e:
        print(e)
        print("extension postgis already exists")
    conn.close()
