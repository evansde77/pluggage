#!/usr/bin/env python
"""
dynamic_factory

Simple factory/plugin loader that uses a mapping of
functions and/or instances registered to it to load
objects on the fly.

"""

from .loaders import load_plugin, load_plugin_function


class DynamicFactory(dict):
    """
    _DynamicFactory_

    """
    def __init__(self, register_functions=None, register_classes=None):
        self._functions = []
        self._classes = []

        if register_functions is not None:
            for name, plugin in register_functions.iteritems():
                self.register_function(name, plugin)

        if register_classes is not None:
            for name, plugin in register_classes.iteritems():
                self.register_class(name, plugin)

    def register_function(self, name, plugin):
        """
        _register_function_

        :param name: name under which to register function
        :param plugin: name of function to load as plugin

        """
        if name in self:
            raise RuntimeError("plugin {0} already registered".format(name))
        self._functions.append(name)
        super(DynamicFactory, self).__setitem__(name, plugin)
        return

    def register_class(self, name, plugin):
        """
        _register_function_

        """
        if name in self:
            raise RuntimeError("plugin {0} already registered".format(name))
        self._classes.append(name)
        self[name] = plugin
        return

    def __setitem__(self, key, value, plugin_type='function'):
        if plugin_type == 'function':
            self.register_function(key, value)

        elif plugin_type == 'class':
            self.register_class(key, value)
        else:
            raise RuntimeError("supported types are function, class")

    def __getitem__(self, key):
        pname = self.get(key, None)
        if pname is None:
            raise KeyError(pname)

        if pname in self._functions:
            return load_plugin_function(pname)
        if pname in self._classes:
            return load_plugin(pname)
        raise KeyError("No idea what key {0} is...".format(key))
