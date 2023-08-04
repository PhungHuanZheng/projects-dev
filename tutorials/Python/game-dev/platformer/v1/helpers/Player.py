from __future__ import annotations

import os
from typing import Literal
import pygame


class Player(pygame.sprite.Sprite):
    """Inheriting from Sprite to handle pixel-perfect collisions."""

    VELOCITY = 5
    GRAVITY = 1
    COLOUR = (255, 0, 0)

    def __init__(self, x: int, y: int, width: int, height: int, asset_path: os.PathLike) -> None:
        self._hitbox = pygame.Rect(x, y, width, height)
        self._mask = None

        self._xvel = 0
        self._yvel = 0
        self._direction: Literal['LEFT', 'RIGHT'] = 'LEFT'

        self._animation_frame = 0
        self._fall_frame = 0

    def move_left(self) -> None:
        self._xvel = -Player.VELOCITY
        self._direction = 'LEFT'
        self._animation_frame = 0

    def move_right(self) -> None:
        self._xvel = Player.VELOCITY
        self._direction = 'RIGHT'
        self._animation_frame = 0

    def AI(self) -> None:
        # get key press and update movement
        keys = pygame.key.get_pressed()
        self._xvel = 0

        if keys[pygame.K_a]:
            self.move_left()
        if keys[pygame.K_d]:
            self.move_right()

        # update gravity
        self._yvel += min(1, (self._fall_frame / 60) * Player.GRAVITY)
        
        # update movement with current velocity
        self._hitbox.x += self._xvel
        self._hitbox.y += self._yvel
        self._fall_frame += 1

    def show(self, window: pygame.Surface) -> None:
        pygame.draw.rect(window, Player.COLOUR, self._hitbox)
        pygame.display.update()
    