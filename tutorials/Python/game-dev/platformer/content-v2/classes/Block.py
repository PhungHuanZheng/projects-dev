from __future__ import annotations

import os
import pygame

from base import BaseEntity
from wrappers import Pos
from constants import FPS


class Block(BaseEntity):
    def __init__(self, base: pygame.Surface, xpos: int, ypos: int, width: int, height: int) -> None:
        super().__init__(base, xpos, ypos, width, height)

    def AI(self):
        pass