from __future__ import annotations

from typing import Literal, TypeVar

from interfaces import IBinaryTree


class UniqueBinaryTree(IBinaryTree):
    def __init__(self, value = None) -> None:
        super().__init__(value)

    def depth(self) -> int:
        return super().depth()
    
    def append(self, value) -> None:
        # if no head value, set as head
        if self._value is None:
            self._value = value
            return 

        # check that value doesn't already exist
        if self.contains(value):
            return
    
        # check value against parent value
        if value > self._value:
            # if right child doesnt exist
            if self._right_child is None:
                self._right_child = UniqueBinaryTree(value)
                
            else:
                # go into right child
                self._right_child.append(value)
            
        else:
            # if right child doesnt exist
            if self._left_child is None:
                self._left_child = UniqueBinaryTree(value)

            else:
                # go into left child
                self._left_child.append(value)
    
    def flatten(self, method: Literal['inorder', 'preorder', 'postorder'] = 'inorder', __list: list = []) -> list:
        return super().flatten(method)
    
    def contains(self, value) -> bool:
        return super().contains(value)
        
