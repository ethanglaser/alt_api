#!/usr/bin/env python3
"""
message object
"""

from typing import Dict, Any
from marshmallow import Schema, fields, post_load


class Message:
    """
    message object
    """

    def __init__(self, message: str) -> None:
        self.message = message


class MessageSchema(Schema):
    """
    message object schema
    """
    message = fields.String(required=True, description="Output message / data")

    @post_load
    def make_object(self, data: Dict[str, Any], **_kwargs: Any) -> Message:
        """
        create object initialization
        """
        return Message(**data)
