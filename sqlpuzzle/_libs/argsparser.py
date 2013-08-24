# -*- coding: utf-8 -*-

import six

import sqlpuzzle.exceptions
from sqlpuzzle._common.utils import is_sql_instance

__all__ = ('parse_args_to_list_of_tuples',)


def parse_args_to_list_of_tuples(options={}, *args, **kwds):
    """
    Parser.

    dict options {
        int min_items: Min of required items to fold one tuple. (default: 1)
        int max_items: Count of items in one tuple. Last `max_items-min_items`
            items is by default set to None. (default: 1)
        bool allow_dict: Flag allowing dictionary as first (and only one)
            argument or dictinary as **kwds. (default: False)
        bool allow_list: Flag allowing list as first (and only one) argument.
            (default: False)
        tuple allowed_data_types: Allowed data types. You can set global, e.g. (str,)
            or for each index, e.g. ((str,), (int, long), (str, unicode)).
            (default: (str, unicode, int, long, bool))
    }

    Examples:

    calling with min_items=1, max_items=2, allow_dict=False:
        arg1, arg2              => ((arg1, None), (arg2, None))
        (arg1a, arg1b), arg2    => ((arg1a, arg1b), arg2, None))
        arg1=val1               => FAIL
        {key1: val1}            => FAIL

    calling with min_items=2, max_items=3, allow_dict=True:
        arg1, arg2              => ((arg1, arg2, None),)
        arg1, arg2, arg3        => ((arg1, arg2, arg3),)
        (arg1a, arg1b, arg1c)   => ((arg1a, arg1b, arg1c),)
        arg1=val1, arg2=val2    => ((arg1, val1, None), (arg2, val2, None))
        {key1: val1, key2: val2} => ((key1, val1, None), (key2, val2, None))
        (arg1a, arg1b), arg2a, arg2b => FAIL
    """
    parser_options = ParserOptions(options)
    parser_input = ParserInput(*args, **kwds)

    parser = Parser(parser_options, parser_input)
    parser.parse()

    return parser.get_output()


class ParserOptions(object):
    def __init__(self, options):
        self.set(options)
        self.check()

    def set(self, options):
        self.min_items = options.get('min_items', 1)
        self.max_items = options.get('max_items', 1)
        self.allow_dict = options.get('allow_dict', False)
        self.allow_list = options.get('allow_list', False)
        self.allowed_data_types = options.get('allowed_data_types', ())

    def check(self):
        if self.min_items > self.max_items:
            raise sqlpuzzle.exceptions.SqlPuzzleException('max_items must be bigger, than min_items.')

        if self.allow_dict and self.max_items <= 1:
            raise sqlpuzzle.exceptions.SqlPuzzleException('For allow_dict must be max_items bigger or equal to 2.')


class ParserInput(object):
    def __init__(self, *args, **kwds):
        self.__args = args
        self.__kwds = kwds

    def get_arguments(self):
        return self.__args

    def get_list(self):
        if self.is_list():
            return self.__args[0]
        return []

    def get_dictionary_or_kwds(self):
        if self.is_dictionary():
            return self.__args[0]
        elif self.is_kwds():
            return self.__kwds
        return {}

    def is_list(self):
        return len(self.__args) == 1 and isinstance(self.__args[0], (list, tuple))

    def is_dictionary(self):
        return len(self.__args) == 1 and isinstance(self.__args[0], dict)

    def is_kwds(self):
        return self.__kwds != {}

    def is_args(self):
        return len(self.__args) > 0 and not isinstance(self.__args[0], (list, tuple))

    def count_of_args_is_in_interval(self, min_, max_):
        return min_ <= len(self.__args) <= max_


class Parser(object):
    def __init__(self, options, input_data):
        self.options = options
        self.input_data = input_data
        self.output_data = []

    def get_output(self):
        return self.output_data

    def parse(self):
        if self.input_data.is_dictionary() or self.input_data.is_kwds():
            if self.options.allow_dict:
                self.__parse_dictionary(self.input_data.get_dictionary_or_kwds())
            else:
                raise sqlpuzzle.exceptions.InvalidArgumentException(
                    'Dictionary or kwds is disabled.')

        elif self.options.min_items > 1 and self.input_data.is_args() and self.input_data.count_of_args_is_in_interval(self.options.min_items, self.options.max_items):
            self.__parse_item(self.input_data.get_arguments())

        elif self.options.allow_list and self.input_data.is_list():
            self.__parse_list(self.input_data.get_list())

        else:
            self.__parse_list(self.input_data.get_arguments())

    def __parse_dictionary(self, dict_):
        for item in six.iteritems(dict_):
            self.__parse_item(item)

    def __parse_list(self, list_):
        for item in list_:
            if isinstance(item, (list, tuple)):
                self.__parse_item(item)
            elif self.options.min_items == 1:
                self.__parse_item((item,))
            else:
                raise sqlpuzzle.exceptions.InvalidArgumentException(
                    'Too few arguments.')

    def __parse_item(self, item):
        batch = self.__create_batch(item)
        self.output_data.append(batch)

    def __create_batch(self, values):
        if len(values) > self.options.max_items:
            raise sqlpuzzle.exceptions.InvalidArgumentException(
                'Too many arguments.')
        return self.__append_nones(tuple(values))

    def __append_nones(self, tuple_with_values):
        count_of_nones = self.options.max_items - len(tuple_with_values)
        tuple_with_nones = (None,) * count_of_nones
        return tuple_with_values + tuple_with_nones
