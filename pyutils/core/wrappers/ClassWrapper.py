from __future__ import annotations

from typing import Callable


class ClassWrapper:
    """
    Provides functionality when interacting with Python classes, "type" objects.
    """

    def __init__(self, class_: type) -> None:
        """
        Creates an instance of `ClassWrapper`.

        Parameters
        ----------
        `class` : `type`
            `type` object to wrap.
        """

        self.__class = class_

    def bind(self, func: Callable[...], func_name: str) -> None:
        """
        Binds a method to the class instance at run time. Method's first argument name
        must be self to bind properly to the class.

        Parameters
        ----------
        `func` : `Callable[...]`
            Method to be bound to the class.
        `func_name` : `str`
            Name of method to be bound to the class.
        """

        # check that first arg is 'self'
        try:
            if len(func.__code__.co_varnames) < 1 or func.__code__.co_varnames[0] != 'self':
                raise Exception
        except Exception:
            raise ValueError(f'The first argument of func should be "self" to bind correctly to the class instance "{self.__class.__name__}".')

        setattr(self.__class, func_name, func)