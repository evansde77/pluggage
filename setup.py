#!/usr/bin/env python

from distutils.core import setup

setup(name='pluggage',
      version='0.0',
      description='Plugin, dynamic loading and factory utility library ',
      author='Dave Evans',
      author_email='evansde77.github@gmail.com',
      url='https://pluggage.readthedocs.org/en/latest/',
      packages=['pluggage'],
      package_dir={'pluggage': 'src/pluggage'},
     )
