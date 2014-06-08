# -*- coding: utf-8 -*-
__version__ = "0.1.0"

from ConfigParser import ConfigParser
import re

entry_rx = re.compile(r"""
    (?P<alias>[^:]+)?
    (?P<value>[^!&]+)
    (
        \s*
        (?P<exclude_variable>[^&\[\]]+)
        \[(?P<exclude_glob>[^&\[\]]+)\]
        \s*
    |
        \s*
        (?P<include_variable>[^&\[\]]+)
        \[(?P<include_glob>[^&\[\]]+)\]
        \s*
    )*
""")


class Entry(object):
    def __init__(self, value):
        pass


def parse_config(filename):
    parser = ConfigParser()
    parser.read(filename)

