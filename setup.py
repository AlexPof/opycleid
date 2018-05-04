from __future__ import print_function
import sys
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]


try:
    import numpy
except ImportError:
    print('numpy is required during installation')
    sys.exit(1)

setup(name='opycleid',
      version='0.2.1',
      description='Transformational music analysis in Python',
      author='Alexandre Popoff',
      author_email='al.popoff@free.fr',
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      url='https://github.com/AlexPof/opycleid.git',
      license='BSD-3',
      )
