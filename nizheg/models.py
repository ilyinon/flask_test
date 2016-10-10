from sqlite3    import *
from sqlalchemy import *
from nizheg     import metadata

model_table = Table(
  'model', metadata,
  Column('id', Integer, primary_key=True),
  Column('name', Unicode(50, convert_unicode=False), nullable=False),
  Column('age', Integer, CheckConstraint('age >= 18 and age < 60')),
  Column('district', Unicode(255, convert_unicode=False)),
)

user_table = Table(
  'user', metadata,
  Column('id', Integer, primary_key=True),
  Column('username', Unicode(20, convert_unicode=False), nullable=False),
  Column('password', Unicode(50, convert_unicode=False), nullable=False),
  Column('is_enabled', Boolean),
  Column('model_id', Integer, ForeignKey('model.id', ondelete="CASCADE"))
)

role_table = Table(
  'role', metadata,
  Column('id', Integer, primary_key=True),
  Column('name', Unicode(50, convert_unicode=False), unique=True)
) 
  
userroles_table = Table(
  'userroles', metadata,
  Column('id', Integer, primary_key=True),
  Column('user_id', Integer, ForeignKey('user.id', ondelete="CASCADE")),
  Column('role_id', Integer, ForeignKey('role.id', ondelete="CASCADE"))
)

district_table = Table (
  'district', metadata, 
  Column('id', Integer, primary_key=True),
  Column('district_name', Unicode(50, convert_unicode=False),
    nullable=False)
)

image_table = Table ( 
  'images', metadata,
  Column('id', Integer, primary_key = True), 
  Column('model_id', Integer, ForeignKey('model.id', ondelete="CASCADE")),
  Column('filename', Unicode(50, convert_unicode=False)),
  Column('desc', Unicode(200, convert_unicode=False)),
  Column('filename_orig', Unicode(50, convert_unicode=False))
)

metadata.create_all()
