#!/usr/bin/env python
"""
_errors_t_

unittests for errors module

"""
import unittest


from pluggage.errors import PluggageError, LoaderError


class ErrorsTests(unittest.TestCase):
    """
    test coverage for error classes

    """
    def test_loader_error(self):
        """test attributes etc of loader error"""
        msg = "failed to load X"
        error = LoaderError(msg, plugin="womp")
        self.assertEqual(error.message, msg)
        self.failUnless(isinstance(error, PluggageError))
        self.assertEqual(error.plugin, "womp")


if __name__ == '__main__':
    unittest.main()
