#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle
import sqlPuzzle.exceptions

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
    sqlPuzzle.select(True)
except sqlPuzzle.exceptions.InvalidArgumentException, e:
    print "catched:", e

try:
    print sqlPuzzle.selectFrom('t').join('t2')
except sqlPuzzle.exceptions.InvalidQueryException, e:
    print "catched:", e

try:
    sqlPuzzle.select().set(name='Alan')
except sqlPuzzle.exceptions.NotSupprotedException, e:
    print "catched:", e

try:
    print sqlPuzzle.update('table').set(name='Alan')
except sqlPuzzle.exceptions.ConfirmUpdateAllException, e:
    print "catched:", e

try:
    print sqlPuzzle.delete().from_('table')
except sqlPuzzle.exceptions.ConfirmDeleteAllException, e:
    print "catched:", e


# all exceptions is inherit from SqlPuzzleException
try:
    sqlPuzzle.select(1)
except sqlPuzzle.exceptions.SqlPuzzleException, e:
    print "catched:", e

# InvalidQueryException is inherit from InvalidArgumentException
try:
    print sqlPuzzle.selectFrom('t').join('t2')
except sqlPuzzle.exceptions.InvalidArgumentException, e:
    print "catched:", e
