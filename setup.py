#!/usr/bin/env python
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

from distutils.core import setup

from sqlpuzzle import VERSION

setup(
    name='sqlpuzzle',
    packages=[
        'sqlpuzzle',
        'sqlpuzzle/_common',
        'sqlpuzzle/_queries',
        'sqlpuzzle/_queryparts',
    ],
    version=VERSION,
    url='https://github.com/horejsek/python-sqlpuzzle',
    description='Python library for writing SQL queries.',
    author='Michal Horejsek',
    author_email='horejsekmichal@gmail.com',
    license='PSF',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ],
)
