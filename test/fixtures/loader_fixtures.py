#!/usr/bin/env python
"""
fixture utils/targets for tests

"""

some_lambda = lambda x: x


def some_function(a):
    print(a)


class SomeClass(object):
    pass


class TheConfuser(object):
    def __call__(self, x):
        print(x)
