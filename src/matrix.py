# -*- coding: utf-8 -*-
__version__ = "0.5.0"

import re
from collections import OrderedDict
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
from fnmatch import fnmatch
from itertools import product
import warnings

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


entry_rx = re.compile(r"""
    ^
    ((?P<merge>\?))?
    ((?P<alias>[^\?:]*):)?
    \s*(?P<value>[^!&]+?)\s*
    (?P<reducers>[!&].+)?
    $
""", re.VERBOSE)
reducer_rx = re.compile(r"""
    \s*
    (?P<type>[!&])
    (?P<variable>[^!&\[\]]+)
    \[(?P<glob>[^\[\]]+)\]
    \s*
""", re.VERBOSE)

special_chars_rx = re.compile(r'[\\/:>?|\[\]< ]+')


class ParseError(Exception):
    pass


class DuplicateEntry(UserWarning):
    def __str__(self):
        return "Duplicate entry %r (from %r). Conflicts with %r - it has the same alias." % self.args
    __repr__ = __str__


class DuplicateEnvironment(Exception):
    def __str__(self):
        return "Duplicate environment %r. It has conflicting sets of data: %r != %r." % self.args
    __repr__ = __str__


class Reducer(object):
    def __init__(self, entry):
        kind, variable, pattern = entry
        assert kind in "&!"
        self.kind = kind
        self.is_exclude = kind == '!'
        self.variable = variable
        self.pattern = pattern

    def __str__(self):
        return "%s(%s[%s])" % (
            "exclude" if self.is_exclude else "include",
            self.variable,
            self.pattern,
        )
    __repr__ = __str__


class Entry(object):
    def __init__(self, value):
        value = value.strip()
        if not value or value == '-':
            self.alias = ''
            self.value = ''
            self.merge = False
            self.reducers = []
        else:
            m = entry_rx.match(value)
            if not m:
                raise ValueError("Failed to parse %r" % value)
            m = m.groupdict()
            self.alias = m['alias']
            self.value = m['value']
            self.merge = m['merge']
            self.reducers = [Reducer(i) for i in reducer_rx.findall(m['reducers'] or '')]

        if self.alias is None:
            self.alias = special_chars_rx.sub('_', self.value)

    def __eq__(self, other):
        return self.alias == other.alias

    def __str__(self):
        return "Entry(%r, %salias=%r)" % (
            self.value,
            ', '.join(str(i) for i in self.reducers) + ', ' if self.reducers else '',
            self.alias,
        )
    __repr__ = __str__


def parse_config(fp):
    parser = ConfigParser()
    parser.readfp(fp)
    config = OrderedDict()
    for name, value in parser.items('matrix'):
        entries = config[name] = []
        for line in value.strip().splitlines():
            entry = Entry(line)
            duplicates = [i for i in entries if i == entry]
            if duplicates:
                warnings.warn(DuplicateEntry(entry, line, duplicates), DuplicateEntry, 1)
            entries.append(entry)
    return config


def from_config(config):
    """
    Generate a matrix from a configuration dictionary.
    """
    matrix = {}
    variables = config.keys()
    for entries in product(*config.values()):
        combination = dict(zip(variables, entries))
        include = True
        for value in combination.values():
            for reducer in value.reducers:
                match = fnmatch(combination[reducer.variable].value, reducer.pattern)
                if match if reducer.is_exclude else not match:
                    include = False
        if include:
            key = '-'.join(entry.alias for entry in entries if entry.alias)
            data = dict(
                zip(variables, (entry.value for entry in entries))
            )
            if key in matrix and data != matrix[key]:
                raise DuplicateEnvironment(key, data, matrix[key])
            matrix[key] = data
    return matrix


def from_file(filename):
    """
    Generate a matrix from a .ini file. Configuration is expected to be in a ``[matrix]`` section.
    """
    config = parse_config(open(filename))
    return from_config(config)


def from_string(string):
    """
    Generate a matrix from a .ini file. Configuration is expected to be in a ``[matrix]`` section.
    """
    config = parse_config(StringIO(string))
    return from_config(config)
