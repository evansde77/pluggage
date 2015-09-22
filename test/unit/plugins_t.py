#!/usr/bin/env python
"""
unittests for pluggage.plugins module
"""

import unittest
import types
from pluggage.plugins import Plugins


class PluginsTest(unittest.TestCase):
    """
    test lightweight plugin helper
    """
    def test_loading_known_refs(self):
        """test loading fixtures works as expected"""
        loader = Plugins()
        func = loader['test.fixtures.loader_fixtures.some_function']
        self.failUnless(isinstance(func, types.FunctionType))
        self.assertEqual(func.__name__, 'some_function')
        obj = loader['test.fixtures.loader_fixtures.SomeClass']
        self.assertEqual(obj.__name__, 'SomeClass')

        self.failUnless(
            'test.fixtures.loader_fixtures.some_function' in loader
        )
        self.failUnless(
            'test.fixtures.loader_fixtures.SomeClass' in loader
        )

        obj2 = loader.get('test.fixtures.loader_fixtures.SomeClass')
        self.assertEqual(obj, obj2)

        inst = loader('test.fixtures.loader_fixtures.SomeClass')
        self.failUnless(isinstance(inst, obj2))

    def test_loading_unknown_plugins(self):
        """test loading missing plugins fails as expected"""
        loader = Plugins()
        self.assertRaises(
            KeyError, loader.__getitem__, 'derp.womp.hork'
        )
        self.assertEqual(
            loader.get('derp.womp.hork', "default"),
            "default"
            )

if __name__ == '__main__':
    unittest.main()
