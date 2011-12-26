# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import types

import sqlpuzzle.exceptions



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
    parserOptions = ParserOptions(options)
    parserInput = ParserInput(*args, **kwds)

    parser = Parser(parserOptions, parserInput)
    parser.parse()

    return parser.getOutput()



class ParserOptions(object):
    def __init__(self, options):
        self.set(options)
        self.check()

    def set(self, options):
        self.minItems = options.get('minItems', 1)
        self.maxItems = options.get('maxItems', 1)
        self.allowDict = options.get('allowDict', False)
        self.allowList = options.get('allowList', False)
        self.allowedDataTypes = options.get('allowedDataTypes', (str, unicode, int, long, float, bool))

    def check(self):
        if self.minItems > self.maxItems:
            raise sqlpuzzle.exceptions.SqlPuzzleError('maxItems must be bigger, than minItems.')

        if self.allowDict and self.maxItems <= 1:
            raise sqlpuzzle.exceptions.SqlPuzzleError('For allowDict must be maxItems bigger or equal to 2.')

        if not isinstance(self.allowedDataTypes, (tuple, list, AllowedDataTypes)):
            raise sqlpuzzle.exceptions.SqlPuzzleError('Invalid options for argsParser.')



class ParserInput(object):
    def __init__(self, *args, **kwds):
        self.__args = args
        self.__kwds = kwds

    def getArguments(self):
        return self.__args

    def getList(self):
        if self.isList():
            return self.__args[0]
        return []

    def getDictionaryOrKwds(self):
        if self.isDictionary():
            return self.__args[0]
        elif self.isKwds():
            return self.__kwds
        return {}

    def isList(self):
        return len(self.__args) == 1 and isinstance(self.__args[0], (list, tuple))

    def isDictionary(self):
        return len(self.__args) == 1 and isinstance(self.__args[0], dict)

    def isKwds(self):
        return self.__kwds != {}

    def isArgs(self):
        return len(self.__args) > 0 and not isinstance(self.__args[0], (list, tuple))

    def countOfArgsIsInInterval(self, min_, max_):
        return min_ <= len(self.__args) <= max_



class Parser(object):
    def __init__(self, options, inputData):
        self.options = options
        self.inputData = inputData
        self.outputData = []

    def getOutput(self):
        return self.outputData

    def parse(self):
        if self.inputData.isDictionary() or self.inputData.isKwds():
            if self.options.allowDict:
                self.__parseDictionary(self.inputData.getDictionaryOrKwds())
            else:
                raise sqlpuzzle.exceptions.InvalidArgumentException('Dictionary or kwds is disabled.')

        elif self.options.minItems > 1 and self.inputData.isArgs() and self.inputData.countOfArgsIsInInterval(self.options.minItems, self.options.maxItems):
            self.__parseItem(self.inputData.getArguments())

        elif self.options.allowList and self.inputData.isList():
            self.__parseList(self.inputData.getList())

        else:
            self.__parseList(self.inputData.getArguments())

    def __parseDictionary(self, dict_):
        for item in dict_.iteritems():
            self.__parseItem(item)

    def __parseList(self, list_):
        for item in list_:
            if isinstance(item, (list, tuple)):
                self.__parseItem(item)
            elif self.options.minItems == 1:
                self.__parseItem((item,))
            else:
                raise sqlpuzzle.exceptions.InvalidArgumentException('Too few arguments.')

    def __parseItem(self, item):
        batch = self.__createBatch(item)
        self.__appendBatchToOutputIfOk(batch)

    def __createBatch(self, values):
        if len(values) > self.options.maxItems:
            raise sqlpuzzle.exceptions.InvalidArgumentException('Too many arguments.')
        return self.__appendNones(tuple(values))

    def __appendNones(self, tupleWithValues):
        countOfNones = self.options.maxItems - len(tupleWithValues)
        tupleWithNones = (None,) * countOfNones
        return tupleWithValues + tupleWithNones

    def __appendBatchToOutputIfOk(self, batch):
        if self.__validateBatch(batch):
            self.outputData.append(batch)
        else:
            raise sqlpuzzle.exceptions.InvalidArgumentException()

    def __validateBatch(self, batch):
        if isinstance(self.options.allowedDataTypes, AllowedDataTypes):
            return self.options.allowedDataTypes.validateBatch(batch)
        return AllowedDataTypes()._validateBatch(batch, self.options.allowedDataTypes)



class AllowedDataTypes(object):
    def __init__(self):
        self._allowedDataTypes = []

    def add(self, *args):
        self._allowedDataTypes.append(args)
        return self

    def validateBatch(self, batch):
        for allowedDataTypes in self._allowedDataTypes:
            if self._validateBatch(batch, allowedDataTypes):
                return True
        return False

    def _validateBatch(self, batch, allowedDataTypes):
        for x, item in enumerate(batch):
            dataTypes = allowedDataTypes
            if isinstance(allowedDataTypes[0], (tuple, list)):
                dataTypes = allowedDataTypes[x]
            if item is not None and not (isinstance(item, dataTypes) or (isinstance(item, type) and issubclass(item, dataTypes))): # TODO: Temporary, class object will be disabled in version 1.0.
                return False
            # isinstance(True, (int, long)) is True => must be special condition
            if bool not in dataTypes and isinstance(item, types.BooleanType):
                return False
        return True
