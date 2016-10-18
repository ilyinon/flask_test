from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


import os
import sys
#from os import path


#from nizheg import app
basedir = os.path.abspath(os.path.dirname(__file__))

#engine = create_engine('mysql+mysqldb:///nizheg:nizheg@localhost/nizheg')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  import models
  Base.metadata.create_all(bind=engine)
