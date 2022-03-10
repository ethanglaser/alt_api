#!/usr/bin/env python3
"""
Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.

see https://stackoverflow.com/a/18561055/8623391
"""
from typing import List, Any
from json import JSONEncoder
from datetime import datetime, date

str_classes: List[Any] = [datetime, date]


def _default(self, obj: Any):  # pylint: disable=unused-argument
    """
    default json serialize
    """
    if any(isinstance(obj, elem) for elem in str_classes):
        return str(obj)
    return getattr(obj.__class__, "to_json",
                   _default.default)(obj)  # type: ignore


_default.default = JSONEncoder.default  # type: ignore
JSONEncoder.default = _default  # type: ignore
