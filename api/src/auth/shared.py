#!/usr/bin/env python3
"""
shared auth data
"""
from __future__ import annotations  # pylint: disable=no-name-in-module

from datetime import datetime, timedelta
from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from typing import Dict, Any

from utils.config import JWT_ISSUER
from utils.enums import UserType

LOGIN_TIME: timedelta = timedelta(hours=2)


class JWTAuthData:
    """
    jwt auth object
    """

    def __init__(self, id: int, user_type: UserType) -> None:  # pylint: disable=redefined-builtin
        self.id = id
        self.user_type = user_type
        self.iss = JWT_ISSUER
        self.exp = datetime.utcnow() + LOGIN_TIME

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> JWTAuthData:
        """
        from dictionary
        """
        new_jwt = cls(data['id'], data['user_type'])
        new_jwt.iss = data['iss']
        new_jwt.exp = data['exp']
        return new_jwt

    def to_json(self) -> Dict[str, Any]:
        """
        Convert to JSON format string representation.
        """
        return vars(self)


class JWTAuthDataSchema(Schema):
    """
    login args
    """
    id = fields.Int(required=True, description="user id")
    user_type = EnumField(UserType, required=True, description="user type")
    iss = fields.String(required=True, description="jwt issuer")
    exp = fields.Int(required=True, description="jwt expiration")

    @post_load
    def make_object(self, data: Dict[str, Any], **_kwargs: Any) -> JWTAuthData:
        """
        create object initialization
        """
        return JWTAuthData.from_dict(data)
