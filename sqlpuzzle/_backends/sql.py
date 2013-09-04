# -*- coding: utf-8 -*-

import six

import re

__all__ = ('SqlBackend',)


class SqlBackend(object):
    _reference_quote = '"'

    @classmethod
    def boolean(cls, value):
        return six.u('%d') % value

    @classmethod
    def is_reference(cls, value):
        if not isinstance(value, six.string_types):
            return False
        value = value.strip()
        return value and value[0] == cls._reference_quote

    @classmethod
    def reference(cls, value):
        """
        Convert as reference on column.
        table => "table"
        table.column => "table"."column"
        db.table.column => "db"."table"."column"
        table."col.umn" => "table"."col.umn"
        "table"."col.umn" => "table"."col.umn"
        """
        from sqlpuzzle._common.utils import force_text
        value = force_text(value)
        parts = re.split('%(quote)s([^%(quote)s]+)%(quote)s|\.' % {'quote': cls._reference_quote}, value)
        parts = (six.u('%(quote)s%(i)s%(quote)s') % {'quote': cls._reference_quote, 'i': i} if i != '*' else i for i in parts if i)
        return six.u('.').join(parts)
