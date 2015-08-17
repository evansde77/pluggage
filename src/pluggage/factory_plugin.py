#!/usr/bin/env python
"""
_factory_plugin_

Plugin base class that can be inherited to register
a class with a factory

"""
import six

from .registry import get_factory
from .registry import PluggageMeta

@six.add_metaclass(PluggageMeta)
class PluggagePlugin(object):
    """
    _PluggagePlugin_

    Inherit from this class to trigger registration
    with the pluggage.registry factory.

    Override the PLUGGAGE_FACTORY_NAME to be the
    name of the factory to register with, and
    the PLUGGAGE_OBJECT_NAME can be used to set the
    name of the plugin, if not overridden (or None)
    the name of the class will be used.

    Eg:

    SomeClass(PluggagePlugin):
        PLUGGAGE_FACTORY_NAME = 'my_factory'

    Will register the plugin as SomeClass under
    my_factory leading to instantiation patterns like:
    f = get_factory('my_factory')
    some_class_instance = f('SomeClass')

    """
    PLUGGAGE_FACTORY_NAME = 'abstract'
    PLUGGAGE_OBJECT_NAME = None

    def __init__(self):
        super(PluggagePlugin, self).__init__()
        self._factory_ref = None

    def _get_factory(self):
        """
        _get_factory_

        Helper method to get the appropriate factory
        for this plugin

        """
        if self._factory_ref is None:
            self._factory_ref = get_factory(self.PLUGGAGE_FACTORY_NAME)
        return self._factory_ref
