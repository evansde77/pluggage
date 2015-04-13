#!/usr/bin/env python
"""
loaders

Util methods to load things on the fly

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
        raise LoaderError(description=msg, plugin=module_dot_class)
    except AttributeError:
        msg = "Plugin name is not a string: {0}".format(module_dot_class)
        raise LoaderError(description=msg, plugin=module_dot_class)
    if len(split_name) != 2:
        msg = (
            "Expected two elements of mod.class string in {0}"
            " which resulted in {1}"
            ).format(module_dot_class, split_name)
        raise LoaderError(description=msg, plugin=module_dot_class)
    return split_name


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

    modname, classname = parse_module_class_name(plugin_name)

    try:
        modref = importlib.import_module(modname)
    except ImportError as ex:
        msg = "Error Importing Module: {0}\n".format(modname)
        msg += str(ex)
        raise LoaderError(description=msg, plugin=plugin_name)
    classref = getattr(modref, classname, None)
    if classref is None:
        msg = "Class {0} is not defined in Module {1}\n".format(
            classname, modname)
        msg += "Unable to instantiate plugin"
        raise LoaderError(description=msg, plugin=plugin_name)
    if type_check is not None:
        if not issubclass(classref, type_check):
            msg = "Class {0} in module {1} is not a {2} subclass:\n".format(
                classname, modname, type_check.__name__
            )
            raise LoaderError(description=msg, plugin=plugin_name)
    return classref


def load_plugin_function(plugin_name):
    """
    _load_plugin_function_

    Like load_plugin, but the returned object is expected to be
    a callable instead of a class

    :param plugin_name: String defining plugin in form
       module1.module2.functionName

    :returns: Reference to function

    """
    modname, funcname = parse_module_class_name(plugin_name)
    try:
        modref = importlib.import_module(modname)
    except ImportError as ex:
        msg = "Error Importing Module: {0}\n".format(modname)
        msg += str(ex)
        raise LoaderError(description=msg, plugin=plugin_name)
    funcref = getattr(modref, funcname, None)
    if funcref is None:
        msg = "Function {0} is not defined in Module {1}\n".format(
            funcname, modname)
        msg += "Unable to instantiate plugin"
        raise LoaderError(description=msg, plugin=plugin_name)
    if not callable(funcref):
        msg = "Function Plugin {0} is not callable".format(plugin_name)
        raise LoaderError(description=msg, plugin=plugin_name)
    return funcref