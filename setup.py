#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from pip.req import parse_requirements

from sqlpuzzle import VERSION

setup(
    name='sqlpuzzle',
    version=VERSION,
    packages=[
        'sqlpuzzle',
        'sqlpuzzle/_backends',
        'sqlpuzzle/_common',
        'sqlpuzzle/_queries',
        'sqlpuzzle/_queryparts',
    ],

    install_requires=[str(ir.req) for ir in parse_requirements('requirements.txt')],

    url='https://github.com/horejsek/python-sqlpuzzle',
    author='Michal Horejsek',
    author_email='horejsekmichal@gmail.com',
    description='Python library for writing SQL queries.',
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
