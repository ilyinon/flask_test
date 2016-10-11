import sqlite3
import os
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
  render_template, flash, jsonify, send_from_directory
from  sqlalchemy import *
import config



db = create_engine('sqlite:///testdb.sqlite')
metadata = MetaData(db)

app = Flask(__name__)
app.config.from_object('config.DevConfig')
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


from . import models
from views import main_part 
