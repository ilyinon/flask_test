# flask_test
It is dummy project for learn some new flask function

1. Install requirements: 
     pip install -r requirements.txt
2. Install uwsgi:
     pip install uwsgi   ( there are should be also installed gcc and python-dev for compile it)
3. Install sqlite:
     yum install sqlite  (for rpm based OS)
4. Run firsty for database initialization:
     python runserver.py
5. Run uwsgi like:
     uwsgi nizheg.ini
6. Do autostart for uwsgi:
7. Add configuration to nginx
