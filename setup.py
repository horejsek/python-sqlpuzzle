#!/usr/bin/env python
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#
# This application is released under the GNU General Public License
# v3 (or, at your option, any later version). You can find the full
# text of the license under http://www.gnu.org/licenses/gpl.txt.
# By using, editing and/or distributing this software you agree to
# the terms and conditions of this license.
# Thank you for using free software!
#

from distutils.core import setup

from sqlpuzzle import version

setup(
    name='sqlpuzzle',
    packages=[
        'sqlpuzzle',
        'sqlpuzzle/_features',
        'sqlpuzzle/_queries',
        'sqlpuzzle/_libs',
    ],
    version=version,
    url='https://github.com/horejsek/python-sqlpuzzle',
    description='Python library for writing SQL queries.',
    author='Michal Horejsek',
    author_email='horejsekmichal@gmail.com',
    license='GNU General Public License (GPL)',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ],
)
