from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any, Callable, Iterable

import pygame as pg

from Platformer.Common.constants import FPS, GRAVITY, PLAYER_VELOCITY
from Platformer.Base import BaseEntity
from Platformer.Helpers.Wrappers import Vector
from Platformer.Helpers import SpriteSheet


class BaseTerrain(BaseEntity):
    def __init__(self, base: pg.Surface, x: int, y: int, width: int, height: int) -> None:
        # conditional attributes
        self.has_collision = True
        self.is_fixed = False
        self.jump_count = 0
        
        super().__init__(base, x, y, width, height)
        
    def AI(self) -> None:
        pass