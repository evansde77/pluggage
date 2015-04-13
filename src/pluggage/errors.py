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
    pass