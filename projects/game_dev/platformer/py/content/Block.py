from __future__ import annotations

import os
import pygame

from _constants import FPS, VELOCITY, GRAVITY
from common import BaseEntity
from helpers.wrappers import Vector


class Block(BaseEntity):
    def __init__(self, base: pygame.Surface, xpos: int, ypos: int, width: int, height: int, has_gravity: bool = True) -> None:
        super().__init__(base, xpos, ypos, width, height, has_gravity)

    @property
    def category(self) -> None:
        return 'BLOCK'

    def AI(self) -> None:
        pass

    