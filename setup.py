#!/usr/bin/env python
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from payex import __version__

def publish():
    """Publish to Pypi"""
    os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
    publish()
    sys.exit()

# Requirements
install_requires = [
    'suds==0.4',
]

if sys.version_info < (2, 7):
    install_requires.append('ordereddict')

setup(name='pypayex',
      version=__version__,
      description='PayEx API wrapper',
      long_description=open('README.md').read(),
      author='Funkbit AS',
      author_email='post@funkbit.no',
      url='https://github.com/funkbit/pypayex',
      packages=['payex'],
      license='BSD',
      install_requires=install_requires,
      test_suite='tests',
      classifiers = (
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        )
     )
