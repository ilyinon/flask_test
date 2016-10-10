from flask import *
from werkzeug.utils import secure_filename
import uuid
import os

from nizheg import app
from ..models import *



UPLOAD_FOLDER = '/tmp/web_file'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def show_models():

  j = join(model_table, image_table,
           model_table.c.id == image_table.c.model_id)
  stmt = select([model_table, image_table]).select_from(j).order_by(func.random()).group_by(model_table.c.id).limit(10)
  models=stmt.execute().fetchall()
  return render_template('show_models.html', models=models)

@app.route('/add', methods=['POST'])
def add_model():
  if not session.get('logged_in'):
    abort(401)
  stmt = model_table.insert()
  stmt.execute(   name     = request.form['name'],
                  age      = request.form['age'],
                  district = request.form['district']
)

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
  stmt = model_table.update( whereclause = model_table.c.id == model_id, 
    values = model_list )
  stmt.execute() 
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
  stmt = model_table.select()
  models=stmt.execute()
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid username or password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('show_models'))
  return render_template('login.html', error=error, models=models)

@app.route('/model/<int:model_id>',methods=['GET'])
def get_mode(model_id):
  stmt = model_table.select( model_table.c.id == model_id )
  model = stmt.execute().fetchall()

  photo = image_table.select( image_table.c.model_id == model_id ) 
  photo_list = photo.execute().fetchall()
  try: 
    model
    if len(model) == 0:
      return redirect(url_for('show_models'))
  except:
   return redirect(url_for('show_models'))
  return render_template('model.html', model=model[0], photo = photo_list  )

@app.route('/model/<int:model_id>/edit', methods=["GET", "POST"])
def edit_model_page(model_id):
  if not session.get('logged_in'):
    abort(401)
  stmt = model_table.select( model_table.c.id == model_id )
  model = stmt.execute().fetchall()
  try:
    model[0]
  except:
   return redirect(url_for('show_models'))
  return render_template('edit_model.html', model=model[0])

@app.route('/photo/<photo_id>', methods=['GET'])
def photo(photo_id):
  return render_template('photo.html', photo_id = photo_id )


@app.route('/model/<int:model_id>/upload', methods=['GET','POST'])
def upload(model_id):
  file = request.files['file']
  stmt = model_table.select( model_table.c.id == model_id )
  model = stmt.execute().fetchall()
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
    stmt = image_table.insert()
    stmt.execute( model_id = model[0].id,
                  filename     = filename,
                  desc      = "currently_stub",
                  filename_orig = filename_orig
    )

    flash('Photo  was uploaded')
    return render_template('edit_model.html', model = model[0])

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('show_models'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


