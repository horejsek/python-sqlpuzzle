# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.queries.query
import sqlPuzzle.queries.delete
import sqlPuzzle.queries.insert
import sqlPuzzle.queries.select
import sqlPuzzle.queries.update


class SqlPuzzle:
    def __init__(self):
        """
        Initialization of SqlPuzzle.
        """
        self.__query = sqlPuzzle.queries.query.Query()
    
    # SELECT
    
    def select(self, *columns):
        """
        Set column(s) to select.
        """
        self.__query = sqlPuzzle.queries.select.Select(*columns)
        return self
    
    def columns(self, *columns):
        """
        Set column(s) to select.
        """
        self.__query.columns(*columns)
        return self
    
    def limit(self, limit, offset=None):
        """
        Set limit (and offset).
        """
        self.__query.limit(limit, offset)
        return self
    
    def offset(self, offset):
        """
        Set offset.
        """
        self.__query.offset(offset)
        return self
    
    # INSERT
    
    def insert(self):
        """
        Set query to insert.
        """
        self.__query = sqlPuzzle.queries.insert.Insert()
        return self
    
    def into(self, table):
        """
        Set table for insert.
        """
        self.__query.into(table)
        return self
    
    def insertInto(self, table):
        """
        Set query to insert.
        """
        return self.insert().into(table)
    
    def values(self, *args, **kwargs):
        """
        Set columns and values.
        """
        self.__query.values(*args, **kwargs)
        return self
    
    # UPDATE
    
    def update(self, table):
        """
        Set table for update.
        """
        self.__query = sqlPuzzle.queries.update.Update(table)
        return self
    
    def set(self, *args, **kwargs):
        """
        Set columns and values.
        """
        self.__query.set(*args, **kwargs)
        return self
    
    # DELETE
    
    def delete(self):
        """
        Set query to delete.
        """
        self.__query = sqlPuzzle.queries.delete.Delete()
        return self
    
    def deleteFrom(self, table):
        """
        Set query to delete.
        """
        return self.delete().from_(table)
    
    # GLOBAL
    
    def from_(self, *tables):
        """
        Set table(s) to query.
        """
        self.__query.from_(*tables)
        return self
    
    def where(self, *args, **kwargs):
        """
        Set condition(s) to query.
        """
        self.__query.where(*args, **kwargs)
        return self
    
    def removeWhere(self, *keys):
        """
        Remove conditions by keys (name of columns).
        """
        self.__query.removeWhere(*keys)
        return self
    
    # PRINT
    
    def __str__(self):
        """
        Print query.
        """
        return str(self.__query)
    
    def getQuery(self):
        """
        Print query.
        """
        return self.__str__()
    
    # ALLOW
    
    def allowUpdateAll(self): self.query.allowUpdateAll()
    def forbidUpdateAll(self): self.query.forbidUpdateAll()
    
    def allowDeleteAll(self): self.query.allowDeleteAll()
    def forbidDeleteAll(self): self.query.forbidDeleteAll()

