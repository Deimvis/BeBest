from typing import Any, List

from .inspect import inspect_class_attrs


class SimpleEnum:
    """
    Simple enum

    Example:
    >>> class MyEnum(SimpleEnum):
    >>>     X = 'x'
    >>>     Y = 2
    >>>     Z = None

    >>> MyEnum.names()
    ['X', 'Y', 'Z']
    >>> MyEnum.values()
    ['x', 2, None]

    """

    @classmethod
    def names(cls) -> List[str]:
        """ Return set of field names """
        class_attrs = inspect_class_attrs(cls)
        return [attr[0] for attr in class_attrs]

    @classmethod
    def values(cls) -> List[Any]:
        """ Return set of field values """
        class_attrs = inspect_class_attrs(cls)
        return [attr[1] for attr in class_attrs]
