# -*- coding: utf-8 -*-

import six

from sqlpuzzle._common import Object

__all__ = ('SelectOptions',)


class SelectOptions(Object):
    _options = {
        'sql_cache': {
            'off': '',
            'cache': 'SQL_CACHE',
            'noCache': 'SQL_NO_CACHE'
        },
        'duplicated': {
            'off': '',
            'all': 'ALL',
            'distinct': 'DISTINCT',
            'distinctrow': 'DISTINCTROW',
        },
        'sql_small_result': {
            'off': '',
            'on': 'SQL_SMALL_RESULT',
        },
        'sql_big_result': {
            'off': '',
            'on': 'SQL_BIG_RESULT',
        },
        'sql_buffer_result': {
            'off': '',
            'on': 'SQL_BUFFER_RESULT',
        },
        'sql_calc_found_rows': {
            'off': '',
            'on': 'SQL_CALC_FOUND_ROWS',
        },
        'straight_join': {
            'off': '',
            'on': 'STRAIGHT_JOIN',
        },
        'high_priority': {
            'off': '',
            'on': 'HIGH_PRIORITY',
        },
    }

    def __init__(self):
        super(SelectOptions, self).__init__()
        self._set_options = {}
        for option_key in self._options.keys():
            self._set_options[option_key] = 'off'

    def __unicode__(self):
        return ' '.join(self._options[key][val] for key, val in six.iteritems(self._set_options) if val != 'off')

    def __eq__(self, other):
        if type(self) != type(other) or len(self._set_options) != len(other._set_options):
            return False
        return all(bool(so == oo) for so, oo in zip(self._set_options.values(), other._set_options.values()))

    def is_set(self):
        return str(self) != ''

    def sql_cache(self):
        self._set_options['sql_cache'] = 'cache'

    def sql_no_cache(self):
        self._set_options['sql_cache'] = 'noCache'

    def all(self):
        self._set_options['duplicated'] = 'all'

    def distinct(self):
        self._set_options['duplicated'] = 'distinct'

    def distinctrow(self):
        self._set_options['duplicated'] = 'distinctrow'

    def sql_small_result(self, allow=True):
        self._set_options['sql_small_result'] = 'on' if allow else 'off'

    def sql_big_result(self, allow=True):
        self._set_options['sql_big_result'] = 'on' if allow else 'off'

    def sql_buffer_result(self, allow=True):
        self._set_options['sql_buffer_result'] = 'on' if allow else 'off'

    def sql_calc_found_rows(self, allow=True):
        self._set_options['sql_calc_found_rows'] = 'on' if allow else 'off'

    def straight_join(self, allow=True):
        self._set_options['straight_join'] = 'on' if allow else 'off'

    def high_priority(self, allow=True):
        self._set_options['high_priority'] = 'on' if allow else 'off'


class SelectForUpdate(Object):
    def __init__(self, ):
        super(SelectForUpdate, self).__init__()
        self._for_update = False

    def __unicode__(self):
        if self._for_update:
            return 'FOR UPDATE'
        return ''

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self._for_update == other._for_update
        )

    def is_set(self):
        return self._for_update

    def for_update(self, allow=True):
        self._for_update = bool(allow)
