#!/usr/bin/env python3
"""
datetime objects

custom datetime field from this:
https://github.com/marshmallow-code/marshmallow/issues/656#issuecomment-318587611
"""

from typing import Any
from marshmallow import fields
from datetime import datetime, date


class DateTimeField(fields.DateTime):
    """
    datetime field
    """

    def _deserialize(self, value, *args, **kwargs: Any):
        if isinstance(value, datetime):
            return value

        return super()._deserialize(value, *args, **kwargs)


class DateField(fields.Date):
    """
    date field
    """

    def _deserialize(self, value, *args, **kwargs: Any):
        if isinstance(value, date):
            return value
        return super()._deserialize(value, *args, **kwargs)
