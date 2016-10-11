class Config(object):
  UPLOAD_FOLDER = '/tmp/web_file'
  ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
  DEBUG=True
  SECRET_KEY='35455450a60b0ed766efb716b1aea023'
  USERNAME='admin'
  PASSWORD='default'
  HOST='0.0.0.0'
  PORT=9000

class DevConfig(Config):
  ENV='Development'
