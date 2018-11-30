import binascii
import re

__all__ = ('SqlBackend',)


class SqlBackend:
    name = 'SQL'

    reference_quote = '"'
    supports_full_join = False
    supports_on_duplicate_key_update = False
    supports_on_conflict_do_update = False
    supports_replace_into = False

    @classmethod
    def boolean(cls, value):
        return '{:d}'.format(value)

    @classmethod
    def is_reference(cls, value):
        if not isinstance(value, str):
            return False
        value = value.strip()
        return len(value) > 1 and value[0] == cls.reference_quote

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
        parts = re.split(r'{quote}([^{quote}]+){quote}|\.'.format(quote=cls.reference_quote), value)
        parts = ('{quote}{i}{quote}'.format(quote=cls.reference_quote, i=i) if i != '*' else i for i in parts if i)
        return '.'.join(parts)

    @classmethod
    def bytes(cls, value):
        return "x'{}'".format(binascii.hexlify(value).decode('ascii'))
