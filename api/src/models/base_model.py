#!/usr/bin/env python3
"""
Base Model
"""

from peewee import Model
from utils.config import MAIN_DB_CONNECTION_URI
from utils.main import get_database


main_database = get_database(MAIN_DB_CONNECTION_URI)


class BaseModel(Model):
    """
    base model object
    """
    class Meta:
        """
        meta class for db
        """
        database = main_database
