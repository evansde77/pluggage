#!/usr/bin/env python
"""
plugins

Simple factory/plugin loader that implements a dictionary
interface around a set of plugins and
imports/loads them on the fly via the dictionary key access
API

"""

from .loaders import load_object


class Plugins(dict):
    """
    _Plugins_

    Dictionary based object that provides simple
    object loading on get/getitem and a couple
    of helpers to instantiate or call plugins

    """
    def __init__(self, **plugins):
        self.update(plugins)

    def __getitem__(self, key):
        pname = super(Plugins, self).__getitem__(self, key)
        obj_ref = load_object(pname)
        return obj_ref

    def get(self, key, default=None):
        if key not in self:
            return default
        return self[key]

    def __call__(self, name, *args, **kwargs):
        """
        _call_

        Get the named plugin and return the results of
        calling it with args/kwargs passed through to it.

        """
        plugin = self[name]
        if not callable(plugin):
            raise RuntimeError(
                "Plugin {0} from {1} is not callable".format(
                    name, super(Plugins, self).get(name)
                )
            )

        return plugin(*args, **kwargs)
