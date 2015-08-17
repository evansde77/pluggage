#!/usr/bin/env python
"""
sample factory plugins used by unittests

"""
from pluggage.factory_plugin import PluggagePlugin


class UnittestPlugin1(PluggagePlugin):
    """
    plugin 1
    """
    PLUGGAGE_FACTORY_NAME = 'unittest'
    PLUGGAGE_OBJECT_NAME = 'UnittestPlugin1'

    def __call__(self, call_this, value):
        call_this(value)


class UnittestPlugin2(PluggagePlugin):
    PLUGGAGE_FACTORY_NAME = 'unittest'
    PLUGGAGE_OBJECT_NAME = 'UnittestPlugin2'

    def __call__(self, call_this, value):
        call_this(value)


class UnittestPlugin3(PluggagePlugin):
    PLUGGAGE_FACTORY_NAME = 'unittest'

    def __call__(self, call_this, value):
        call_this(value)
