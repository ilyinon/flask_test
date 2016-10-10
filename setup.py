from setuptools import setup

setup(
  name='nizheg',
  version='0.1',
  long_description=__doc__,
  packages=['nizheg'],
  include_package_data=True,
  zip_safe=False,
  install_requires=['Flask','SQLAlchemy']
)

