#!/usr/bin/env python
"""
_errors_

Exception classes for the package

"""


class PluggageError(Exception):
    """
    base class for package errors

    """
    pass


class LoaderError(PluggageError):
    """
    LoaderError

    Indicates a failure to dynamically load a plugin
    """
    def __init__(self, message, plugin=None):
        super(LoaderError, self).__init__(message)
        self.plugin = plugin
