#!/usr/bin/env python
"""
_loaders_t_

unittest coverage for pluggae.loaders module

Note: requires that test/fixtures is on pythonpath

"""
import unittest

from pluggage.errors import LoaderError
from pluggage.loaders import (
    parse_module_class_name,
    load_object
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
        """test calls to load_object method"""
        load_object('test.fixtures.loader_fixtures.some_function')
        load_object('test.fixtures.loader_fixtures.SomeClass')

if __name__ == '__main__':
    unittest.main()
