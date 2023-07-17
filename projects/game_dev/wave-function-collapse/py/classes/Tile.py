from __future__ import annotations

import random

from classes.helpers import Pos


class Tile:
    def __init__(self, x: int, y: int, state_count: int) -> None:
        self.pos = Pos(x, y)

        self._final_state = None
        self._all_states = list(range(state_count))
        self.is_collapsed = False

    @property
    def final_state(self) -> int:
        if self._final_state is None:
            raise Exception(f'Tile has not been collapsed yet, final state has {len(self._all_states)} possibilities.')
        return self._final_state
    
    @property
    def entropy(self) -> int:
        return len(self._all_states)
    
    @property
    def possible_states(self) -> list[int]:
        return self._all_states
    
    def set_states(self, new_states: list[int]) -> None:
        self._all_states = new_states

    def collapse(self) -> None:
        self.is_collapsed = True
        self._final_state = self._all_states[random.randint(0, len(self._all_states) - 1)]