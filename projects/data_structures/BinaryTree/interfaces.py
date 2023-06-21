from __future__ import annotations

from typing import Literal, TypeVar, Type
from abc import ABC, abstractmethod


class IBinaryTree(ABC):
    """
    Binary Tree where the number on the right child is greater than the parent and 
    the number on the left child is smaller than the parent. Acts as a base class for
    different variations.
    """

    def __init__(self, value = None) -> None:
        super().__init__()
        self._value = value

        self._left_child: IBinaryTree = None
        self._right_child: IBinaryTree = None

    @property
    def value(self):
        return self._value
    
    @property
    def left(self) -> IBinaryTree:
        return self._left_child
    
    @property
    def right(self) -> IBinaryTree:
        return self._right_child

    @abstractmethod
    def depth(self) -> int:
        """Finds and returns max depth of the binary tree"""

    @abstractmethod
    def append(self, value) -> None:
        """Adds a new value to the binary tree."""

    @abstractmethod
    def flatten(self, method: Literal['inorder', 'preorder', 'postorder'] = 'inorder') -> list:
        """Traverses and flattens the binary tree with the method passed."""

    def contains(self, value) -> bool:
        """Searches the binary tree and returns whether the value passed exists within."""
        # if no head value, return false
        if self._value is None:
            return False
        
        # binary tree naturally supports binary search, linearly go down one branch
        branch = self
        while branch is not None:
            # check if value is branch's value
            if branch.value == value:
                return True

            # check branch children
            if branch.left is not None:
                if self.left.value == value:
                    return True
            if branch.right is not None:
                if branch.right.value == value:
                    return True

            # else check which child to go into
            if value < branch.value:
                if branch.left is not None:
                    branch = branch.left
                    continue

                return False

            if value > branch.value:
                if branch.right is not None:
                    branch = branch.right
                    continue

                return False
            
        return False

    def display(self, method: Literal['inorder', 'preorder', 'postorder'] = 'inorder', indent: str = '\t') -> None:
        """Traverses and prints the binary tree with the method passed with indentation."""
        if method == 'inorder':
            if self._left_child is not None:
                # go left
                self._left_child.display(method=method, indent=indent)

            if self._value is not None:
                # print root
                print(self._value)

            if self._right_child is not None:
                # go right
                self._right_child.display(method=method, indent=indent)

        if method == 'preorder':
            if self._value is not None:
                # print root
                print(self._value)

            if self._left_child is not None:
                # go left
                self._left_child.display(method=method, indent=indent)

            if self._right_child is not None:
                # go right
                self._right_child.display(method=method, indent=indent)

        if method == 'postorder':
            if self._left_child is not None:
                # go left
                self._left_child.display(method=method, indent=indent)

            if self._right_child is not None:
                # go right
                self._right_child.display(method=method, indent=indent)

            if self._value is not None:
                # print root
                print(self._value)