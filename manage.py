import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db

app.config


#migrate = Migrate(app, db)
#manager = 


if __name__ == '__main__':
  manager.run()
