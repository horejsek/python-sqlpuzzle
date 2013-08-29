#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlpuzzle
import sqlpuzzle.exceptions

#
# Inheritance of SqlPuzzleException:
#
# SqlPuzzleException
# - ConfirmException
# - - ConfirmUpdateAllException
# - - ConfirmDeleteAllException
# - InvalidArgumentException
# - - InvalidQueryException
#

try:
    sqlpuzzle.select(True)
except sqlpuzzle.exceptions.InvalidArgumentException, e:
    print('catched:', e)

try:
    print(sqlpuzzle.select_from('t').on('t2'))
except sqlpuzzle.exceptions.InvalidQueryException, e:
    print('catched:', e)

try:
    print(sqlpuzzle.update('table').set(name='Alan'))
except sqlpuzzle.exceptions.ConfirmUpdateAllException, e:
    print('catched:', e)

try:
    print(sqlpuzzle.delete().from_('table'))
except sqlpuzzle.exceptions.ConfirmDeleteAllException, e:
    print('catched:', e)


# All exceptions are inherited from SqlPuzzleException.
try:
    sqlpuzzle.select(1)
except sqlpuzzle.exceptions.SqlPuzzleException, e:
    print('catched:', e)
