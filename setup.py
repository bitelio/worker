from os import path
from setuptools import setup


def version():
    init = path.join(path.dirname(__file__), 'worker', '__init__.py')
    line = list(filter(lambda l: l.startswith('__version__'), open(init)))[0]
    return line.split('=')[-1].strip(" '\"\n")


setup(name='worker',
      packages=['worker'],
      version=version(),
      author='Guillermo Guirao Aguilar',
      author_email='info@bitelio.com',
      url='https://github.com/bitelio/worker',
      entry_points={'console_scripts': ['worker = worker:run']})
