# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.queries
import datetime
import re
import types


class SqlValue:
    """
    Wrap value.
    """
    
    def __init__(self, value):
        """
        Initialization of SqlValue.
        """
        self._map = {
            str: self._string,
            unicode: self._string,
            int: self._integer,
            long: self._integer,
            float: self._float,
            bool: self._boolean,
            datetime.date: self._date,
            datetime.datetime: self._datetime,
            list: self._list,
            tuple: self._list,
            sqlPuzzle.queries.select.Select: self._subselect,
            types.NoneType: self._null,
        }

        self.value = value
    
    def __str__(self):
        """
        Convert and print value.
        """
        return self._getConvertMethod()()
    
    def __repr__(self):
        return "<SqlValue: %s>" % self.__str__()
    
    def _getConvertMethod(self):
        """
        Get right method to convert of the value.
        """
        for type_, method in self._map.iteritems():
            if isinstance(self.value, type_):
                return method
        return self._undefined
    
    def _string(self):
        """
        Convert as string.
        """
        # sometime, e.g. in subselect, is needed reference to column instead of self.value
        if self.value.strip()[0] == '`':
            return self._backQuotes()
        return '"%s"' % self.value
    
    def _integer(self):
        """
        Convert as integer.
        """
        return '%d' % self.value
    
    def _float(self):
        """
        Convert as float.
        """
        return '%.5f' % self.value
    
    def _boolean(self):
        """
        Convert as boolean.
        """
        return '%d' % self.value
    
    def _date(self):
        """
        Convert as date.
        """
        return self._datetime()
    
    def _datetime(self):
        """
        Convert as datetime.
        """
        return self.value.isoformat()
    
    def _list(self):
        """
        Convert as list of values.
        """
        return "(%s)" % ", ".join(str(SqlValue(item)) for item in self.value)
    
    def _subselect(self):
        """
        Convert as subselect.
        """
        return "(%s)" % self.value
    
    def _null(self):
        """
        NULL
        """
        return 'NULL'
    
    def _undefined(self):
        """
        undefined
        """
        return 'undefined'
    
    def _backQuotes(self):
        """
        Convert as reference on column.
        "table" => "`table`"
        "table.column" => "`table`.`column`"
        "db.table.column" => "`db`.`table`.`column`"
        "table.`col.umn`" => "`table`.`col.umn`"
        "`table`.`col.umn`" => "`table`.`col.umn`"
        """
        return '.'.join('`%s`' % i if i != '*' else i for i in re.split('`([^`]+)`|\.', self.value) if i)



class SqlReference(SqlValue):
    def __init__(self, value):
        """
        Initialization of SqlReference.
        """
        self._map = {
            str: self._backQuotes,
            unicode: self._backQuotes,
            sqlPuzzle.queries.select.Select: self._subselect,
        }

        self.value = value

