from __future__ import annotations

import os

import pygame as pg

from Common.constants import PLAYER_JUMP_HEIGHT, PLAYER_VELOCITY
from API.base import BaseEntity


class Player(BaseEntity):
    def __init__(self, base: pg.Surface, x: int, y: int, width: int, height: int) -> None:
        super().__init__(base, x, y, width, height)
        
        # instance attributes to be set when subclassing to game objects/instances
        self.has_gravity = True
        self.has_physics = True
        self.has_collision = True
        self.immune_time = 20
        self.velocity = 5
        self.update_interval = 1

    def AI(self) -> None:
        keys = pg.key.get_pressed()

        # handle jump animations
        # if self.vel.y < -0.1:
        #     self.set_animation(f'jump_{self.direction}')

        # elif self.vel.y > 0.1:
        #     self.set_animation(f'fall_{self.direction}')

        #     if keys[pg.K_SPACE]:
        #         self.set_animation(f'double_jump_{self.direction}')
        #         self.vel.y = -PLAYER_JUMP_HEIGHT
        # else:
        #     if keys[pg.K_SPACE]:
                # self.vel.y = -PLAYER_JUMP_HEIGHT

        if all([keys[pg.K_a], keys[pg.K_d]]) or all([not keys[pg.K_a], not keys[pg.K_d]]):
            self.set_animation(f'idle_{self.direction}')
        
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_VELOCITY
            self.set_direction(Player.LEFT)
            self.set_animation(f'run_{self.direction}')
        if keys[pg.K_d]:
            self.vel.x = PLAYER_VELOCITY
            self.set_direction(Player.RIGHT)
            self.set_animation(f'run_{self.direction}')