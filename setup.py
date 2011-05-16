#!/usr/bin/env python

from distutils.core import setup

version = '0.1b'

setup(
    name = 'sqlPuzzle',
    packages = ['sqlPuzzle'],
    version = version,
    url = 'https://github.com/horejsek/sqlPuzzle',
    description = 'Python module.',
    author = 'Michal Horejsek',
    author_email = 'horejsekmichal@gmail.com',
    license = 'GNU General Public License (GPL)',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ],
)
