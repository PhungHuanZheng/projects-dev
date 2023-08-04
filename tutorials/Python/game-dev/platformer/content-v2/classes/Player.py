from __future__ import annotations

import os
import pygame

from base import BaseEntity
from wrappers import Pos
from constants import FPS, VELOCITY, GRAVITY


class Player(BaseEntity):
    def __init__(self, base: pygame.Surface, xpos: int, ypos: int, width: int, height: int) -> None:
        super().__init__(base, xpos, ypos, width, height)

    def AI(self) -> None:
        # handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_d]:
            if keys[pygame.K_a]:
                # change velocity and update sprite direction
                self._vel.x = -Player.VELOCITY
                self.set_animation('run', direction='left')

            if keys[pygame.K_d]:
                # change velocity and update sprite direction
                self._vel.x = Player.VELOCITY
                self.set_animation('run', direction='right')

        else:
            self.set_animation('idle')

        super().AI()
        
    