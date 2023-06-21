from __future__ import annotations

from typing import Literal, TypeVar
from abc import ABC, abstractmethod

from interfaces import IBinaryTree


class UniqueBinaryTree(IBinaryTree):
    def __init__(self, value = None) -> None:
        super().__init__(value)

    def depth(self) -> int:
        return super().depth()
    
    def append(self, value) -> None:
        return super().append(value)
        
