from __future__ import annotations

from typing import Type, Literal
from abc import ABC, abstractmethod
from dataclasses import dataclass

from pyutils.base import ICell

    

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