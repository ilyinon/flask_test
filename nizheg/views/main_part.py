from flask import *
from werkzeug.utils import secure_filename
from ..models import engine, Model, District, Image

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy.sql.expression import func

Session = sessionmaker(bind=engine)

db_session = Session()


import uuid
import os

from nizheg import app



UPLOAD_FOLDER = '/tmp/web_file'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def show_models():

  userList = db_session.query(Model.id, Model.name, Model.age, District.name, Image.filename).\
             join(District, Model.district ==  District.id).\
             join(Image, Model.id == Image.model_id).group_by(Model.id).limit(5).all()

  print userList

  return render_template('show_models.html', models=userList)

@app.route('/add', methods=['POST'])
def add_model():
  if not session.get('logged_in'):
    abort(401)

  new_model = Model(name     = request.form['name'], 
                    age      = request.form['age'],
                    district = request.form['district'] 
  )
  db_session.add(new_model)
  db_session.commit()

  flash('New model was successfully posted')
  return redirect(url_for('show_models'))

@app.route('/edit', methods=['POST'])
def edit_model():
  if not session.get('logged_in'):
    abort(401)
  model_id = request.form['id']
  model_name = request.form['name']
  model_age = request.form['age']
  model_district = request.form['district']

  model_list = {}

  if model_name:
    model_list['name'] =  model_name
  if model_district:
    model_list['district'] =  model_district
  if model_age:
    model_list['age'] =  model_age
#  stmt = model_table.update( whereclause = model_table.c.id == model_id, 
#    values = model_list )
#  stmt.execute() 
  flash('Model info was successful changed')
  return redirect(url_for('show_models'))

@app.route('/delete', methods=['POST'])
def delete_model():
  if not session.get('logged_in'):
    abort(401)
  model_id = request.form['id']

  stmt = model_table.delete(  model_table.c.id == model_id  )
  stmt.execute()

  flash('Model was successful deleted')
  return redirect(url_for('show_models'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
  error = None
  userList = Model.query.join(District, Model.district==District.id)

#  stmt = model_table.select()
#  models=stmt.execute()
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid username or password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('show_models'))
  return render_template('login.html', error=error, models=userList)

@app.route('/model/<int:model_id>',methods=['GET'])
def get_model(model_id):

  userList = db_session.query(Model.name, Model.age, Model.district, District.name, Model.id).\
             join(District, Model.district ==  District.id).\
             filter(Model.id == model_id).all()

  photo_list = db_session.query(Image.filename).filter(Image.model_id == model_id).all()
  try:
    userList
    if len(userList) == 0:
      return redirect(url_for('show_models'))
  except:
    pass

  return render_template('model.html', model=userList[0], photo = photo_list  )

@app.route('/model/<int:model_id>/edit', methods=["GET", "POST"])
def edit_model_page(model_id):
  if not session.get('logged_in'):
    abort(401)
  userList = db_session.query(Model.name, Model.age, Model.district, District.name, Model.id).\
              join(District, Model.district ==  District.id).\
              filter(Model.id == model_id).all()
#  stmt = model_table.select( model_table.c.id == model_id )
#  model = stmt.execute().fetchall()
  

  try:
    userList[0]
  except:
   return redirect(url_for('show_models'))
  return render_template('edit_model.html', model=userList[0])

@app.route('/photo/<photo_id>', methods=['GET'])
def photo(photo_id):
  return render_template('photo.html', photo_id = photo_id )


@app.route('/model/<int:model_id>/upload', methods=['GET','POST'])
def upload(model_id):
  file = request.files['file']
  model_list = db_session.query(Model.name, Model.age, Model.district, District.name, Model.id).\
               join(District, Model.district ==  District.id).\
               filter(Model.id == model_id).all()

  if 'file' not in request.files:
    flash('No photo here')
    return redirect('edit_model.html')
  if file.filename == '':
    flash('No selected photo')
    return redirect(request.url)
  if file and allowed_file(file.filename):
    filename_orig = secure_filename(file.filename)
    filename = str(uuid.uuid4())
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    new_image = Image(model_id = model_id,
                     filename = filename,
                     filename_orig  = filename_orig
    )
    db_session.add(new_image)
    db_session.commit()


    flash('Photo  was uploaded')
    return  render_template('edit_model.html', model=model_list[0])

@app.route('/admin', methods=['GET'])
def admin_page():
  districtList = db_session.query(District.id, District.name).order_by(District.id).all()


  return render_template('admin.html', districts=districtList)

@app.route('/edit_district', methods =['POST'])
def edit_district():

  new_district = District(name     = request.form['district']   )
  db_session.add(new_district)
  db_session.commit()
  return redirect(url_for('admin_page'))
  

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('show_models'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


