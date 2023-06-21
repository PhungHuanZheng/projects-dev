from __future__ import annotations

from typing import Literal, TypeVar

from interfaces import IBinaryTree


class UniqueBinaryTree(IBinaryTree):
    def __init__(self, value = None) -> None:
        super().__init__(value)

    def depth(self) -> int:
        return super().depth()
    
    def append(self, value) -> None:
        if self._value is None:
            self._value = value
            return 

        # check that value doesn't already exist
        if self.contains(value):
            return
    
        # check value against parent value
        if value > self._value:
            # if right child doesnt exist
            if self._rightChild is None:
                self._rightChild = UniqueBinaryTree(value)
                
            else:
                # go into right child
                self._rightChild.append(value)
            
        else:
            # if right child doesnt exist
            if self._leftChild is None:
                self._leftChild = UniqueBinaryTree(value)

            else:
                # go into left child
                self._leftChild.append(value)
    
    def flatten(self, method: Literal['inorder', 'preorder', 'postorder'] = 'inorder', __list: list = []) -> list:
        return super().flatten(method)
    
    def contains(self, value) -> bool:
        return super().contains(value)
    
    def display(self, method: Literal['inorder', 'preorder', 'postorder'] = 'inorder', indent: str = '\t') -> None:
        return super().display(method, indent)
        
