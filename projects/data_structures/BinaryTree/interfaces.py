from __future__ import annotations

from typing import Literal, TypeVar, Type
from abc import ABC, abstractmethod


class IBinaryTree(ABC):
    """
    Binary Tree where the number on the right child is greater than the parent and 
    the number on the left child is smaller than the parent. Acts as a base class for
    different variations.
    """

    def __init__(self, value) -> None:
        super().__init__()
        self._value = value

        self._leftChild = None
        self._rightChild = None

    @abstractmethod
    def depth(self) -> int:
        """Finds and returns max depth of the binary tree"""

    @abstractmethod
    def append(self, value) -> None:
        """Adds a new value to the binary tree."""

    @abstractmethod
    def flatten(self, method: Literal['inorder', 'preorder', 'postorder'] = 'inorder') -> list:
        """Traverses and flattens the binary tree with the method passed."""

    @abstractmethod
    def contains(self, value) -> bool:
        """Searches the binary tree and returns whether the value passed exists within."""

    @abstractmethod
    def display(self, method: Literal['inorder', 'preorder', 'postorder'] = 'inorder', indent: str = '\t') -> None:
        """Traverses and prints the binary tree with the method passed with indentation."""