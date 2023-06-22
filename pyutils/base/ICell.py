from __future__ import annotations

from abc import ABC


class ICell(ABC):
    """
    Interface dataclass to make new `Cell` objects compatible with the `Grid` class.
    Subclass' `__str__` method should be overwritten to allow call to it through
    `Grid.display`.

    Attributes
    ----------
    `x` : `int`
        Zero-indexed x-position of the cell on the grid.
    `y` : `int`
        Zero-indexed y-position of the cell on the grid.

    Methods
    -------
    :func:`display`
        Prints cell data, used in call to `Grid.display`.
    """

    def __init__(self, x, y) -> None:
        """
        Instantiates an instance of `Grid`.

        Parameters
        ----------
        `x` : `int`
            Zero-indexed x-position of the cell on the grid.
        `y` : `int`
            Zero-indexed y-position of the cell on the grid.
        """

        self.x = x
        self.y = y

    def __str__(self) -> str:
        return '[]'