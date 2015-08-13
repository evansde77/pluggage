#!/usr/bin/env python
"""
_loaders_t_

unittest coverage for pluggae.loaders module

Note: requires that test/fixtures is on pythonpath

"""
import types
import unittest

from pluggage.errors import LoaderError
from pluggage.loaders import (
    parse_module_class_name,
    load_object,
    load_plugin
)


class LoadersTest(unittest.TestCase):
    """
    tests for loaders module functions

    """
    def test_parse_module_dot_class(self):
        """
        tests for module name parser
        """
        name_1 = "module.submodule.Class"
        name_2 = "module.Class"
        name_3 = "module.submodule.subsubmodule.Class"

        self.assertEqual(
            parse_module_class_name(name_1),
            ['module.submodule', 'Class']
        )
        self.assertEqual(
            parse_module_class_name(name_2),
            ['module', 'Class']
        )
        self.assertEqual(
            parse_module_class_name(name_3),
            ['module.submodule.subsubmodule', 'Class']
        )

        # error cases
        with self.assertRaises(LoaderError) as ecm:
            parse_module_class_name("no_period_character")
        ex = ecm.exception
        self.assertEqual(ex.plugin, "no_period_character")

        with self.assertRaises(LoaderError) as ecm:
            parse_module_class_name({"not": "a string"})
        ex = ecm.exception
        self.failUnless(ex.message.startswith("Plugin name is not a string"))

    def test_load_object(self):
        """test calls to load_object function"""
        # succesful loads
        func_obj = load_object('test.fixtures.loader_fixtures.some_function')
        self.failUnless(isinstance(func_obj, types.FunctionType))
        cls_obj = load_object('test.fixtures.loader_fixtures.SomeClass')
        self.failUnless(isinstance(cls_obj, types.TypeType))
        l_obj = load_object('test.fixtures.loader_fixtures.some_lambda')
        self.failUnless(isinstance(l_obj, types.LambdaType))
        cls_obj2 = load_object('test.fixtures.loader_fixtures.TheConfuser')
        self.failUnless(isinstance(cls_obj2, types.TypeType))

        # failures
        # bad module
        self.assertRaises(LoaderError, load_object, 'herp.derp.womp.some_function')
        # good module, bad object
        self.assertRaises(LoaderError, load_object, 'test.fixtures.loader_fixtures.herp_derp_womp')

    def test_load_plugin(self):
        """test calls to load_plugin"""

        cls_obj = load_plugin(
            'test.fixtures.loader_fixtures.SomeClass'
        )
        self.failUnless(isinstance(cls_obj, types.TypeType))

        load_plugin(
            'test.fixtures.loader_fixtures.SomeClass',
            type_check=(object,)
            )
        class BadSubclass(object):
            pass

        with self.assertRaises(LoaderError) as ecm:
            load_plugin(
                'test.fixtures.loader_fixtures.SomeClass',
                type_check=BadSubclass
                )
        self.failUnless('BadSubclass' in ecm.exception.message)


if __name__ == '__main__':
    unittest.main()
