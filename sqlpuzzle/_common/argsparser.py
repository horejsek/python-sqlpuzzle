# -*- coding: utf-8 -*-

import six

from sqlpuzzle.exceptions import InvalidArgumentException

__all__ = ('parse_args',)


def parse_args(options={}, *args, **kwds):
    """
    Parser of arguments.

    dict options {
        int min_items: Min of required items to fold one tuple. (default: 1)
        int max_items: Count of items in one tuple. Last `max_items-min_items`
            items is by default set to None. (default: 1)
        bool allow_dict: Flag allowing dictionary as first (and only one)
            argument or dictinary as **kwds. (default: False)
        bool allow_list: Flag allowing list as first (and only one) argument.
            (default: False)
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
    parser_input = ParserInput(args, kwds)

    parser = Parser(parser_options, parser_input)
    parser.parse()
    return parser.output_data


class ParserOptions(object):
    def __init__(self, options):
        self.min_items = options.get('min_items', 1)
        self.max_items = options.get('max_items', 1)
        self.allow_dict = options.get('allow_dict', False)
        self.allow_list = options.get('allow_list', False)

        assert self.min_items <= self.max_items
        assert not self.allow_dict or (self.allow_dict and self.max_items > 1)


class ParserInput(object):
    def __init__(self, args, kwds):
        self.args = args
        self.kwds = kwds

    @property
    def list(self):
        if self.is_list:
            return self.args[0]
        return []

    @property
    def dictionary_or_kwds(self):
        if self.is_dictionary:
            return self.args[0]
        elif self.is_kwds:
            return self.kwds
        return {}

    @property
    def is_list(self):
        return len(self.args) == 1 and isinstance(self.args[0], (list, tuple))

    @property
    def is_dictionary(self):
        return len(self.args) == 1 and isinstance(self.args[0], dict)

    @property
    def is_kwds(self):
        return self.kwds != {}

    @property
    def is_args(self):
        return len(self.args) > 0 and not isinstance(self.args[0], (list, tuple))

    def count_of_args_is_in_interval(self, min_, max_):
        return min_ <= len(self.args) <= max_


class Parser(object):
    def __init__(self, options, input_data):
        self.options = options
        self.input_data = input_data
        self.output_data = []

    def parse(self):
        if (
                self.options.min_items > 1
                and self.input_data.is_args
                and self.input_data.count_of_args_is_in_interval(self.options.min_items, self.options.max_items)
        ):
            self._parse_item(self.input_data.args)

        elif self.options.allow_list and self.input_data.is_list:
            self._parse_list(self.input_data.list)

        elif not self.input_data.is_dictionary and self.input_data.args:
            self._parse_list(self.input_data.args)

        if self.input_data.is_dictionary or self.input_data.is_kwds:
            if not self.options.allow_dict:
                raise InvalidArgumentException('Dictionary or kwds is disabled.')
            self._parse_dictionary(self.input_data.dictionary_or_kwds)

    def _parse_dictionary(self, dictionary):
        for item in sorted(six.iteritems(dictionary)):
            self._parse_item(item)

    def _parse_list(self, list_):
        for item in list_:
            if isinstance(item, (list, tuple)):
                self._parse_item(item)
            elif self.options.min_items == 1:
                self._parse_item((item,))
            else:
                raise InvalidArgumentException('Too few arguments.')

    def _parse_item(self, item):
        batch = self._create_batch(item)
        self.output_data.append(batch)

    def _create_batch(self, values):
        if len(values) > self.options.max_items:
            raise InvalidArgumentException('Too many arguments.')
        return self._append_nones(tuple(values))

    def _append_nones(self, tuple_with_values):
        count_of_nones = self.options.max_items - len(tuple_with_values)
        tuple_with_nones = (None,) * count_of_nones
        return tuple_with_values + tuple_with_nones
