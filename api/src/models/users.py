#!/usr/bin/env python3
"""
Team Members model
"""

from __future__ import annotations

from peewee import TextField, BooleanField, UUIDField
from loguru import logger
from typing import Optional, Any, Dict
from argon2 import PasswordHasher
from models.base_model import BaseModel
from utils.enums import EnumField, UserType
from uuid import uuid4


class Users(BaseModel):
    """
    users model
    """
    id = UUIDField(primary_key=True)
    email = TextField(index=True)
    username = TextField(index=True)
    name = TextField()
    password = TextField()
    receives_weekly_report = BooleanField()
    # note - don't change this to "type". it will fail
    user_type = EnumField(UserType)


class User:
    """
    User object
    """

    def __init__(self, email: str, username: str, name: str, password: str, receives_weekly_report: bool,
                 user_type: UserType) -> None:
        self.id = uuid4()
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.receives_weekly_report = receives_weekly_report
        self.user_type = user_type

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> User:
        """
        create from dictionary
        """
        input_dict['user_type'] = UserType[input_dict.pop('type')]

        return cls(**input_dict)


def delete_user(email: Optional[str] = None, username: Optional[str] = None) -> None:
    """
    delete user with given email or username
    """
    if email is None and username is None:
        raise ValueError('email and username both not defined')
    if Users.select().where((Users.email == email) | (Users.username == username)).count() == 0:
        raise ValueError('no user found with given email / username')
    Users.delete().where((Users.email == email) | (Users.username == username)).execute()


def add_user(user: User, upsert: bool = False) -> None:
    """
    utility function for adding new users

    """
    if Users.select().where((Users.email == user.email) |
                            (Users.username == user.username)).count() > 0:
        if not upsert:
            raise ValueError(
                'user with given username or email already registered')
        delete_user(email=user.email)

    hasher = PasswordHasher()
    hashed_password = hasher.hash(user.password)
    user.password = hashed_password
    Users.create(**vars(user))
    logger.info(f'added user {user.email}')
