#!/usr/bin/env python

__author__ = 'Kazuki Inamura'
__email__ = 'kzinmr109@gmail.com'
__copyright__ = ''
__license__ = 'See COPYING'

import os
from setuptools import setup, find_packages

version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
with open(version_file) as fh:
    pyknp_version = fh.read().strip()
__version__ = pyknp_version

setup(
    name='pyknp-extend',
    version=pyknp_version,
    maintainer=__author__,
    maintainer_email=__email__,
    author=__author__,
    author_email=__email__,
    description='Feature extension of pyknp-0.3.',
    license=__license__,
    url='https://github.com/kzinmr/pyknp-extend',
    packages=find_packages(),
)
