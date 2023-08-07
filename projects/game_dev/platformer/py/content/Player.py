from __future__ import annotations

import os
import pygame

from _constants import FPS, VELOCITY, GRAVITY
from common import BaseEntity
from helpers.wrappers import Vector


class Player(BaseEntity):
    VELOCTY = VELOCITY

    def __init__(self, base: pygame.Surface, xpos: int, ypos: int, width: int, height: int, has_gravity: bool = True) -> None:
        super().__init__(base, xpos, ypos, width, height, has_gravity)

    @property
    def category(self) -> None:
        return 'PLAYER'

    def AI(self) -> None:
        super().AI()

        # move player based on key pressed
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self._vel.y = -15

        if self._is_falling:
            self.set_animation('fall')

        if all([keys[pygame.K_a], keys[pygame.K_d]]) or all([not keys[pygame.K_a], not keys[pygame.K_d]]):
            self.set_animation('idle')

        elif keys[pygame.K_a] or keys[pygame.K_d]:
            new_velx = 0
            if keys[pygame.K_a]:
                new_velx += -Player.VELOCTY
                self.set_animation('run', direction='LEFT')

            if keys[pygame.K_d]:
                new_velx += Player.VELOCTY
                self.set_animation('run', direction='RIGHT')

            self._vel.x = new_velx
