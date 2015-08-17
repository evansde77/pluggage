#!/usr/bin/env python
"""
loaders

Util methods to load things on the fly, optionally type checking them
if needed.

"""

import importlib
from .errors import LoaderError


def parse_module_class_name(module_dot_class):
    """
    _parse_module_class_name_

    parse a string of the form module.submodule.Class

    :param module_dot_class: String containing module.Class style ref

    :returns: the modulename and the class name as a tuple (mod, cls)

    """
    try:
        split_name = module_dot_class.rsplit(".", 1)
    except IndexError:
        # string not contanining enough dots
        msg = "Couldn't split mod.class name: {0}".format(module_dot_class)
        raise LoaderError(msg, plugin=module_dot_class)
    except AttributeError:
        msg = "Plugin name is not a string: {0}".format(module_dot_class)
        raise LoaderError(msg, plugin=module_dot_class)
    if len(split_name) != 2:
        msg = (
            "Expected two elements of mod.class string in {0}"
            " which resulted in {1}"
            ).format(module_dot_class, split_name)
        raise LoaderError(msg, plugin=module_dot_class)
    return split_name


def load_object(plugin_name):
    """
    _load_object_

    Given a module.submodule.thing style string,
    load thing and return it.
    Assumes that the last element is an attr in the
    module denoted by the previous elements

    :param plugin_name: string, name of plugin of form module.submod.thing

    :returns: Imported reference to thing.

    """
    modname, objname = parse_module_class_name(plugin_name)

    try:
        modref = importlib.import_module(modname)
    except ImportError as ex:
        msg = "Error Importing Module: {0}\n".format(modname)
        msg += str(ex)
        raise LoaderError(msg, plugin=plugin_name)
    objref = getattr(modref, objname, None)
    if objref is None:
        msg = "Object {0} is not defined in Module {1}\n".format(
            objname, modname)
        msg += "Unable to load plugin"
        raise LoaderError(msg, plugin=plugin_name)
    return objref


def load_plugin(plugin_name, type_check=None):
    """
    _load_plugin_

    Given a plugin name of the form mod.submod.Class, load the
    module and return an instance of the class.

    To verify the plugin is of the appropriate type, pass a class
    ref as type_check to perform an issubclass test on the
    loaded class

    :param plugin_name: string, name of plugin of form module.Class
    :param type_check: Class object or tuple of objects to be passed to
       issubclass to verify type of plugin

    :returns: Class Reference for the plugin

    """
    classref = load_object(plugin_name)
    if type_check is not None:
        if not issubclass(classref, type_check):
            msg = "Plugin in {0} is not a {1} subclass:\n".format(
                plugin_name, type_check.__name__
            )
            raise LoaderError(msg, plugin=plugin_name)
    return classref
