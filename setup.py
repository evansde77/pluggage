#!/usr/bin/env python

from setuptools import setup

setup(name='pluggage',
      version='0.0.2',
      description='Plugin, dynamic loading and factory utility library ',
      author='Dave Evans',
      author_email='evansde77.github@gmail.com',
      url='https://pluggage.readthedocs.org/en/latest/',
      packages=['pluggage'],
      package_dir={'pluggage': 'src/pluggage'},
      entry_points = { 
        'pluggage_modules': [
         ]
       }
     )
