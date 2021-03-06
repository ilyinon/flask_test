from flask import *
from werkzeug.utils import secure_filename
from ..models import engine, Model, District, Image

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy.sql.expression import func

Session = sessionmaker(bind=engine)

#db_session = Session()


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
  db_session = Session()

  userList = db_session.query(Model.id, Model.name, Model.age, District.name, Image.filename).\
             join(District, Model.district ==  District.id).\
             join(Image, Model.id == Image.model_id).group_by(Model.id).limit(5).all()
  db_session.close()
  return render_template('show_models.html', models=userList)

@app.route('/add', methods=['POST'])
def add_model():
  if not session.get('logged_in'):
    abort(401)
  db_session = Session()
  new_model = Model(name     = request.form['name'], 
                    age      = request.form['age'],
                    district = request.form['district'] 
  )
  db_session.add(new_model)
  db_session.commit()
  db_session.close()

  flash('New model was successfully posted')
  return redirect(url_for('show_models'))

@app.route('/edit', methods=['POST'])
def edit_model():
  if not session.get('logged_in'):
    abort(401)
  db_session = Session()
  if request.form['name']:
    updated_attribute = { Model.name: request.form['name']}
    db_session.query(Model).filter(Model.id == request.form['id']).update(updated_attribute)
  elif request.form['age']:
    updated_attribute = { Model.age: request.form['age']}
    db_session.query(Model).filter(Model.id == request.form['id']).update(updated_attribute)
  elif request.form['district']:
    updated_attribute = { Model.district: request.form['district']}
    db_session.query(Model).filter(Model.id == request.form['id']).update(updated_attribute)
  
  db_session.commit()
  db_session.close()

  flash('Model info was successful updated')
  return redirect('/model/'+request.form['id']+'/edit')



@app.route('/delete', methods=['POST'])
def delete_model():
  if not session.get('logged_in'):
    abort(401)
  model_id = request.form['id']
# TODO: add this functionality!

  flash('Model was successful deleted')
  return redirect(url_for('show_models'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid username or password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('show_models'))
  return render_template('login.html', error=error)

@app.route('/model/<int:model_id>',methods=['GET'])
def get_model(model_id):

  db_session = Session()
  userList = db_session.query(Model.name, Model.age, Model.district, District.name, Model.id).\
             join(District, Model.district ==  District.id).\
             filter(Model.id == model_id).all()

  photo_list = db_session.query(Image.filename).filter(Image.model_id == model_id).all()
  db_session.close()
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
  db_session = Session()
  userList = db_session.query(Model.name, Model.age, Model.district, District.name, Model.id).\
              join(District, Model.district ==  District.id).\
              filter(Model.id == model_id).all()
  try:
    userList[0]
  except:
    return redirect(url_for('show_models'))

  DistrictList = db_session.query(District.id, District.name).order_by(District.id).all()
  ImageList = db_session.query(Image.filename).filter(Image.model_id == model_id).all()
  db_session.close()

  return render_template('edit_model.html', model=userList[0], districts = DistrictList, images = ImageList)


@app.route('/photo/<photo_id>', methods=['GET'])
def photo(photo_id):
  return render_template('photo.html', photo_id = photo_id )


@app.route('/model/<int:model_id>/upload', methods=['GET','POST'])
def upload(model_id):

  db_session = Session()
  ImagesCount = db_session.query(Image.filename).\
                filter(Image.model_id == model_id).count()
  if ImagesCount >= 5:
    flash('You are reached limit of 5 photos!\n For adding new you should delete old one')
    return redirect('/model/'+str(model_id)+'/edit')

  file = request.files['file']

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
    db_session.close()

    flash('Photo  was uploaded')
    return redirect('/model/'+str(model_id)+'/edit')


@app.route('/admin', methods=['GET'])
def admin_page():
  db_session = Session()
  districtList = db_session.query(District.id, District.name).order_by(District.id).all()
  db_session.close()
  return render_template('admin.html', districts = districtList)


@app.route('/edit_district', methods =['POST'])
def edit_district():
  db_session = Session()
  new_district = District(name     = request.form['district']   )
  db_session.add(new_district)
  db_session.commit()
  db_session.close()
  return redirect(url_for('admin_page'))
  

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('show_models'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete_image/<filename>', methods=['GET', 'POST'])
def delete_image(filename):
  if not os.path.exists("os.path.join(app.config['UPLOAD_FOLDER'], filename)"):
    flash('image is not found')
  else:
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  db_session = Session()
  if db_session.query(Image).filter(Image.filename == filename).delete():
    flash('record is deleted')
  db_session.close()
  flash('Photo was deleted')
  return redirect('/')

