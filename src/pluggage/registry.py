#!/usr/bin/env python
"""
_registry_

Plugin class registry utils

"""
import pkg_resources
import importlib

from .errors import FactoryError


class Registry(object):
    """
    _Registry_

    Plugin registry. Wrapper for a plugin registry.
    Instantiate with the name of the factory and then use
    it to access plugins registered with that factory.

    The __call__ operator will instantiate a named plugin
    passing optional args/kwargs to the named plugin class

    """
    # singleton registry of factory name: plugin name:cls mapping
    _REGISTRY = {}

    def __init__(self, factory_name):
        self.factory_name = factory_name
        self.registry = self._REGISTRY.setdefault(factory_name, {})

    def register(self, obj_name, cls):
        if obj_name in self.registry:
            msg = (
                "Duplicate Plugin registered for {} "
                "register: {}, existing {}"
            ).format(
                obj_name,
                cls.__name__,
                self.registry[obj_name].__name__
            )
            raise FactoryError(
                msg, factory=self.factory_name, plugin=obj_name
            )
        self.registry[obj_name] = cls

    def get(self, plugin, default=None):
        """
        get with default access to test if plugins are
        registered or just get access to the class object

        :param plugin: Name of the plugin
        :param default: optional, thing to return if
           not present
        """
        return self.registry.get(plugin, default)

    def __call__(self, plugin, *args, **kwargs):
        cls = self.get(plugin)
        if cls is None:
            msg = (
                "No plugin registered with {} for name {}"
            ).format(self.factory_name, plugin)
            raise FactoryError(
                msg, factory=self.factory_name,  plugin=plugin
            )
        return cls(*args, **kwargs)


def get_factory(factory_name, throw_on_nonexist=False, load_modules=None):
    """
    get an instance of the Registry object for the named
    factory. Note that this will create a new
    empty entry in the registry for factory name if it
    doesnt exist, unless the throw_on_nonexist is True

    :param factory_name: Name of the factory to get plugins for
    :param throw_on_nonexist: If no plugins exist for the factory,
        raise an exception
    :param load_modules: List of module names to import to trigger
        plugin registration

    :returns: Instance of Registry set up to use the given factory
        name
    """
    if load_modules is not None:
        for module_name in load_modules:
            importlib.import_module(module_name)

    if (factory_name not in Registry._REGISTRY) and throw_on_nonexist:
        msg = "Factory name {} not found in registry".format(factory_name)
        raise FactoryError(msg, factory=factory_name)
    return Registry(factory_name)


def init_factory(factory_name, throw_on_nonexist=False, load_modules=None):
    """
    Similar to get_factory but uses the pluggage_modules
    entry points to load plugin modules registered by other packages.
    Call this from a main routine to initialise a factory
    with pluggage modules entry points defined in setuptools

    Arguments are same as for get_factory

    :returns: Instance of Registry set up to use the given factory
        name

    """
    for entry_point in pkg_resources.iter_entry_points(group='pluggage_modules'):
        entry_point.load()
    return get_factory(factory_name, throw_on_nonexist=False, load_modules=None)


class PluggageMeta(type):
    """
    metaclass for Pluggage derived objects that register the
    objects with the appropriate registry/factory object
    """
    def __init__(cls, name, bases, dct):
        factory = get_factory(cls.PLUGGAGE_FACTORY_NAME)
        object_name = cls.PLUGGAGE_OBJECT_NAME
        if object_name is None:
            object_name = cls.__name__
        factory.register(object_name, cls)
        super(PluggageMeta, cls).__init__(name, bases, dct)
