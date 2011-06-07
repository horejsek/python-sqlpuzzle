# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.exceptions


def parseArgsToListOfTuples(options={}, *args, **kwds):
    """
    Parser.
    
    dict options {
        int minItems: Min of required items to fold one tuple. (default: 1)
        int maxItems: Count of items in one tuple. Last `maxItems-minItems`
            items is by default set to None. (default: 1)
        bool allowDict: Flag allowing dictionary as first (and only one)
            argument or dictinary as **kwds. (default: False)
        bool allowList: Flag allowing list as first (and only one) argument.
            (default: False)
        tuple allowedDataTypes: Allowed data types. You can set global, e.g. (str,)
            or for each index, e.g. ((str,), (int, long), (str, unicode)).
            (default: (str, unicode, int, long, bool))
    }
    
    Examples:
    
    calling with minItems=1, maxItems=2, allowDict=False:
        arg1, arg2              => ((arg1, None), (arg2, None))
        (arg1a, arg1b), arg2    => ((arg1a, arg1b), arg2, None))
        arg1=val1               => FAIL
        {key1: val1}            => FAIL
    
    calling with minItems=2, maxItems=3, allowDict=True:
        arg1, arg2              => ((arg1, arg2, None),)
        arg1, arg2, arg3        => ((arg1, arg2, arg3),)
        (arg1a, arg1b, arg1c)   => ((arg1a, arg1b, arg1c),)
        arg1=val1, arg2=val2    => ((arg1, val1, None), (arg2, val2, None))
        {key1: val1, key2: val2} => ((key1, val1, None), (key2, val2, None))
        (arg1a, arg1b), arg2a, arg2b => FAIL
    """
    minItems = options.get('minItems', 1)
    maxItems = options.get('maxItems', 1)
    allowDict = options.get('allowDict', False)
    allowList = options.get('allowList', False)
    allowedDataTypes = options.get('allowedDataTypes', (str, unicode, int, long, bool))
    
    result = []
    
    if minItems > maxItems:
        raise sqlPuzzle.exceptions.SqlPuzzleError('maxItems must be bigger, than minItems.')
    
    if allowDict and maxItems <= 1:
        raise sqlPuzzle.exceptions.SqlPuzzleError('For allowDict must be maxItems bigger or equal to 2.')

    if allowDict:
        dict_ = {}
        if args and isinstance(args[0], dict):
            if len(args) == 1:
                dict_ = args[0]
            else:
                raise sqlPuzzle.exceptions.InvalidArgumentException('Dictionary must be as only one argument.')
        elif kwds != {}:
            dict_ = kwds
        
        for arg in dict_.iteritems():
            values = __createTuple(arg, maxItems)
            __appendIfOk(result, values, allowedDataTypes)
    else:
        if (len(args) == 1 and isinstance(args[0], dict)) or kwds != {}:
            raise sqlPuzzle.exceptions.InvalidArgumentException('Dictionary or kwds is disabled.')
    
    if not result:
        if minItems > 1 and minItems <= len(args) <= maxItems and not isinstance(args[0], (list, tuple)):
            values = __createTuple(args, maxItems)
            __appendIfOk(result, values, allowedDataTypes)
    
    if not result:
        list_ = args
        if allowList and len(args) == 1 and isinstance(args[0], (list, tuple)):
            list_ = args[0]
        
        for arg in list_:
            if isinstance(arg, (list, tuple)):
                values = __createTuple(arg, maxItems)
            elif minItems == 1:
                values = __createTuple((arg,), maxItems)
            else:
                raise sqlPuzzle.exceptions.InvalidArgumentException('Too few arguments.')
            __appendIfOk(result, values, allowedDataTypes)

    return result



def __createTuple(values, length):
    """
    From list/tuple create tuple with `length` items. Default value is None.
    If is in list_ more items, than say length => raise.
    """
    if len(values) > length:
        raise sqlPuzzle.exceptions.InvalidArgumentException('Too many arguments.')
    return tuple(values) + (None,)*(length-len(values))



def __appendIfOk(data, values, allowedDataTypes):
    """
    Append tuple into result, if tuple is ok.
    """
    if __validate(values, allowedDataTypes):
        data.append(values)
    else:
        raise sqlPuzzle.exceptions.InvalidArgumentException()


def __validate(values, allowedDataTypes):
    """
    Validate tuple on data types.
    """
    if not isinstance(allowedDataTypes, (tuple, list)):
        raise sqlPuzzle.exceptions.SqlPuzzleError('Invalid options for argsParser.')
    
    for x, item in enumerate(values):
        dataTypes = allowedDataTypes
        if isinstance(allowedDataTypes[0], (tuple, list)):
            dataTypes = allowedDataTypes[x]
        if item is not None and not isinstance(item, dataTypes):
            return False
    return True


