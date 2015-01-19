#!/usr/bin/env python

from distutils.core import setup

setup(name='picas',
      version='0.1',
      description='Python client using CouchDB as a token pool server.',
      author='Jan Bot',
      author_email='jan.bot@surfsara.nl',
      url='https://github.org/jjbot/picasclient/',
      packages=['picas'],
      requires=['couchdb (==1.0)']
     )
