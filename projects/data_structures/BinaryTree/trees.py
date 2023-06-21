from __future__ import annotations

from typing import Literal, TypeVar
from abc import ABC, abstractmethod

from BinaryTree.interfaces import IBinaryTree


class UniqueBinaryTree(IBinaryTree):
    def __init__(self, value) -> None:
        super().__init__(value)