#!/usr/bin/env python
"""
_errors_t_

unittests for errors module

"""
import unittest


from pluggage.errors import PluggageError, LoaderError, FactoryError


class ErrorsTests(unittest.TestCase):
    """
    test coverage for error classes

    """
    def test_loader_error(self):
        """test attributes etc of loader error"""
        msg = "failed to load X"
        error = LoaderError(msg, plugin="womp")
        self.assertEqual(str(error), msg)
        self.failUnless(isinstance(error, PluggageError))
        self.assertEqual(error.plugin, "womp")

    def test_factory_error(self):
        """test attributes of factory error"""
        msg = "failed to load X from factory Y"
        error = FactoryError(msg, factory="Y", plugin="X")
        self.assertEqual(str(error), msg)
        self.failUnless(isinstance(error, PluggageError))
        self.assertEqual(error.plugin, "X")
        self.assertEqual(error.factory, "Y")


if __name__ == '__main__':
    unittest.main()
