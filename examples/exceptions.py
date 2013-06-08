#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlpuzzle
import sqlpuzzle.exceptions

#
# inheritance of SqlPuzzleException:
#
# SqlPuzzleException
# - SqlPuzzleError (internal error)
# - SqlNotImplemented
# - ConfirmException
# - - ConfirmUpdateAllException
# - - ConfirmDeleteAllException
# - InvalidArgumentException
# - - InvalidQueryException
# - NotSupprotedException
#

try:
    sqlpuzzle.select(True)
except sqlpuzzle.exceptions.InvalidArgumentException, e:
    print "catched:", e

try:
    print sqlpuzzle.select_from('t').join('t2')
except sqlpuzzle.exceptions.InvalidQueryException, e:
    print "catched:", e

try:
    sqlpuzzle.select()._values
except sqlpuzzle.exceptions.NotSupprotedException, e:
    print "catched:", e

try:
    print sqlpuzzle.update('table').set(name='Alan')
except sqlpuzzle.exceptions.ConfirmUpdateAllException, e:
    print "catched:", e

try:
    print sqlpuzzle.delete().from_('table')
except sqlpuzzle.exceptions.ConfirmDeleteAllException, e:
    print "catched:", e


# all exceptions is inherit from SqlPuzzleException
try:
    sqlpuzzle.select(1)
except sqlpuzzle.exceptions.SqlPuzzleException, e:
    print "catched:", e

# InvalidQueryException is inherit from InvalidArgumentException
try:
    print sqlpuzzle.select_from('t').join('t2')
except sqlpuzzle.exceptions.InvalidArgumentException, e:
    print "catched:", e
