from __future__ import annotations

import os

import pygame as pg

from API.base import BaseEntity


class BaseTerrain(BaseEntity):
    def __init__(self, base: pg.Surface, x: int, y: int, width: int, height: int) -> None:
        super().__init__(base, x, y, width, height)

        self.has_gravity = False
        self.has_physics = False
        self.has_collision = True
        self.immune_time = 0
        self.velocity = 0
        self.update_interval = 1

    def AI(self) -> None:
        pass

