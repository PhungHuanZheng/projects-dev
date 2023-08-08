from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any, Callable, Iterable

import pygame as pg

from Platformer.Common.constants import FPS, GRAVITY, PLAYER_VELOCITY
from Platformer.Base import BaseEntity
from Platformer.Helpers.Wrappers import Vector
from Platformer.Helpers import SpriteSheet


class Player(BaseEntity):
    def __init__(self, base: pg.Surface, x: int, y: int, width: int, height: int) -> None:
        # conditional attributes
        self.has_physics = True
        self.has_gravity = True
        self.has_collision = True
        self.is_fixed = False
        self.is_alive = True
        self.jump_count = 2
        
        super().__init__(base, x, y, width, height)
        
    def AI(self) -> None:
        # get keys pressed
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE]:
            self.vel.y = -11
            self.falling_framecount = 0
        if keys[pg.K_a]:
            self.set_direction('LEFT')
            self.vel.sub(Vector(PLAYER_VELOCITY, 0))
        if keys[pg.K_d]:
            self.set_direction('RIGHT')
            self.vel.add(Vector(PLAYER_VELOCITY, 0))

        # falling/jumping take priority
        if self.vel.y < -0.1:
            self.set_animation(f'jump_{self.direction}')
        elif self.vel.y < -0.1:
            self.set_animation(f'fall_{self.direction}')
        else:
            # idle 
            if not any([keys[pg.K_a], keys[pg.K_d]]) or all([keys[pg.K_a], keys[pg.K_d]]):
                self.set_animation(f'idle_{self.direction}')
            else:
                if keys[pg.K_a]:
                    self.set_animation(f'run_{self.direction}')
                if keys[pg.K_d]:
                    self.set_animation(f'run_{self.direction}')