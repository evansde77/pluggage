#!/usr/bin/env python
"""
_maths_main_

Examples using the math plugins, including using
get factory to load the module

"""

from pluggage.registry import get_factory


if __name__ == '__main__':
    #
    # get the maths factory and tell it to load the
    # maths_plugins module.
    factory = get_factory('maths', load_modules=['maths_plugins'])

    #
    # use the factory to make some plugin objects
    #
    add = factory('Add')
    subtract = factory('Subtract')
    multiply = factory('Multiply')
    divide = factory('Divide')

    #
    # use the plugins
    #
    print(add(2, 3))
    print(subtract(8, 5))
    print(multiply(5, 5))
    print(divide(10, 2))
