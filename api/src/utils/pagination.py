#!/usr/bin/env python3
"""
pagination data
"""
from __future__ import annotations  # pylint: disable=no-name-in-module

from typing import Dict, Any, Optional, List
from marshmallow import Schema, fields, post_load, EXCLUDE
from marshmallow.validate import Range

from utils.enums import BaseEnum
from marshmallow_enum import EnumField

DEFAULT_PER_PAGE: int = 10


class PaginationDataQuery:
    """
    pagination query params
    """

    def __init__(self, page: int, ascend: bool, per_page: Optional[int] = None, order_by: Optional[BaseEnum] = None) -> None:
        self.page = page
        self.ascend = ascend
        self.per_page = per_page
        self.order_by = order_by


def pagination_schema(order_by_options: Optional[BaseEnum] = None, default_order_by: Optional[BaseEnum] = None) -> Any:
    """
    get pagination schema
    """
    if [order_by_options, default_order_by].count(None) == 1:
        raise ValueError('order by options and default must be defined')

    class PaginationDataQuerySchema(Schema):
        """
        pagination data query schema
        """
        page = fields.Int(required=False, description="current page",
                          validate=Range(min=0, error="current page must be greater than or equal to 0"), missing=0)
        ascend = fields.Bool(
            required=False, description="ascending", missing=True)
        per_page = fields.Int(required=False, description="per page",
                              validate=Range(min=1, error="per page must be greater than 0"))
        order_by = None if order_by_options is None else EnumField(
            order_by_options, required=False, missing=default_order_by)

        class Meta:
            """
            schema config
            """
            unknown = EXCLUDE

        @post_load
        def make_object(self, data: Dict[str, Any], **_kwargs: Any) -> PaginationDataQuery:
            """
            create object initialization
            """
            return PaginationDataQuery(**data)

    return PaginationDataQuerySchema


class PaginatedDataRes:
    """
    paginated data res object
    """

    def __init__(self, data: List[Any], count: int) -> None:
        self.data = data
        self.count = count

    def to_json(self) -> Dict[str, Any]:
        """
        Convert to JSON format string representation.
        """
        return vars(self)


def pagination_res(iterable: Any) -> Any:
    """
    create schema for paginated result
    """
    class PaginatedDataResSchema(Schema):
        """
        price data res object schema
        """
        data = fields.Nested(iterable, many=True,
                             required=True, description="paginated data")
        count = fields.Int(
            required=True, description="total number of paginated elements")

        @post_load
        def make_object(self, data: Dict[str, Any], **_kwargs: Any) -> PaginatedDataRes:
            """
            create object initialization
            """
            return PaginatedDataRes(**data)

        class Meta:
            """
            schema config
            """
            unknown = EXCLUDE

    return PaginatedDataResSchema
