#!/usr/bin/env python
"""
_factory_t_

Test using the factory with the fixtures plugin definitions
"""
import mock
import unittest

from pluggage.registry import get_factory
from pluggage.errors import FactoryError


def setUpModule():
    """
    ensure that the fixtures model is imported
    so that the plugins register
    """
    import test.fixtures.sample_plugins


class TestFactory(unittest.TestCase):
    """
    test fixture plugins access via factory
    """
    def test_getting_plugins(self):
        """
        test loading and calling the fixture plugins
        via the get_factory API
        """
        factory = get_factory('unittest')
        self.failUnless('UnittestPlugin1' in factory.registry)
        self.failUnless('UnittestPlugin2' in factory.registry)
        self.failUnless('UnittestPlugin3' in factory.registry)

        mock_1 = mock.Mock()
        mock_2 = mock.Mock()
        mock_3 = mock.Mock()

        x = factory('UnittestPlugin1')
        x(mock_1, 'abc')
        self.failUnless(mock_1.called)
        mock_1.assert_has_calls([mock.call('abc')])

        self.failUnless(
            isinstance(x._get_factory(), type(factory))
        )

        y = factory('UnittestPlugin2')
        y(mock_2, 'def')
        self.failUnless(mock_2.called)
        mock_2.assert_has_calls([mock.call('def')])

        z = factory('UnittestPlugin3')
        z(mock_3, 'ijk')
        self.failUnless(mock_3.called)
        mock_3.assert_has_calls([mock.call('ijk')])

    def test_missing_factory(self):
        """test behaviour of empty/missing factory"""
        empty_factory = get_factory('this_is_empty')
        self.failUnless(not empty_factory.registry)

        with self.assertRaises(FactoryError):
            get_factory('this_doesnt_exist', True)


if __name__ == '__main__':
    unittest.main()