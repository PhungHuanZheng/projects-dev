from __future__ import annotations

from typing import Type, Literal
from abc import ABC, abstractmethod
from dataclasses import dataclass


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
    

class Grid:
    """
    Builds a 2D environment with (x, y) positioning to access values within. Suitable for
    flat environments such as maps.
    """

    def __init__(self, width: int, height: int, cell_type: Type[ICell] | Literal['default'] = 'default') -> None:
        # build grid data
        if cell_type == 'default':
            cell_type = ICell
        self._data: list[list[ICell]] = [[cell_type(x, y) for x in range(width)] for y in range(height)]
        self._shape = (width, height)

    def cell_at(self, x, y) -> ICell:
        """
        Returns `ICell` instance at the grid coordinate `x` and `y` passed.

        Parameters
        ----------
        `x` : `int`
            Zero-indexed x-position of the cell on the grid.
        `y` : `int`
            Zero-indexed y-position of the cell on the grid.

        Returns
        -------
        `ICell`
            `ICell` instance or subclass.
        """

        return self._data[y][x]

    @property
    def shape(self) -> tuple[int, int]:
        """Shape of the `Grid` instance as (width, height)."""

        return self._shape
    
    def display(self) -> None:
        """Displays rows and columns of the `Grid` instance."""

        for row in self._data:
            for cell in row:
                print(cell, end=' ')
            print()