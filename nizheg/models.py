from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import os
import sys

Base = declarative_base()


basedir = os.path.abspath(os.path.dirname(__file__))

class Model(Base):
  __tablename__ = 'model'
  id   = Column(Integer, primary_key=True)
  name = Column(String(50))
  age  = Column(Integer)
  district = Column(Integer, ForeignKey('district.id'))

  def __repr__(self):
    return "<Model(name='%s', age='%s', district='%s')>" % (self.name, self.age, self.district)


class District(Base):
  __tablename__ = 'district'
  id   = Column(Integer, primary_key = True)
  name = Column(String(50), unique=True)
  
  def __repr__(self):
    return '<Post %r>' % (self.name)


class Image(Base):
  __tablename__ = 'image'
  id            = Column(Integer, primary_key = True)
  model_id      = Column(Integer, ForeignKey('model.id'))
  filename      = Column(String(200))
  filename_orig = Column(String(200))

  def __repr__(self):
    return '<Image %r>' % (self.filename_orig)


class Role(Base):
  __tablename__  = 'role'
  id         = Column(Integer, primary_key = True)
  rolename   = Column(String(20))

  def __repr__(self):
    return '<Rolename %r>' % (self.rolename)



class User(Base):
  __tablename__ = 'user'
  id            = Column(Integer, primary_key = True)
  username      = Column(String(20))
  password      = Column(String(20))
  email         = Column(String(100))
  registered_on = Column(DateTime)
  role_id       = Column(Integer, ForeignKey('role.id'))

  def __repr__(self):
    return '<Username %r>' % (self.username)




from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
engine = create_engine('mysql://nizheg:nizheg@localhost/nizheg?charset=utf8', pool_recycle=3600)
Base.metadata.create_all(engine)

