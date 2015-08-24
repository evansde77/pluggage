#!/usr/bin/env python
"""
_maths_plugins_

Some toy plugin examples

"""

from pluggage.factory_plugin import PluggagePlugin


class Add(PluggagePlugin):
    PLUGGAGE_FACTORY_NAME = 'maths'

    def __call__(self, x, y):
        return x+y


class Subtract(PluggagePlugin):
    PLUGGAGE_FACTORY_NAME = 'maths'

    def __call__(self, x, y):
        return x-y


class Multiply(PluggagePlugin):
    PLUGGAGE_FACTORY_NAME = 'maths'

    def __call__(self, x, y):
        return x*y


class Divide(PluggagePlugin):
    PLUGGAGE_FACTORY_NAME = 'maths'

    def __call__(self, x, y):
        return float(x)/float(y)
