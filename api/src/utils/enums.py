#!/usr/bin/env python3
"""
BaseEnum objects (better than strings)
"""

from typing import Set, Any, Callable, Tuple, Union, TYPE_CHECKING
from peewee import TextField
from aenum import extend_enum

# hack to get type checking working as expected
if TYPE_CHECKING:
    from enum import Enum as BaseEnum
else:
    from aenum import Enum

    class BaseEnum(str, Enum):
        """
        base enum object
        only works for strings (see https://stackoverflow.com/a/51976841)
        """
        @classmethod
        def has_value(cls, value: str) -> bool:
            """
            Return true / false for whether the input is stored as a value in the enum
            """
            return value in cls.__members__

        @classmethod
        def get_values(cls) -> Set[Any]:
            """
            Return a list of the values stored within the enum
            """
            return set(item.value for item in cls)


class EnumField(TextField):
    """
    This class enable an Enum like field for Peewee
    """

    def __init__(self, choices: Callable, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.choices = choices
        self.max_length = 255

    @staticmethod
    def db_value(value: Any) -> Any:
        """
        get value for database
        """
        return value.value

    def python_value(self, value: Any) -> Union[BaseEnum, Any]:  # pylint: disable=used-before-assignment
        """
        get value for python
        """
        if self.choices.has_value(value):  # type: ignore
            return self.choices(value)

        # cannot cast to enum. return value
        return value


# NOTE - no enums can be on "auto" when they are saved into the database
# this causes bugs!

def combine_enum(CombinedEnum: Any, classes: Tuple[Any, ...]):
    '''
    combine multiple enums

    don't try to return a class directly. otherwise it won't work with pickle.
    pickle needs global space class definitions
    '''
    for curr_class in classes:
        for curr_name, elem in curr_class.__members__.items():  # type: ignore
            extend_enum(CombinedEnum, curr_name, elem.value)


class UserType(BaseEnum):
    """
    enum for the type of a given user
    """
    user = 'user'
    admin = 'admin'
